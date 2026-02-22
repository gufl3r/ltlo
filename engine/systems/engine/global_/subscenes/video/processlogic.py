import typing
import engine.types.scene as scene_types
import engine.factories.generic as generic_entities

if typing.TYPE_CHECKING:
    from engine.scenes.engine.default.subscenes.video import VideoSubScene

def process_interaction(scene: "VideoSubScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "skip_video":
            scene.video_player.pause()
            scene.video_player.delete()
            return "video_end"
        case "request_pause":
            def current_video_frame(_):
                frame = scene.video_player.texture
                if not frame:
                    return
                return generic_entities.image(
                    name="video_frame", 
                    image=frame, 
                    position=(0,0),
                    size=scene.save["settings"]["resolution"],
                    duration=-1,
                    interaction_name=None,
                    hud=False
                )
            scene.commit_entities_update_by_id([scene_types.EntityInitializerConfig(entity_generator=current_video_frame)])
            scene.video_player.pause()
            scene.pause()
        case "resume_game":
            scene.video_player.play()
        case "exit_to_menu":
            return "exit_to_menu"

def process_release_interaction(scene: "VideoSubScene", logic_data: dict):
    pass

def process_natural(scene: "VideoSubScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"
        case "video_end":
            scene.video_player.delete()
            return "video_end"