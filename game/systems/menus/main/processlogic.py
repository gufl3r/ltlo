import typing

if typing.TYPE_CHECKING:
    from game.scenes.menus.main import MainMenuScene

def process_interaction(scene: "MainMenuScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "start_game":
            return "ingame"

        case "open_settings":
            return "settings_scene"

def process_natural(scene: "MainMenuScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"