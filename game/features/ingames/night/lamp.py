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