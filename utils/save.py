import json
import datetime
from pyglet.window import Window
import utils.path
import os
import traceback
import userpaths
import utils.registry.gamecapacities as game_capacities
import utils.registry.versioninfo as version_info

SAVE_FOLDER_PATH = f"{userpaths.get_my_documents()}/{version_info.AUTHOR}"
os.makedirs(SAVE_FOLDER_PATH, exist_ok=True)

# ---------- LOGGING ----------

def _write_log(
    *,
    severity: str,
    message: str,
    errors: list | None = None,
    save_snapshot: dict | None = None,
    exception: Exception | None = None
) -> None:
    log_dir = utils.path.runtime_root("logs")
    os.makedirs(log_dir, exist_ok=True)

    # hora local -> UTC corretamente
    now_utc = datetime.datetime.now().astimezone(datetime.timezone.utc)

    # timestamp compacto e ordenável
    timestamp_compact = now_utc.strftime("%Y%m%d%H%M%S")

    filename = f"{log_dir}/save_{severity}_{timestamp_compact}.json"

    log_payload = {
        # mantém os dois se quiser
        "timestamp_utc": timestamp_compact,
        "timestamp_iso": now_utc.isoformat(),
        "severity": severity,
        "message": message,
        "game_version": version_info.GAME_VERSION,
        "errors": errors or [],
    }

    if save_snapshot is not None:
        log_payload["save_snapshot"] = save_snapshot

    if exception is not None:
        log_payload["exception"] = {
            "type": type(exception).__name__,
            "message": str(exception),
            "traceback": traceback.format_exc()
        }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_payload, f, indent=2, ensure_ascii=False)

# ---------- SAVE ----------

def init_save() -> dict:
    try:
        with open(f"{SAVE_FOLDER_PATH}/{version_info.NAME_SLUG}_save.json", "r", encoding="utf-8") as f:
            save = json.load(f)

        errors = _validate(save)
        if errors:
            _write_log(
                severity="error",
                message="Invalid save file detected during load.",
                errors=errors,
                save_snapshot=save
            )
            raise ValueError("Save file is invalid.")

        return save

    except FileNotFoundError:
        default_save = {
            "version": version_info.GAME_VERSION,
            "game": {
                "night": 1
            },
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

        _write_log(
            severity="warning",
            message="Save file not found. Creating a new one.",
            save_snapshot=default_save
        )

        with open(f"{SAVE_FOLDER_PATH}/{version_info.NAME_SLUG}_save.json", "w", encoding="utf-8") as f:
            json.dump(default_save, f, indent=2)

        return default_save

    except json.JSONDecodeError as e:
        _write_log(
            severity="fatal",
            message="Save file is corrupted (invalid JSON).",
            exception=e
        )
        raise ValueError("Save file is corrupted, delete or fix save.json")


def save_settings(save: dict) -> None:
    errors = _validate(save)
    if errors:
        _write_log(
            severity="error",
            message="Attempted to save invalid save file.",
            errors=errors,
            save_snapshot=save
        )
        raise ValueError("Attempted to save an invalid save file.")
    
    with open(f"{SAVE_FOLDER_PATH}/{version_info.NAME_SLUG}_save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, indent=2)


def apply_settings(save: dict, window: Window) -> None:
    resolution = save["settings"]["resolution"]
    fullscreen = save["settings"]["fullscreen"]
    window.set_fullscreen(fullscreen, width=resolution[0], height=resolution[1])


# ---------- VALIDATION ----------

def _validate(save: dict) -> list[str]:
    errors = []

    try:
        # structure
        if not all(k in save for k in ("version", "game", "settings")):
            errors.append("Main structure missing 'version', 'game' or 'settings'.")

        if save.get("version") not in version_info.VERSIONS_SUPPORTED:
            errors.append("Save file version is not supported.")

        # game
        if not isinstance(save.get("game"), dict):
            errors.append("'game' must be a dict.")
        else:
            if not isinstance(save["game"].get("night"), int):
                errors.append("'night' must be an int.")
            elif not (1 <= save["game"]["night"] <= 6):
                errors.append("'night' out of bounds (1-6).")

        # settings
        settings = save.get("settings")
        if not isinstance(settings, dict):
            errors.append("'settings' must be a dict.")
        else:
            if settings.get("resolution") not in game_capacities.RESOLUTION_OPTIONS:
                errors.append(f"Invalid resolution. Must be one of {game_capacities.RESOLUTION_OPTIONS}.")

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
        _write_log(
            severity="fatal",
            message="Exception during save validation.",
            exception=e,
            save_snapshot=save
        )
        return ["Unhandled exception during validation."]
