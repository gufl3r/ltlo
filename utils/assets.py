import pyglet
import pathlib
import time
import utils.path

def asset_path_to_obj(
    images: list[str] | None = None,
    audios: list[str] | None = None,
    videos: list[str] | None = None,
    animations: list[str] | None = None
):
    start_time = time.perf_counter()

    objs = {
        "images": {},
        "audios": {},
        "videos": {},
        "animations": {}
    }

    def resolve_path(raw_path: str) -> pathlib.Path:
        path_obj = pathlib.Path(raw_path)
        if not path_obj.is_absolute():
            path_obj = pathlib.Path(utils.path.resource_path(raw_path))
        if not path_obj.is_file():
            raise ValueError(f"Asset has to be a file: '{path_obj.stem}'")
        return path_obj

    if images:
        for image_path in images:
            path_obj = resolve_path(image_path)
            name = path_obj.stem
            if name in objs["images"]:
                raise ValueError(f"There can't be more than 1 image with the same name: '{name}'")
            objs["images"][name] = pyglet.image.load(str(path_obj))

    if audios:
        for audio_path in audios:
            path_obj = resolve_path(audio_path)
            name = path_obj.stem
            if name in objs["audios"]:
                raise ValueError(f"There can't be more than 1 audio with the same name: '{name}'")
            objs["audios"][name] = pyglet.media.load(str(path_obj))

    if videos:
        for video_path in videos:
            path_obj = resolve_path(video_path)
            name = path_obj.stem
            if name in objs["videos"]:
                raise ValueError(f"There can't be more than 1 video with the same name: '{name}'")
            objs["videos"][name] = pyglet.media.load(str(path_obj))

    if animations:
        for animation_path in animations:
            path_obj = resolve_path(animation_path)
            name = path_obj.stem
            if name in objs["animations"]:
                raise ValueError(f"There can't be more than 1 animation with the same name: '{name}'")
            objs["animations"][name] = pyglet.image.load_animation(str(path_obj))

    print(f"Assets loaded in {time.perf_counter() - start_time}")
    return objs