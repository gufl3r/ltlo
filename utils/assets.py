import pyglet
import pathlib
import time

def asset_path_to_obj(images: list[str] = [], audios: list[str] = [], videos: list[str] = [], animations: list[str] = []):
    start_time = time.perf_counter()
    objs = {
        "images": {},
        "audios": {},
        "videos": {},
        "animations": {}
    }
    for image_path in images:
        image_name = pathlib.Path(image_path).stem
        if image_name in objs["images"]:
            raise ValueError(f"There can't be more than 1 image with the same name: '{image_name}'")
        objs["images"][image_name] = pyglet.image.load(image_path)
    for audio_path in audios:
        audio_name = pathlib.Path(audio_path).stem
        if audio_name in objs["audios"]:
            raise ValueError(f"There can't be more than 1 audio with the same name: '{audio_name}'")
        objs["audios"][audio_name] = pyglet.media.load(audio_path)
    for video_path in videos:
        video_name = pathlib.Path(video_path).stem
        if video_name in objs["videos"]:
            raise ValueError(f"There can't be more than 1 video with the same name: '{video_name}'")
        objs["videos"][video_name] = pyglet.media.load(video_path)
    for animation_path in animations:
        animation_name = pathlib.Path(animation_path).stem
        if animation_name in objs["animations"]:
            raise ValueError(f"There can't be more than 1 animation with the same name: '{animation_name}'")
        objs["animations"][animation_name] = pyglet.image.load_animation(animation_path)
    print(f"Assets loaded in {time.perf_counter()-start_time}")
    return objs