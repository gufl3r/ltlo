import json
import utils.path
import sys
import utils.registry.runtimeconfigextension.build as build

BASE_RESOLUTION = []
UI_OFFSETS = {}

_LOADED = False

def load(file_name="runtimeconfig.json"):
    global BASE_RESOLUTION, UI_OFFSETS, _LOADED

    if _LOADED:
        return

    with open(utils.path.resource_path(file_name), "r") as f:
        current_cfg = json.load(f)
    _validate(current_cfg)
    if not getattr(sys, "frozen", False): # dev
        cfg = build.build(current_cfg)
        _validate(cfg)
        with open(utils.path.resource_path(file_name), "w") as f:
            json.dump(cfg, f)
    else:
        cfg = current_cfg

    BASE_RESOLUTION = tuple(cfg["render"]["base_resolution"])
    UI_OFFSETS = cfg.get("ui", {}).get("offsets", {})

    _LOADED = True

def _validate(cfg: dict):
    # --- render ---
    if "render" not in cfg:
        raise ValueError("runtime_config: missing 'render'")

    if "base_resolution" not in cfg["render"]:
        raise ValueError("runtime_config: missing render.base_resolution")

    br = cfg["render"]["base_resolution"]
    if not (
        isinstance(br, list)
        and len(br) == 2
        and all(isinstance(x, int) for x in br)
    ):
        raise ValueError("render.base_resolution must be [int, int]")

    # --- ui offsets ---
    if "ui" in cfg and "offsets" in cfg["ui"]:
        offsets = cfg["ui"]["offsets"]

        if not isinstance(offsets, dict):
            raise ValueError("ui.offsets must be a dict")

        _validate_offsets(offsets)
        
def _validate_offsets(node, path="ui.offsets"):
    if isinstance(node, dict):
        for key, value in node.items():
            _validate_offsets(value, f"{path}.{key}")
    else:
        if not isinstance(node, int):
            raise ValueError(
                f"{path} must contain only integers, got {type(node).__name__}"
            )
