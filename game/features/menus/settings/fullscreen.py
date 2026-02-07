import dataclasses
import pyglet
import typing
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

def toggle_fullscreen(scene: "SettingsScene", data: dict) -> None:
    entity_id: int = data["entity_id"]

    button = scene.entity_by_id(entity_id)
    if not button:
        return

    # alterna estado
    enabled = not scene.save["settings"]["fullscreen"]
    scene.save["settings"]["fullscreen"] = enabled

    new_color = (0, 255, 0) if enabled else (255, 0, 0)

    def replace_button(entity: scene_types.Entity):
        entity.drawable.color = new_color

        return dataclasses.replace(
            entity,
            drawable=entity.drawable,
        )

    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=button.id_,
            relation="replace",
            entity_generator=replace_button,
        )
    ])