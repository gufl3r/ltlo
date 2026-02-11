import json
import os
import pyglet
from pyglet.window import Window
import userpaths

import utils.log
import utils.registry.gamecapacities as game_capacities
import utils.registry.gameinfo as game_info

SAVE_FOLDER_PATH = f"{userpaths.get_my_documents()}/{game_info.AUTHOR}"
os.makedirs(SAVE_FOLDER_PATH, exist_ok=True)


# ---------- SAVE ----------

def init_save() -> dict:
    try:
        with open(f"{SAVE_FOLDER_PATH}/{game_info.NAME_SLUG}_save.json", "r", encoding="utf-8") as f:
            save = json.load(f)

        errors = _validate(save)
        if errors:
            utils.log.write_log(
                severity="error",
                message="Invalid save file detected during load.",
                errors=errors,
                save_snapshot=save
            )
            raise ValueError("Save file is invalid.")

        return save

    except FileNotFoundError:
        default_save = {
            "version": game_info.GAME_VERSION,
            "game": {"night": 1},
            "settings": {
                "resolution": [1280, 720],
                "fullscreen": False,
                "audio": {
                    "master": 1.0,
                    "music": 1.0,
                    "sfx": 1.0,
                    "cutscene": 1.0
                }
            }
        }

        utils.log.write_log(
            severity="warning",
            message="Save file not found. Creating a new one.",
            save_snapshot=default_save
        )

        with open(f"{SAVE_FOLDER_PATH}/{game_info.NAME_SLUG}_save.json", "w", encoding="utf-8") as f:
            json.dump(default_save, f, indent=2)

        return default_save

    except json.JSONDecodeError as e:
        utils.log.write_log(
            severity="fatal",
            message="Save file is corrupted (invalid JSON).",
            exception=e
        )
        raise ValueError("Save file is corrupted, delete or fix save.json")


def save_settings(save: dict) -> None:
    errors = _validate(save)
    if errors:
        utils.log.write_log(
            severity="error",
            message="Attempted to save invalid save file.",
            errors=errors,
            save_snapshot=save
        )
        raise ValueError("Attempted to save an invalid save file.")

    with open(f"{SAVE_FOLDER_PATH}/{game_info.NAME_SLUG}_save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, indent=2)


def apply_settings(save: dict, window: Window) -> None | tuple[str, str]:
    settings = save["settings"]
    resolution = settings["resolution"]
    fullscreen = settings["fullscreen"]

    try:
        window.set_fullscreen(
            fullscreen=fullscreen,
            width=resolution[0],
            height=resolution[1]
        )
    except pyglet.window.NoSuchScreenModeException as e:
        return (
            str(e),
            "An error occurred while setting this screen mode:\n"
            f"'fullscreen {resolution[0]}x{resolution[1]}'\n\n"
            "Please check if your monitor supports it."
        )


# ---------- VALIDATION ----------

def _validate(save: dict) -> list[str]:
    errors: list[str] = []

    try:
        if not all(k in save for k in ("version", "game", "settings")):
            errors.append("Main structure missing 'version', 'game' or 'settings'.")

        if save.get("version") not in game_info.VERSIONS_SUPPORTED:
            errors.append("Save file version is not supported.")

        game = save.get("game")
        if not isinstance(game, dict):
            errors.append("'game' must be a dict.")
        else:
            night = game.get("night")
            if not isinstance(night, int):
                errors.append("'night' must be an int.")
            elif not (1 <= night <= 6):
                errors.append("'night' out of bounds (1-6).")

        settings = save.get("settings")
        if not isinstance(settings, dict):
            errors.append("'settings' must be a dict.")
        else:
            if settings.get("resolution") not in game_capacities.RESOLUTION_OPTIONS:
                errors.append("Invalid resolution option.")

            if not isinstance(settings.get("fullscreen"), bool):
                errors.append("'fullscreen' must be boolean.")

            audio = settings.get("audio")
            if not isinstance(audio, dict):
                errors.append("'audio' must be a dict.")
            else:
                for k in ("master", "music", "sfx", "cutscene"):
                    v = audio.get(k)
                    if not isinstance(v, (int, float)):
                        errors.append(f"Audio '{k}' must be int or float.")
                    elif not (0.0 <= v <= 1.0):
                        errors.append(f"Audio '{k}' out of bounds (0.0-1.0).")

        return errors

    except Exception as e:
        utils.log.write_log(
            severity="fatal",
            message="Exception during save validation.",
            exception=e,
            save_snapshot=save
        )
        return ["Unhandled exception during validation."]
