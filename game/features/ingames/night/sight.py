import dataclasses
import typing
import engine.utils.detections
import engine.types.scene as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.night import NightScene

FAST_LOOK = 12
SLOW_LOOK = 6

def generate_natural_logic(scene: "NightScene"):
    look_offset_x = 0
    mouse_pos = (scene.window._mouse_x, scene.window._mouse_y)

    trigger_keys = [
        ("look_left_fast",  -FAST_LOOK),
        ("look_right_fast",  FAST_LOOK),
        ("look_left_slow",  -SLOW_LOOK),
        ("look_right_slow",  SLOW_LOOK),
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
            look_offset_x = scene.relative_axis_value(strength, "x")
            break

    if look_offset_x:
        apply_sight_offset(scene, look_offset_x)

def apply_sight_offset(scene: "NightScene", offset_x: float):
    if not offset_x:
        return
    if "dark_room" not in scene.cached_ids:
        return

    # -------- limites da visão --------
    current_scene_x = scene.x

    room = scene.entity_by_id(scene.cached_ids["dark_room"])
    if not room:
        return
    room_width = room.drawable.width
    viewport_width = scene.window.width

    max_scene_x = room_width - viewport_width

    desired_scene_x = current_scene_x + offset_x
    
    clamped_val = sorted((0, desired_scene_x, max_scene_x))[1]

    new_scene_x = int(clamped_val)

    real_offset_x = new_scene_x - current_scene_x

    if real_offset_x == 0:
        return

    scene.x = new_scene_x

    # -------- resolve alvos --------
    targets = scene.entities_by_tags(required=["room_movable"])
    if not targets:
        return

    def _transform_entity(entity: scene_types.Entity):
        if entity.name == "dark_room":
            entity.drawable.x = -scene.x
        else:
            entity.drawable.x -= real_offset_x

        return dataclasses.replace(
            entity,
            drawable=entity.drawable,
        )
    
    failed_commits = scene.commit_entities_update_by_id([
            scene_types.EntitiesListByIdConfig(
                self_id=entity.id_,
                relation="replace",
                entity_generator=_transform_entity,
            )
            for entity in targets
        ])

    if failed_commits:
        scene.x -= real_offset_x
        print(f"[DEBUG] Sight logic reverted due to failed commits.")