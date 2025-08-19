from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from app.core.config import env_secrets

# Создаем security scheme для Swagger
security = HTTPBearer(
    scheme_name='API Token',
    description='Введите API токен в формате: Bearer <your-token>',
    auto_error=False,
)


def get_api_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    """Dependency для получения API токена из Bearer заголовка."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='API токен не предоставлен',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if credentials.credentials != env_secrets.API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Неверный API токен',
        )

    return credentials.credentials


class APITokenMiddleware(BaseHTTPMiddleware):
    """Middleware for checking static API token."""

    def __init__(self, app: ASGIApp, token: str, header_name: str = 'X-API-Token'):
        super().__init__(app)
        self.token = token
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        # Skip check for documentation and health check
        if self._should_skip_auth(request):
            return await call_next(request)

        # Check for token in header
        api_token = request.headers.get(self.header_name)

        # Also check for Bearer token in Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            api_token = auth_header.split(' ')[1]

        if not api_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail': 'API токен не предоставлен'},
                headers={'WWW-Authenticate': f'{self.header_name}, Bearer'},
            )

        if api_token != self.token:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={'detail': 'Неверный API токен'},
            )

        return await call_next(request)

    @staticmethod
    def _should_skip_auth(request: Request) -> bool:
        """Determines whether authentication should be skipped for this request."""
        path = request.url.path

        # Skip documentation
        if path.startswith(('/docs', '/redoc', '/openapi')):
            return True

        # Skip health check endpoints (if any)
        return path.startswith(('/health', '/ping'))


def create_api_token_middleware(app: ASGIApp) -> APITokenMiddleware:
    """Factory for creating middleware with token from configuration."""
    return APITokenMiddleware(
        app=app,
        token=env_secrets.API_TOKEN,
        header_name=env_secrets.API_TOKEN_HEADER,
    )
