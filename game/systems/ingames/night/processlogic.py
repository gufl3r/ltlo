import typing

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def process_interaction(scene: "NightScene", logic_data: dict):
    pass

def process_natural(self: "NightScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"