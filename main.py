import utils.libs
utils.libs.load()
import utils.registry.registry as registry
registry.load()
import pyglet
import utils.save
import game.mastercontroller as master_controller
import utils.registry.gameinfo as game_info
import utils.log
import copy
import utils.registry.gamecapacities as game_capacities

def main() -> None:
    save = utils.save.init_save()
    window = pyglet.window.Window(caption=game_info.NAME_SLUG.upper())

    pre_apply_snapshot = copy.deepcopy(save)

    error = utils.save.apply_settings(save, window)

    if error:
        utils.log.write_log(
            severity="warning",
            message="Invalid screen mode detected on boot. Settings were restored silently.",
            errors=[error[0]],
            save_snapshot=pre_apply_snapshot
        )
        save["settings"]["resolution"] = game_capacities.RESOLUTION_OPTIONS[0]
        save["settings"]["fullscreen"] = False
        utils.save.save_settings(save)

    master_controller.MasterController(save, window).loop()

if __name__ == "__main__":
    main()