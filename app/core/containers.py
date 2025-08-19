from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from logging import basicConfig
from operator import attrgetter
from sys import stdout
from typing import ClassVar, cast

from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

# from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from httpx import AsyncClient, Timeout
from saq import Queue
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.types import Lifespan
from starlette_exporter.middleware import PrometheusMiddleware
from that_depends import BaseContainer, container_context, providers

from app import models
from app.core.config import EnvSecrets
from app.core.db import DBSessionMiddleware
from app.core.logging import setup_logger
from app.core.redis_client import redis_client
from app.repos import ActivityRepo, BuildingRepo, OrganizationRepo, PhoneRepo
from app.resources.exc_handlers import (
    exception_handlers,
)
from app.resources.openapi import app_description, contact, openapi_tags
from app.services.activity import ActivityService
from app.services.building import BuildingService
from app.services.organization import OrganizationService
from app.services.phone import PhoneService

logger = setup_logger(__name__)


async def init_di_context() -> AsyncIterator[None]:
    async with container_context(AppContainer):
        yield


@asynccontextmanager
async def lifespan(app: Callable[[FastAPI], AsyncIterator[None]]) -> AsyncIterator[None]:
    logger.info('Initiate resources at service startup')
    await AppContainer.init_resources()
    yield
    logger.info('Shut down resources at shutdown')
    await AppContainer.tear_down()


class AppContainer(BaseContainer):
    env = providers.Singleton(EnvSecrets)

    db_engine = providers.Singleton(
        create_async_engine,
        url=env.DB_DSN,
        echo=False,
        pool_size=env.PG_POOL_SIZE,
        max_overflow=env.PG_MAX_OVERFLOW,
        pool_recycle=env.PG_POOL_RECYCLE,
    )

    global_redis = providers.Resource(
        redis_client,
        url=env.REDIS_DSN,
    )

    saq_queue = providers.Factory(
        Queue.from_url,
        env.saq_redis_url,
    )

    session_factory = providers.Singleton(
        async_sessionmaker[AsyncSession],
        db_engine.cast,
        expire_on_commit=False,
        autoflush=True,
    )

    apm_config = providers.Dict(
        SERVICE_NAME=env.ELASTIC_APM_SERVICE_NAME,
        SERVICE_VERSION=env.VERSION,
        DEBUG=env.DEBUG,
        SERVER_URL=env.ELASTIC_APM_URL,
        SECRET_TOKEN=env.ELASTIC_APM_SECRET_TOKEN,
        ENVIRONMENT=env.ENV,
        ENABLED=env.ELASTIC_APM_ENABLED,
    )

    apm_client = providers.Factory(
        make_apm_client,
        config=apm_config.cast,
    )

    # Basic middleware
    base_middlewares: ClassVar = [
        providers.Factory(
            Middleware,  # type: ignore[arg-type]
            cls=ElasticAPM,
            client=apm_client.cast,
        ),
        providers.Factory(
            Middleware,
            cls=DBSessionMiddleware,
            session_factory=session_factory.cast,
        ),
        # providers.Factory(
        #     Middleware,
        #     cls=BrotliMiddleware,
        #     quality=env.BROTLI_QUALITY,
        #     lgwin=env.BROTLI_LGWIN,
        #     lgblock=env.BROTLI_LGBLOCK,
        #     minimum_size=env.BROTLI_MINIMUM_SIZE,
        #     gzip_fallback=env.BROTLI_GZIP_FALLBACK,
        # ),
        providers.Factory(
            Middleware,
            cls=PrometheusMiddleware,
            app_name=env.SERVICE_NAME,
        ),
        providers.Factory(
            Middleware,
            cls=CORSMiddleware,
            allow_origins=env.CORS_ALLOW_ORIGINS,
            allow_credentials=env.CORS_ALLOW_CREDENTIALS,
            allow_methods=env.CORS_ALLOW_METHODS,
            allow_headers=env.CORS_ALLOW_HEADERS,
        ),
    ]

    # Add authentication middleware if required
    # Disabled in favor of dependency-based authentication
    # if env.API_TOKEN_REQUIRED:
    #     base_middlewares.insert(
    #         0,
    #         providers.Factory(
    #             Middleware,
    #             cls=APITokenMiddleware,
    #             token=env.API_TOKEN,
    #             header_name=env.API_TOKEN_HEADER,
    #         ),
    #     )

    middlewares = providers.List(*base_middlewares)

    http_timeout = providers.Singleton(
        Timeout,
        timeout=60,
    )

    http_client = providers.Factory(
        AsyncClient,
        timeout=http_timeout.cast,
    )

    logging = providers.Factory(
        basicConfig,
        stream=stdout,
        level=env.LOGGING_LEVEL,
        format=env.LOGGING_FORMAT,
    )

    servers = providers.List(
        providers.Dict(
            url=env.api_root_path_non_empty,
            description=env.ENV,
        ),
    )

    app_factory = providers.Factory(
        FastAPI,
        root_path=env.API_ROOT_PATH,
        title=env.APP_TITLE,
        debug=env.DEBUG,
        version=env.VERSION,
        openapi_url=env.openapi_url if env.ENABLE_DOCS else None,
        docs_url='/docs' if env.ENABLE_DOCS else None,
        redoc_url='/redoc' if env.ENABLE_DOCS else None,
        exception_handlers=exception_handlers,
        description=app_description,
        middleware=middlewares.cast,
        servers=servers.cast,
        openapi_tags=openapi_tags,
        contact=contact,
        lifespan=cast(Lifespan[FastAPI], lifespan),
        generate_unique_id_function=attrgetter('name'),
    )

    phone_repo = providers.Factory(
        PhoneRepo,
        model=models.Phone,
    )
    phone_service = providers.Factory(
        PhoneService,
        repo=phone_repo.cast,
    )
    activity_repo = providers.Factory(
        ActivityRepo,
        model=models.Activity,
    )
    activity_service = providers.Factory(
        ActivityService,
        repo=activity_repo.cast,
    )
    building_repo = providers.Factory(
        BuildingRepo,
        model=models.Building,
    )
    building_service = providers.Factory(
        BuildingService,
        repo=building_repo.cast,
    )
    organization_repo = providers.Factory(
        OrganizationRepo,
        model=models.Organization,
    )
    organization_service = providers.Factory(
        OrganizationService,
        repo=organization_repo.cast,
        phone_service=phone_service.cast,
        building_service=building_service.cast,
    )
