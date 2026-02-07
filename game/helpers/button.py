import typing
import game.types.scenes as scene_types
import utils.registry.runtimeconfig as runtime_config

if typing.TYPE_CHECKING:
    from game.scenes.scene import Scene

def try_relate(scene: "Scene", i: int, entity: scene_types.Entity):
    if "button_rect" not in entity.tags:
        return []

    if any(relation.name == "button" for relation in entity.relations):
        return []

    label = scene._entities[i + runtime_config.UI_OFFSETS["button"]["rect_to_label"]]

    return [
        scene_types.Relation(
            name="button",
            related_to=label.id_
        )
    ]