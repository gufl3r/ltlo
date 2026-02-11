import typing
import game.features.ingames.night.lamp as lamp_feature
import game.features.ingames.night.blanket as blanket_feature
import game.features.ingames.night.player as player_feature

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def process_interaction(scene: "NightScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "toggle_lamp":
            lamp_feature.toggle_lamp(scene, logic_data)
        case "use_blanket":
            blanket_feature.hold_blanket(scene, logic_data)
        case "toggle_foot":
            player_feature.toggle_foot(scene, logic_data)

def process_release_interaction(scene: "NightScene", logic_data: dict):
    blanket_feature.let_go_of_blanket(scene,logic_data)

def process_natural(scene: "NightScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"
        case "mouse_release":
            blanket_feature.let_go_of_blanket(scene, logic["data"])
        case "cover_consequences":
            player_feature.cover_consequences(scene, logic["data"])