import typing

if typing.TYPE_CHECKING:
    from engine.scenes.engine.default.subscenes.pause import PauseSubScene

def process_interaction(scene: "PauseSubScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "exit_to_menu":
            return "exit_to_menu"
        case "resume_game":
            return "resume_game"

def process_release_interaction(scene: "PauseSubScene", logic_data: dict):
    pass

def process_natural(scene: "PauseSubScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"