from secrets import token_urlsafe
from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings

from app.resources.regexps import semver_re

type LoggingLevel = Literal[
    'CRITICAL',
    'FATAL',
    'ERROR',
    'WARNING',
    'WARN',
    'INFO',
    'DEBUG',
    'NOTSET',
]


class EnvSecrets(BaseSettings):
    class Config:
        env_file = '.env'

    SERVICE_NAME: str = 'organizations-backend'
    APP_TITLE: str = 'Organizations Management System'
    DEBUG: bool = False
    ENV: str = 'dev'
    VERSION: Annotated[str, Field(pattern=semver_re)] = '0.1.0'
    API_ROOT_PATH: str = ''
    OPENAPI_URL: str = '/openapi.json'

    DB_DSN: str = 'postgresql+asyncpg://user:password@postgres/database'
    PG_POOL_SIZE: int = 10
    PG_MAX_OVERFLOW: int = 5
    PG_POOL_RECYCLE: int = 1800

    REDIS_DSN: str = 'redis://redis'

    AUTH_USERNAME: str = 'user'
    AUTH_PASSWORD: str = Field(default_factory=lambda: token_urlsafe(16))

    # API Token configuration
    API_TOKEN: str = Field(
        default='Secunda_demo_token',
        description='Static API token for authentication',
    )
    API_TOKEN_HEADER: str = 'X-API-Token'
    API_TOKEN_REQUIRED: bool = True

    DOCS_USERNAME: str = 'test'
    DOCS_PASSWORD: str = 'test'
    ENABLE_DOCS: bool = True

    BROTLI_QUALITY: int = 4
    BROTLI_LGWIN: int = 22
    BROTLI_LGBLOCK: int = 0
    BROTLI_MINIMUM_SIZE: int = 400
    BROTLI_GZIP_FALLBACK: bool = True

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True

    LOGGING_LEVEL: LoggingLevel = 'INFO'
    LOGGING_FORMAT: str = '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'

    HASH_ALGO: str = 'sha256'
    HASH_ITERATIONS: int = 100000
    HASH_DKLEN: int = 128

    FILE_ALLOWED_CONTENT_TYPES: list[str] = [
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/webp',
        'application/pdf',
    ]
    FILE_ALLOWED_MAX_SIZE: int = 50 * 1024 * 1024  # 50MB
    VERIFICATION_ALLOWED_CONTENT_TYPES: list[str] = [
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/webp',
        'application/pdf',
    ]
    VERIFICATION_ALLOWED_MAX_SIZE: int = 20 * 1024 * 1024  # 20MB

    ELASTIC_APM_URL: str = 'http://apm-server-apm-http.monitoring.svc.cluster.local:8200'
    ELASTIC_APM_ENABLED: bool = True
    ELASTIC_APM_SECRET_TOKEN: str = ''
    ELASTIC_APM_SERVICE_NAME: str = 'organizations-backend'

    EMAIL_FOR_WITHDRAWAL_INFO: str = 'team@unovay.com'

    ADD_MONEY_PURPOSE_OF_PAYMENT: str = (
        'Account Top Up under T&C agreement with Sungai Wang Services SDN BHD'
    )

    @property
    def saq_redis_url(self) -> str:
        return f'{self.REDIS_DSN}/0'

    @property
    def openapi_url(self) -> str:
        return self.API_ROOT_PATH + self.OPENAPI_URL

    @property
    def api_root_path_non_empty(self) -> str:
        return self.API_ROOT_PATH or '/'


env_secrets = EnvSecrets()
