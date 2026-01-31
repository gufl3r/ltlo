import json
import utils.path

AUTHOR: str = ""
NAME_SLUG: str = ""
GAME_VERSION: str = ""
VERSIONS_SUPPORTED: list[str] = []


class VersionInfoError(RuntimeError):
    pass


def _validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise VersionInfoError("versioninfo.json must be an object")

    required_keys = {
        "author": str,
        "name_slug": str,
        "version": str,
        "versions_supported": list,
    }

    for key, expected_type in required_keys.items():
        if key not in data:
            raise VersionInfoError(f"Missing key '{key}' in versioninfo.json")

        if not isinstance(data[key], expected_type):
            raise VersionInfoError(
                f"Key '{key}' must be {expected_type.__name__}"
            )

    if not data["versions_supported"]:
        raise VersionInfoError("versions_supported cannot be empty")

    if data["version"] not in data["versions_supported"]:
        raise VersionInfoError(
            "Current version must be listed in versions_supported"
        )

    for v in data["versions_supported"]:
        if not isinstance(v, str):
            raise VersionInfoError("versions_supported must contain only strings")


def load(file_name: str = "versioninfo.json") -> None:
    global AUTHOR, NAME_SLUG, GAME_VERSION, VERSIONS_SUPPORTED

    path = utils.path.resource_path(file_name)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _validate(data)

    AUTHOR = data["author"]
    NAME_SLUG = data["name_slug"]
    GAME_VERSION = data["version"]
    VERSIONS_SUPPORTED = list(data["versions_supported"])
