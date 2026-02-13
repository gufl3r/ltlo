import typing

if typing.TYPE_CHECKING:
    from game.subscenes.default.video import VideoSubScene

def process_interaction(scene: "VideoSubScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "skip_video":
            scene.video_player.volume = 0
            return "video_end"

def process_release_interaction(scene: "VideoSubScene", logic_data: dict):
    pass

def process_natural(scene: "VideoSubScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"
        case "video_end":
            return "video_end"