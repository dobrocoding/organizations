import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_request_with_valid_token(client: AsyncClient) -> None:
    """Test authenticated request with valid token."""
    headers = {'Authorization': 'Bearer Secunda_demo_token'}

    response = await client.get(
        '/organizations/search/', params={'query': 'test'}, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_authenticated_request_without_token(client: AsyncClient) -> None:
    """Test authenticated request without token."""
    response = await client.get('/organizations/search/', params={'query': 'test'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticated_request_with_invalid_token(client: AsyncClient) -> None:
    """Test authenticated request with invalid token."""
    headers = {'Authorization': 'Bearer invalid-token'}

    response = await client.get(
        '/organizations/search/', params={'query': 'test'}, headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_authenticated_request_with_empty_token(client: AsyncClient) -> None:
    """Test authenticated request with empty token."""
    headers = {'Authorization': 'Bearer '}

    response = await client.get(
        '/organizations/search/', params={'query': 'test'}, headers=headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticated_request_with_wrong_header_name(client: AsyncClient) -> None:
    """Test authenticated request with wrong header name."""
    headers = {'X-API-Token': 'Secunda_demo_token'}

    response = await client.get(
        '/organizations/search/', params={'query': 'test'}, headers=headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticated_request_case_sensitive_token(client: AsyncClient) -> None:
    """Test authenticated request with case sensitive token."""
    headers = {'Authorization': 'Bearer SECUNDA_DEMO_TOKEN'}

    response = await client.get(
        '/organizations/search/', params={'query': 'test'}, headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
