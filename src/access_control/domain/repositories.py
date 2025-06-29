from typing import Protocol

from .entities import EntityReference, Permission


class PermissionRepository(Protocol):
    async def add_permission(
        self,
        subject: EntityReference,
        resource: EntityReference,
        permission: Permission,
    ) -> None: ...
    async def remove_object(self, object: EntityReference) -> None: ...
    async def remove_permission(
        self,
        subject: EntityReference,
        resource: EntityReference,
        permission: Permission,
    ) -> None: ...
    async def check_permission(
        self,
        subject: EntityReference,
        resource: EntityReference,
        permission: Permission,
    ) -> bool: ...
