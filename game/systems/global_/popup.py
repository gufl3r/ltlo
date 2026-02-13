import typing
import dataclasses
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.scene import Scene

def info_box_ok(scene: "Scene", logic_data: dict):
    def kill_entity(entity: scene_types.Entity):
        return dataclasses.replace(
            entity,
            ticks_left=0
        )
    popup_entities = scene.entities_by_tags(required=["info_box"])

    if not popup_entities:
        return

    scene.commit_entities_update_by_id(
        [
            scene_types.EntitiesListByIdConfig(
                self_id=entity.id_,
                relation="replace",
                entity_generator=kill_entity
            )
            for entity in popup_entities
        ]
    )
    