import typing
import game.features.ingames.night.lamp as lamp_feature

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def process_interaction(scene: "NightScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "toggle_lamp":
            lamp_feature.toggle_lamp(scene, logic_data)

def process_natural(self: "NightScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"