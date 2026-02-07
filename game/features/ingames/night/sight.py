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
        look_offset_x = int(scene.relative_coordinate(look_strength, "x"))

        # direção lógica da câmera
        if "look_left" in entity.tags:
            look_offset_x = -look_offset_x

        break

    if not look_offset_x:
        return

    # -------- limites da visão --------
    current_scene_x = scene.x

    room = scene.entities_by_name("dark_room")[0]
    room_width = room.drawable.width
    viewport_width = scene.window.width

    max_scene_x = room_width - viewport_width
    if max_scene_x < 0:
        max_scene_x = 0

    desired_scene_x = current_scene_x + look_offset_x
    clamped_scene_x = sorted((0, desired_scene_x, max_scene_x))[1]

    real_offset_x = clamped_scene_x - current_scene_x
    if not real_offset_x:
        return

    # atualiza posição lógica da câmera
    scene.x = clamped_scene_x

    # -------- resolve alvos --------
    targets = scene.entities_by_tags(required=["room_movable"])
    if not targets:
        return

    # -------- apply (mundo move ao contrário da câmera) --------
    def apply_look_offset(entity: scene_types.Entity):
        entity.drawable.x -= real_offset_x

        return dataclasses.replace(
            entity,
            drawable=entity.drawable,
        )
    
    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=entity.id_,
            relation="replace",
            entity_generator=apply_look_offset,
        )
        for entity in targets
    ])
