import pyglet
from pyglet.window import key
import engine.factories.generic as generic_entities
import engine.types.scene as scene_types
import typing

if typing.TYPE_CHECKING:
    from engine.scenes.engine.default.subscenes.video import VideoSubScene

def init_entities(scene: "VideoSubScene"):
    skip_video_listener = generic_entities.keyboard_listener(
        "enter_listener",
        key.ENTER,
        "skip_video",
        -1
    )

    skip_video_listener2 = generic_entities.keyboard_listener(
        "space_listener",
        key.SPACE,
        "skip_video",
        -1
    )

    entities_to_add = [
        skip_video_listener,
        skip_video_listener2
    ]

    scene.commit_entities_update_by_id([
        scene_types.EntityInitializerConfig(
            relation=None,
            entity_generator=lambda _, e=e: e
        )
        for e in entities_to_add
    ])

def init_vars(scene: "VideoSubScene"):
    scene.video_player = pyglet.media.Player()
    audio_settings = scene.save["settings"]["audio"]
    scene.video_player.volume = audio_settings["cutscene"] * audio_settings["master"]

def init_media(scene: "VideoSubScene"):
    scene.video_player.queue(scene.data["video_asset"])
    scene.video_player.play()
    scene.video_player.seek(0)