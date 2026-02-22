import typing

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.subscenes.underbed import UnderBedSubscene

def process_interaction(scene: "UnderBedSubscene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "exit_under_bed":
            return "exit_under_bed"

        case "request_pause":
            scene.pause()
        case "exit_to_menu":
            return "exit_to_menu"

def process_release_interaction(scene: "UnderBedSubscene", logic_data: dict):
    pass

def process_natural(scene: "UnderBedSubscene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"