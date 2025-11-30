from dishka import make_async_container

from app.infrastructure.di.app_providers.provider import AppProvider
from app.infrastructure.di.entity_providers.group_provider import GroupProvider
from app.infrastructure.di.entity_providers.permission_provider import (
    PermissionProvider,
)
from app.infrastructure.di.entity_providers.user_provider import UserProvider
from app.infrastructure.di.request_providers.providers import RequestProvider


def build_container():
    return make_async_container(
        AppProvider(),
        RequestProvider(),
        UserProvider(),
        PermissionProvider(),
        GroupProvider(),
    )
