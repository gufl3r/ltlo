import dataclasses
import typing
import engine.utils.detections
import engine.types.scene as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.night import NightScene
    from game.scenes.ingames.night.subscenes.underbed import UnderBedSubscene

FAST_LOOK = 12
SLOW_LOOK = 6

def generate_natural_logic(scene: "NightScene | UnderBedSubscene"):
    if not any(name in scene.cached_ids for name in ["dark_room", "under_bed"]):
        return
    look_offset = (0, 0)
    mouse_pos = (scene.window._mouse_x, scene.window._mouse_y)

    trigger_keys = [
        ("look_left_fast",  -FAST_LOOK),
        ("look_right_fast",  FAST_LOOK),
        ("look_left_slow",  -SLOW_LOOK),
        ("look_right_slow",  SLOW_LOOK),
        ("look_down_fast",  -FAST_LOOK),
        ("look_up_fast",     FAST_LOOK),
        ("look_down_slow",  -SLOW_LOOK),
        ("look_up_slow",     SLOW_LOOK),
    ]

    for cache_key, strength in trigger_keys:
        trigger_id = scene.cached_ids.get(cache_key)
        if trigger_id is None: continue

        entity = scene.entity_by_id(trigger_id)
        if not entity: continue

        if engine.utils.detections.point_inside_area(
            mouse_pos,
            ((entity.drawable.x, entity.drawable.y), (entity.drawable.width, entity.drawable.height))
        ):
            look_offset = (
                (scene.relative_axis_value(strength, "x"), 0) 
                if any(direction in cache_key for direction in ["left", "right"]) else 
                (0, scene.relative_axis_value(strength, "y"))
            )
            break

    bg = scene.entity_by_id(scene.cached_ids["dark_room" if "dark_room" in scene.cached_ids else "under_bed"])
    if bg and look_offset != (0, 0):
        apply_sight_offset(scene, look_offset, bg)

def apply_sight_offset(
    scene: "NightScene | UnderBedSubscene",
    offset: tuple[int, int],
    anchor_entity: scene_types.Entity,
):
    offset_x, offset_y = offset

    if not offset_x and not offset_y:
        return

    if not anchor_entity:
        return

    # -------- limites da visão --------
    current_scene_x = scene.x
    current_scene_y = scene.y

    room_width = anchor_entity.drawable.width
    room_height = anchor_entity.drawable.height

    viewport_width = scene.window.width
    viewport_height = scene.window.height

    max_scene_x = room_width - viewport_width
    max_scene_y = room_height - viewport_height

    desired_scene_x = current_scene_x + offset_x
    desired_scene_y = current_scene_y + offset_y

    clamped_x = sorted((0, desired_scene_x, max_scene_x))[1]
    clamped_y = sorted((0, desired_scene_y, max_scene_y))[1]

    new_scene_x = clamped_x
    new_scene_y = clamped_y

    real_offset_x = new_scene_x - current_scene_x
    real_offset_y = new_scene_y - current_scene_y

    if real_offset_x == 0 and real_offset_y == 0:
        return

    scene.x = new_scene_x
    scene.y = new_scene_y

    # -------- resolve alvos --------
    targets = scene.entities_by_tags(required=["movable"])
    if not targets:
        return

    def _transform_entity(entity: scene_types.Entity):
        entity.drawable.x -= real_offset_x
        entity.drawable.y -= real_offset_y

        return dataclasses.replace(
            entity,
            drawable=entity.drawable,
        )

    failed_commits = scene.commit_entities_update_by_id([
        scene_types.EntityInitializerConfig(
            self_id=entity.id_,
            relation="replace",
            entity_generator=_transform_entity,
        )
        for entity in targets
    ])

    if failed_commits:
        scene.x -= real_offset_x
        scene.y -= real_offset_y
        print("[DEBUG] Sight logic reverted due to failed commits.")