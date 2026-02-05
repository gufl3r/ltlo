import json
import utils.path

RESOLUTION_OPTIONS = []

_LOADED = False

def load(file_name: str = "gamecapacities.json") -> None:
    global RESOLUTION_OPTIONS, _LOADED

    if _LOADED:
        return

    path = utils.path.resource_path(file_name)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _validate(data)

    RESOLUTION_OPTIONS = data["settings"]["resolution_options"]

    _LOADED = True


def _validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("gameoptions.json must be an object")

    if "settings" not in data:
        raise ValueError("Missing 'settings' section")

    settings = data["settings"]

    if "resolution_options" not in settings:
        raise ValueError("Missing settings.resolution_options")

    options = settings["resolution_options"]

    if not isinstance(options, list) or not options:
        raise ValueError("resolution_options must be a non-empty list")

    for i, opt in enumerate(options):
        if (
            not isinstance(opt, list)
            or len(opt) != 2
            or not all(isinstance(x, int) for x in opt)
        ):
            raise ValueError(
                f"resolution_options[{i}] must be [int, int]"
            )

