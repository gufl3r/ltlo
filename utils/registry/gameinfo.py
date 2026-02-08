import json
import utils.path

AUTHOR = ""
NAME_SLUG = ""
GAME_VERSION = ""
VERSIONS_SUPPORTED = []

_LOADED = False

def _validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise TypeError("gameinfo.json must be an object")

    required_keys = {
        "author": str,
        "name_slug": str,
        "version": str,
        "versions_supported": list,
    }

    for key, expected_type in required_keys.items():
        if key not in data:
            raise KeyError(f"Missing key '{key}' in gameinfo.json")

        if not isinstance(data[key], expected_type):
            raise TypeError(
                f"Key '{key}' must be {expected_type.__name__}"
            )

    if not data["versions_supported"]:
        raise ValueError("versions_supported cannot be empty")

    if data["version"] not in data["versions_supported"]:
        raise ValueError(
            "Current version must be listed in versions_supported"
        )

    for v in data["versions_supported"]:
        if not isinstance(v, str):
            raise TypeError("versions_supported must contain only strings")


def load(file_name: str = "gameinfo.json") -> None:
    global AUTHOR, NAME_SLUG, GAME_VERSION, VERSIONS_SUPPORTED, _LOADED

    if _LOADED:
        return

    path = utils.path.resource_path(file_name)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _validate(data)

    AUTHOR = data["author"]
    NAME_SLUG = data["name_slug"]
    GAME_VERSION = data["version"]
    VERSIONS_SUPPORTED = list(data["versions_supported"])

    _LOADED = True
