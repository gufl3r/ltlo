import pyglet
import typing
import game.types.scenes as scene_types
import dataclasses

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def toggle_lamp(scene: "NightScene", logic_data: dict):
    def new_lamp(entity: scene_types.Entity):
        index, state = next((index, state) for index, state in enumerate(entity.states) if state.name == "turned_on")
        turned_on = not state.data["value"]
        states = entity.states.copy()
        states[index] = scene_types.State("turned_on", {"value": turned_on})
        source = scene.assets["animations"]["lamp_off"]
        if turned_on:
            source = scene.assets["animations"]["lamp_on"]
        return dataclasses.replace(
            entity,
            drawable=pyglet.sprite.Sprite(source, x=entity.drawable.x, y=entity.drawable.y),
            states=states,
            tags=entity.tags if scene.ANIMATION_LOOP_TAG in entity.tags else entity.tags + [scene.ANIMATION_LOOP_TAG]
        )
    
    lamp_entity_id: int = logic_data["entity_id"]
    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=lamp_entity_id,
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