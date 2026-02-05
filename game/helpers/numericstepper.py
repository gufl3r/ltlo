import typing
import game.types.scenes as scene_types
import utils.registry.runtimeconfig as runtime_config

if typing.TYPE_CHECKING:
    from game.scenes.scene import Scene

def try_relate(scene: "Scene", i: int, entity: scene_types.Entity):
    if "numeric_stepper" not in entity.tags:
        return []

    if any(rel.name == "numeric_stepper" for rel in entity.relations):
        return []

    if "decrease" in entity.tags:
        target_index = i + runtime_config.UI_OFFSETS["numeric_stepper"]["decrease_to_value"]
    else:
        target_index = i + runtime_config.UI_OFFSETS["numeric_stepper"]["increase_to_value"]

    candidate = scene._entities[target_index]

    return [
        scene_types.Relation(
            name="numeric_stepper",
            related_to=candidate.id
        )
    ]