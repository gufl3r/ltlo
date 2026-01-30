import typing
import utils.detections
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

FAST_LOOK = 12
SLOW_LOOK = 6

def generate_natural_logic(scene: "NightScene"):
    look_offset_x = 0

    # -------- detecta look trigger --------
    for entity in reversed(scene._entities):
        if entity.name != "look_trigger":
            continue

        if not utils.detections.point_inside_area(
            (scene.window._mouse_x, scene.window._mouse_y),
            (entity.drawable.position, (entity.drawable.width, entity.drawable.height))
        ):
            continue

        look_strength = FAST_LOOK if "look_fast" in entity.tags else SLOW_LOOK
        look_offset_x = int(scene.relative_coordinate(look_strength, "x"))

        if "look_right" in entity.tags:
            look_offset_x = -look_offset_x

        break

    if not look_offset_x:
        return

    # -------- resolve alvos via helper --------
    targets = scene.entities_by_tags(required=["room_movable"])
    if not targets:
        return

    # -------- apply --------
    def apply_look_offset(entity: scene_types.Entity):
        drawable = entity.drawable
        drawable.x += look_offset_x

        return scene_types.Entity(
            drawable=drawable,
            name=entity.name,
            ticks_left=entity.ticks_left,
            interaction_name=entity.interaction_name,
            hud=entity.hud,
            tags=entity.tags,
            id=entity.id,
            relations=entity.relations,
        )

    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=entity.id,
            relation="replace",
            entity_generator=apply_look_offset,
        )
        for entity in targets
    ])
