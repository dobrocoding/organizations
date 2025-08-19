from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_api_token
from app.core.containers import AppContainer
from app.core.db import managed_db_session
from app.dependencies.db_session import get_db_session
from app.schemas.organization import (
    OrganizationDetailResponseSchema,
    OrganizationResponseSchema,
)
from app.services.organization import OrganizationService

router = APIRouter(tags=['Organizations'], prefix='/organizations')


@router.get(
    path='/organization/{organization_id}/',
    name='organizations:get_by_id',
)
@managed_db_session
async def get_organization_by_id(
    organization_id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> OrganizationDetailResponseSchema:
    """Get detailed information about an organization by its identifier."""
    return await organization_service.get_organization_detail(
        session=session, organization_id=organization_id
    )


@router.get(
    path='/building/{building_id}/',
    name='buildings:get_organizations',
)
@managed_db_session
async def get_organizations_in_building(
    building_id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Get a list of all organizations in a specific building."""
    return await organization_service.get_organizations_by_building(
        session=session, building_id=building_id
    )


@router.get(
    path='/activity/{activity_id}/',
    name='organizations:get_by_activity',
)
@managed_db_session
async def get_organizations_by_activity(
    activity_id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Get a list of all organizations that belong to the specified activity type."""
    return await organization_service.get_organizations_by_activity(
        session=session, activity_id=activity_id
    )


@router.get(
    path='/search/radius/',
    name='organizations:search_by_radius',
)
@managed_db_session
async def search_organizations_by_radius(
    latitude: Annotated[Decimal, Query(description='Широта центральной точки')],
    longitude: Annotated[Decimal, Query(description='Долгота центральной точки')],
    radius_km: Annotated[Decimal, Query(description='Радиус поиска в километрах')],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Get a list of organizations within a given radius from a specified point on the map."""
    return await organization_service.get_organizations_in_radius(
        session=session,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )


@router.get(
    path='/search/bounds/',
    name='organizations:search_by_bounds',
)
@managed_db_session
async def search_organizations_by_bounds(
    min_lat: Annotated[Decimal, Query(description='Минимальная широта')],
    max_lat: Annotated[Decimal, Query(description='Максимальная широта')],
    min_lng: Annotated[Decimal, Query(description='Минимальная долгота')],
    max_lng: Annotated[Decimal, Query(description='Максимальная долгота')],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Get a list of organizations within a rectangular area on the map."""
    # Validate bounds parameters
    if min_lat >= max_lat:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='min_lat must be less than max_lat',
        )
    if min_lng >= max_lng:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='min_lng must be less than max_lng',
        )

    return await organization_service.get_organizations_in_bounds(
        session=session,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lng=min_lng,
        max_lng=max_lng,
    )


@router.get(
    path='/search/name/',
    name='organizations:search_by_name',
)
@managed_db_session
async def search_organizations_by_name(
    name: Annotated[str, Query(description='Название организации для поиска')],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Search organizations by name."""
    return await organization_service.get_organizations_by_name(session=session, name=name)


@router.get(
    path='/search/',
    name='organizations:search',
)
@managed_db_session
async def search_organizations(
    query: Annotated[str, Query(description='Поисковый запрос (название или описание)')],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    organization_service: Annotated[
        OrganizationService, Depends(AppContainer.organization_service)
    ],
    _: Annotated[str, Depends(get_api_token)],
) -> list[OrganizationResponseSchema]:
    """Search organizations by name or description."""
    return await organization_service.search_organizations(session=session, query=query)
