import uuid
from decimal import Decimal

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import BuildingFactory, OrganizationFactory

# Test constants
EXPECTED_ORGANIZATIONS_COUNT = 2


@pytest.mark.asyncio
async def test_get_organizations_in_building(
    client: AsyncClient, db_session: AsyncSession, api_headers: dict[str, str]
) -> None:
    """Test getting organizations in building."""
    # Create building and organizations
    building = BuildingFactory.build()
    org1 = OrganizationFactory.build_with_building(building.id)
    org2 = OrganizationFactory.build_with_building(building.id)

    db_session.add_all([building, org1, org2])
    await db_session.commit()

    response = await client.get(f'/organizations/building/{building.id}/', headers=api_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == EXPECTED_ORGANIZATIONS_COUNT

    org_ids = {str(org1.id), str(org2.id)}
    returned_ids = {item['id'] for item in data}
    assert org_ids == returned_ids


@pytest.mark.asyncio
async def test_get_organizations_in_building_empty(
    client: AsyncClient, db_session: AsyncSession, api_headers: dict[str, str]
) -> None:
    """Test getting organizations in empty building."""
    building = BuildingFactory.build()
    db_session.add(building)
    await db_session.commit()

    response = await client.get(f'/organizations/building/{building.id}/', headers=api_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_search_organizations_by_radius(
    client: AsyncClient, db_session: AsyncSession, api_headers: dict[str, str]
) -> None:
    """Test searching organizations by radius."""
    # Create buildings in Moscow
    building1 = BuildingFactory.build_in_moscow()
    building2 = BuildingFactory.build_in_moscow()
    # Create building far from Moscow
    far_building = BuildingFactory.build(
        latitude=55.7558 + 1.0,  # 1 degree north
        longitude=37.6176 + 1.0,  # 1 degree east
    )

    # Create organizations in buildings
    org1 = OrganizationFactory.build_with_building(building1.id)
    org2 = OrganizationFactory.build_with_building(building2.id)
    far_org = OrganizationFactory.build_with_building(far_building.id)

    db_session.add_all([building1, building2, far_building, org1, org2, far_org])
    await db_session.commit()

    response = await client.get(
        '/organizations/search/radius/',
        params={'latitude': 55.7558, 'longitude': 37.6176, 'radius_km': 5.0},
        headers=api_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    # Should find organizations in Moscow, but not the distant organization
    org_ids = {str(org1.id), str(org2.id)}
    returned_ids = {item['id'] for item in data}
    assert org_ids == returned_ids
    assert str(far_org.id) not in returned_ids


@pytest.mark.asyncio
async def test_search_organizations_by_bounds(
    client: AsyncClient, db_session: AsyncSession, api_headers: dict[str, str]
) -> None:
    """Test searching organizations by bounds."""
    # Create buildings in different locations with fixed coordinates
    building1 = BuildingFactory.build(latitude=Decimal('55.7558'), longitude=Decimal('37.6176'))
    building2 = BuildingFactory.build(
        latitude=Decimal('55.7558') + Decimal('0.001'),
        longitude=Decimal('37.6176') + Decimal('0.001'),
    )
    # Create building outside the area
    outside_building = BuildingFactory.build(
        latitude=Decimal('55.7558') + Decimal('0.1'), longitude=Decimal('37.6176') + Decimal('0.1')
    )

    # Create organizations in buildings
    org1 = OrganizationFactory.build_with_building(building1.id)
    org2 = OrganizationFactory.build_with_building(building2.id)
    outside_org = OrganizationFactory.build_with_building(outside_building.id)

    db_session.add_all([building1, building2, outside_building, org1, org2, outside_org])
    await db_session.commit()

    response = await client.get(
        '/organizations/search/bounds/',
        params={
            'min_lat': 55.7550,
            'max_lat': 55.7560,
            'min_lng': 37.6170,
            'max_lng': 37.6180,
        },
        headers=api_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    # Should find organizations in the area, but not outside it
    returned_ids = {item['id'] for item in data}
    # Check that we get at least one organization in the area
    assert len(data) >= 1
    # Check that outside organization is not found
    assert str(outside_org.id) not in returned_ids


@pytest.mark.asyncio
async def test_search_organizations_invalid_radius_params(
    client: AsyncClient, api_headers: dict[str, str]
) -> None:
    """Test searching organizations with invalid radius parameters."""
    response = await client.get(
        '/organizations/search/radius/',
        params={'latitude': 'invalid', 'longitude': 37.6176, 'radius_km': 5.0},
        headers=api_headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_search_organizations_invalid_bounds_params(
    client: AsyncClient, api_headers: dict[str, str]
) -> None:
    """Test searching organizations with invalid bounds parameters."""
    response = await client.get(
        '/organizations/search/bounds/',
        params={
            'min_lat': 55.7560,  # min greater than max
            'max_lat': 55.7550,
            'min_lng': 37.6170,
            'max_lng': 37.6180,
        },
        headers=api_headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_organizations_in_nonexistent_building(
    client: AsyncClient, api_headers: dict[str, str]
) -> None:
    """Test getting organizations in non-existent building."""
    fake_id = str(uuid.uuid4())

    response = await client.get(f'/organizations/building/{fake_id}/', headers=api_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
