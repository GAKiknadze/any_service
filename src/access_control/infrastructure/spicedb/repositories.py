from authzed.api.v1 import (
    AsyncClient,
    CheckPermissionRequest,
    CheckPermissionResponse,
    DeleteRelationshipsRequest,
    ObjectReference,
    Relationship,
    RelationshipFilter,
    RelationshipUpdate,
    SubjectFilter,
    SubjectReference,
    WriteRelationshipsRequest,
)

from src.access_control.domain import entities


class SpiceDBPermissionRepository:
    def __init__(self, client: AsyncClient):
        self.__client = client

    async def add_permission(
        self,
        subject: entities.EntityReference,
        resource: entities.EntityReference,
        permission: entities.Permission,
    ) -> None:
        await self.__client.WriteRelationships(
            WriteRelationshipsRequest(
                updates=[
                    RelationshipUpdate(
                        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
                        relationship=Relationship(
                            resource=ObjectReference(
                                object_type=resource.entity_type,
                                object_id=resource.entity_id,
                            ),
                            relation=permission.name,
                            subject=SubjectReference(
                                object=ObjectReference(
                                    object_type=subject.entity_type,
                                    object_id=subject.entity_id,
                                )
                            ),
                        ),
                    )
                ]
            )
        )

    async def remove_object(self, object: entities.EntityReference) -> None:
        await self.__client.DeleteRelationships(
            DeleteRelationshipsRequest(
                RelationshipFilter(
                    resource_type=object.entity_type,
                    optional_resource_id=object.entity_id,
                )
            )
        )

    async def remove_permission(
        self,
        subject: entities.EntityReference,
        resource: entities.EntityReference,
        permission: entities.Permission,
    ) -> None:
        await self.__client.DeleteRelationships(
            DeleteRelationshipsRequest(
                RelationshipFilter(
                    resource_type=resource.entity_type,
                    optional_resource_id=resource.entity_id,
                    optional_relation=permission.name,
                    optional_subject_filter=SubjectFilter(
                        subject_type=subject.entity_type,
                        optional_subject_id=subject.entity_id,
                    ),
                )
            )
        )

    async def check_permission(
        self,
        subject: entities.EntityReference,
        resource: entities.EntityReference,
        permission: entities.Permission,
    ) -> bool:
        resp = await self.__client.CheckPermission(
            CheckPermissionRequest(
                resource=ObjectReference(
                    object_type=resource.entity_type, object_id=resource.entity_id
                ),
                permission=permission.name,
                subject=SubjectReference(
                    object=ObjectReference(
                        object_type=subject.entity_type, object_id=subject.entity_id
                    )
                ),
            )
        )

        return (
            resp.permissionship == CheckPermissionResponse.PERMISSIONSHIP_HAS_PERMISSION
        )
