import engine.utils.libs
import engine.registry.registry
engine.utils.libs.load()
engine.registry.registry.load()
import pyglet
import shared.utils.save as saves_manager
import game.mastercontroller as master_controller
import engine.registry.gameinfo as game_info
import engine.utils.log
import copy
import engine.registry.gamecapacities as game_capacities

def main() -> None:
    save = saves_manager.init_save()
    window = pyglet.window.Window(caption=game_info.NAME_SLUG.upper())

    pre_apply_snapshot = copy.deepcopy(save)

    error = saves_manager.apply_settings(save, window)

    if error:
        engine.utils.log.write_log(
            severity="warning",
            message="Invalid screen mode detected on boot. Settings were restored silently.",
            errors=[error[0]],
            save_snapshot=pre_apply_snapshot
        )
        save["settings"]["resolution"] = game_capacities.RESOLUTION_OPTIONS[0]
        save["settings"]["fullscreen"] = False
        saves_manager.save_settings(save)

    master_controller.MasterController(save, window).loop()

if __name__ == "__main__":
    main()