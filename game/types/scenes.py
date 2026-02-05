import dataclasses
import typing

@dataclasses.dataclass
class EntitiesListByIdConfig:
    entity_generator: typing.Callable
    relation: typing.Literal["behind", "replace", None] = None
    anchor_id: int | None = None
    self_id: int | None = None

@dataclasses.dataclass
class CommitTracker:
    config: EntitiesListByIdConfig
    found_anchor: bool = False
    found_self: bool = False
    done: bool = False

@dataclasses.dataclass
class Relation:
    name: str
    related_to: int

@dataclasses.dataclass
class State:
    name: str
    data: dict

@dataclasses.dataclass
class Entity:
    drawable: typing.Any
    name: str
    ticks_left: int
    interaction_name: str | None
    hud: bool
    id: int = 0
    tags: list[str] = dataclasses.field(default_factory=list)
    states: list[State] = dataclasses.field(default_factory=list)
    relations: list[Relation] = dataclasses.field(default_factory=list)