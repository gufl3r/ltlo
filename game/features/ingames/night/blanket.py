import typing
import game.types.scenes as scene_types
import dataclasses
import copy

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

TENSION = 0.075

def generate_natural_logic(scene: "NightScene"):
    def new_blanket(entity: scene_types.Entity):
        drawable = entity.drawable
        drawable.y = blanket_y
        return dataclasses.replace(
            entity,
            drawable=drawable
        )

    blanket_entity = scene.entities_by_name("blanket")[0]
    held_state = next(state for state in blanket_entity.states if state.name == "held")
    held = held_state.data["value"]

    current_y = blanket_entity.drawable.y
    blanket_y = current_y

    # 1. Define o Alvo
    target_y = scene.save["settings"]["resolution"][1] * -0.9
    if held:
        target_y = scene.window._mouse_y - blanket_entity.drawable.height + scene.save["settings"]["resolution"][1] * 0.05

    diff = target_y - current_y

    if abs(diff) < 1.0:
        blanket_y = target_y
    else:
        step = diff * TENSION
        if abs(step) < 1.0:
            if step > 0:
                step += 1
            else:
                step -= 1

        blanket_y += step

    if int(blanket_y) != int(current_y):
        scene.commit_entities_update_by_id([
            scene_types.EntitiesListByIdConfig(
                self_id=blanket_entity.id_,
                relation="replace",
                entity_generator=new_blanket,
            )
        ])

def hold_blanket(scene: "NightScene", logic_data: dict):
    def new_blanket(entity: scene_types.Entity):
        states = copy.deepcopy(entity.states)
        for i, state in enumerate(states):
            if state.name == "held":
                states[i] = scene_types.State(name="held",data={"value": True})
                break
        return dataclasses.replace(
            entity,
            states=states
        )
    blanket_entity_id: int = logic_data["entity_id"]
    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=blanket_entity_id,
            relation="replace",
            entity_generator=new_blanket,
        )
    ])

def let_go_of_blanket(scene: "NightScene", logic_data: dict):
    def new_blanket(entity: scene_types.Entity):
        states = copy.deepcopy(entity.states)
        for i, state in enumerate(states):
            if state.name == "held":
                states[i] = scene_types.State(name="held",data={"value": False})
                break
        return dataclasses.replace(
            entity,
            states=states
        )
    blanket_entity = scene.entities_by_name("blanket")[0]
    blanket_entity_id: int = blanket_entity.id_
    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            self_id=blanket_entity_id,
            relation="replace",
            entity_generator=new_blanket,
        )
    ])