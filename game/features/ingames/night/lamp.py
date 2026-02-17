import pyglet
import typing
import engine.types.scene as scene_types
import dataclasses

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.night import NightScene

def toggle_lamp(scene: "NightScene", logic_data: dict):
    lamp_id = scene.cached_ids["lamp"]

    def new_lamp(entity: scene_types.Entity):
        states = entity.states.copy()
        
        target_index = -1
        is_on = False

        for i, state in enumerate(states):
            if state.name == "turned_on":
                target_index = i
                is_on = state.data["value"]
                break

        new_is_on = not is_on
        states[target_index] = scene_types.State("turned_on", {"value": new_is_on})

        if new_is_on:
            new_source = scene.assets["animations"]["lamp_on"]
        else:
            new_source = scene.assets["animations"]["lamp_off"]

        old_sprite = entity.drawable
        new_sprite = pyglet.sprite.Sprite(
            img=new_source, 
            x=old_sprite.x, 
            y=old_sprite.y
        )
        new_sprite.width = old_sprite.width
        new_sprite.height = old_sprite.height

        new_tags = entity.tags
        if scene.ANIMATION_LOOP_TAG not in new_tags:
            new_tags = entity.tags + [scene.ANIMATION_LOOP_TAG]

        return dataclasses.replace(
            entity,
            drawable=new_sprite,
            states=states,
            tags=new_tags
        )
    
    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=lamp_id,
            relation="replace",
            entity_generator=new_lamp,
        )
    ])

# pause test
# def toggle_lamp(scene: "NightScene", logic_data: dict):
#     def new_lamp(entity: scene_types.Entity):
#         # acha o estado de pause da animação
#         pause_index, pause_state = next(
#             (i, s) for i, s in enumerate(entity.states)
#             if s.name == "_animation_pause_frame_index"
#         )

#         paused_frame = pause_state.data["value"]

#         # decide novo valor
#         if paused_frame == -1:
#             # pausa no frame atual
#             new_pause_value = entity.drawable.frame_index
#         else:
#             # despausa
#             new_pause_value = -1

#         states = entity.states.copy()
#         states[pause_index] = scene_types.State(
#             "_animation_pause_frame_index",
#             {"value": new_pause_value}
#         )

#         return dataclasses.replace(
#             entity,
#             states=states
#         )

#     lamp_entity_id: int = logic_data["entity_id"]

#     scene.commit_entities_update_by_id([
#         scene_types.EntitiesListByIdConfig(
#             self_id=lamp_entity_id,
#             relation="replace",
#             entity_generator=new_lamp,
#         )
#     ])