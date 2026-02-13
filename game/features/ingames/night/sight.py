import dataclasses
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
        look_offset_x = scene.relative_axis_value(look_strength, "x")

        if "look_left" in entity.tags:
            look_offset_x = -look_offset_x
        break

    # Delega a movimentação para a função standalone
    if look_offset_x:
        apply_sight_offset(scene, look_offset_x)

def apply_sight_offset(scene: "NightScene", offset_x: float):
    if not offset_x:
        return

    # -------- limites da visão --------
    current_scene_x = scene.x # assumindo que já é int, mas garante

    room = scene.entities_by_name("dark_room")[0]
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