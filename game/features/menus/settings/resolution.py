import utils.save
import typing
import game.types.scenes as scene_types
import pyglet
import utils.registry.gamecapacities as game_capacities

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene


def switch_resolution(scene: "SettingsScene", data: dict) -> None:
    entity_id: int = data["entity_id"]

    button = scene.entity_by_id(entity_id)
    if not button:
        return

    # -------- lógica --------
    resolution_options = game_capacities.RESOLUTION_OPTIONS
    current = scene.save["settings"]["resolution"]
    current_index = resolution_options.index(current)

    new_index = (current_index + 1) % len(resolution_options)
    new_resolution = resolution_options[new_index]
    scene.save["settings"]["resolution"] = new_resolution

    new_text = f"{new_resolution[0]}x{new_resolution[1]}"

    # -------- resolve relation --------
    relation = next(
        (r for r in button.relations if r.name == "button"),
        None
    )

    if not relation:
        return

    label_id = relation.related_to
    label_entity = scene.entity_by_id(label_id)
    if not label_entity:
        return

    # -------- replace --------
    def replace_label(entity: scene_types.Entity):
        drawable = entity.drawable

        if isinstance(drawable, pyglet.text.Label):
            new_label = pyglet.text.Label(
                text=new_text,
                x=drawable.x,
                y=drawable.y,
                width=drawable.width,
                height=drawable.height,
                font_size=drawable.font_size,
                anchor_x=drawable.anchor_x,
                anchor_y=drawable.anchor_y,
                color=drawable.color,
            )

            return scene_types.Entity(
                drawable=new_label,
                name=entity.name,
                ticks_left=entity.ticks_left,
                interaction_name=entity.interaction_name,
                hud=entity.hud,
                tags=entity.tags,
                id=entity.id,
                relations=entity.relations,
            )

        return entity

    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=label_id,
            relation="replace",
            entity_generator=replace_label,
        )
    ])
