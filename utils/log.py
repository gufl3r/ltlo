import json
import datetime
import os
import traceback
import utils.path
import utils.registry.gameinfo as game_info


def write_log(
    *,
    severity: str,
    message: str,
    errors: list | None = None,
    save_snapshot: dict | None = None,
    exception: Exception | None = None
) -> None:
    log_dir = utils.path.runtime_root("logs")
    os.makedirs(log_dir, exist_ok=True)

    # hora local convertida corretamente para UTC
    now_utc = datetime.datetime.now().astimezone(datetime.timezone.utc)

    # timestamp compacto, ordenável e estável
    timestamp_compact = now_utc.strftime("%Y%m%d%H%M%S")

    filename = f"{log_dir}/save_{severity}_{timestamp_compact}.json"

    payload = {
        "timestamp_utc": timestamp_compact,
        "timestamp_iso": now_utc.isoformat(),
        "severity": severity,
        "message": message,
        "game_version": game_info.GAME_VERSION,
        "errors": errors or [],
    }

    if save_snapshot is not None:
        payload["save_snapshot"] = save_snapshot

    if exception is not None:
        payload["exception"] = {
            "type": type(exception).__name__,
            "message": str(exception),
            "traceback": traceback.format_exc(),
        }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)