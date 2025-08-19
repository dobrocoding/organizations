from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.core.config import env_secrets


def verify_api_token(request: Request) -> bool:
    """Dependency для проверки API токена."""
    api_token = request.headers.get(env_secrets.API_TOKEN_HEADER)

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='API токен не предоставлен',
            headers={'WWW-Authenticate': env_secrets.API_TOKEN_HEADER},
        )

    if api_token != env_secrets.API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Неверный API токен',
        )

    return True

    # Typed dependency for use in endpoints


API_TOKEN_AUTH = Annotated[bool, Depends(verify_api_token)]
