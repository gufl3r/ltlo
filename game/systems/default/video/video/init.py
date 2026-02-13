import pyglet
from pyglet.window import key
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import typing

if typing.TYPE_CHECKING:
    from game.subscenes.default.video import VideoSubScene

def init_entities(scene: "VideoSubScene"):
    skip_video_listener = generic_entities.keyboard_listener(
        "enter_listener",
        key.ENTER,
        "skip_video",
        -1
    )

    scene.commit_entities_update_by_id(
        [scene_types.EntitiesListByIdConfig(
            anchor_id=None,
            self_id=None,
            relation=None,
            entity_generator=lambda _, e=skip_video_listener: e
        )]
    )

def init_vars(scene: "VideoSubScene"):
    scene.video_player = pyglet.media.Player()
    audio_settings = scene.save["settings"]["audio"]
    scene.video_player.volume = audio_settings["cutscene"] * audio_settings["master"]

def init_media(scene: "VideoSubScene"):
    scene.video_player.queue(scene.data["video_asset"])
    scene.video_player.play()
    scene.video_player.seek(0)