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

    def replace_button(entity):
        drawable = entity.drawable

        # Label não muda (texto fixo)
        if isinstance(drawable, pyglet.text.Label):
            return entity

        # Retângulo muda de cor
        if isinstance(drawable, pyglet.shapes.RoundedRectangle):
            new_rect = pyglet.shapes.RoundedRectangle(
                x=drawable.x,
                y=drawable.y,
                width=drawable.width,
                height=drawable.height,
                radius=drawable.radius,
                color=new_color,
            )

            return scene_types.Entity(
                drawable=new_rect,
                name=entity.name,
                ticks_left=entity.ticks_left,
                interaction_name=entity.interaction_name,
                hud=entity.hud,
                tags=entity.tags,
                id=entity.id,
            )

        return entity

    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=button.id,
            relation="replace",
            entity_generator=replace_button,
        )
    ])