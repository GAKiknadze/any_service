from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    name: str


@dataclass(frozen=True)
class EntityReference:
    entity_type: str
    entity_id: str
