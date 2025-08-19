import operator
from typing import Any, TypedDict, cast

from pydantic import AnyUrl


class OpenAPITag(TypedDict):
    name: str
    description: str


class Contact(TypedDict):
    name: str
    email: str
    url: AnyUrl


app_description: str = 'Backend service'
_openapi_tags: list[OpenAPITag] = [
    OpenAPITag(name='Organizations', description='Manages organizations.'),
]
_contact: Contact = Contact(
    name='Ilia Boiarintsev',
    email='theilyaboyarintsev@gmail.com',
    url=AnyUrl('https://github.com/dobrocoding'),
)

# Security scheme configuration
security_schemes = {
    'Bearer': {
        'type': 'http',
        'scheme': 'bearer',
        'description': 'API токен для аутентификации. Введите токен в формате: Bearer <your-token>',
    }
}

openapi_tags = cast(list[dict[str, Any]], sorted(_openapi_tags, key=operator.itemgetter('name')))
contact = cast(dict[str, Any], _contact)
