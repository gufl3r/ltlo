import pyglet
import typing
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

STEP = 0.05  # 5%

import pyglet
import typing
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

STEP = 0.05  # 5%

def numeric_stepper_change(scene: "SettingsScene", data: dict):
    entity_id: int = data["entity_id"]

    button = scene.entity_by_id(entity_id)
    if not button or not button.relations:
        return

    # -------- domínio (setting) --------
    domain_tag = next(
        t for t in button.tags
        if t.startswith("domain:")
    )
    setting_name = domain_tag.split(":", 1)[1]

    # -------- direção --------
    delta = STEP if "increase" in button.tags else -STEP

    # -------- calcula novo valor --------
    current = scene.save["settings"]["audio"][setting_name]
    new_value = round(sorted((0, current + delta, 1))[1], 2)

    scene.save["settings"]["audio"][setting_name] = new_value
    new_text = f"{int(new_value * 100)}%"

    # -------- value via relation --------
    relation = next(
        (r for r in button.relations if r.name == "numeric_stepper"),
        None
    )

    if not relation:
        return

    value_id = relation.related_to
    value_entity = scene.entity_by_id(value_id)
    if not value_entity:
        return

    def replace_value_label(entity: scene_types.Entity):
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
            self_id=value_id,
            relation="replace",
            entity_generator=replace_value_label,
        )
    ])
