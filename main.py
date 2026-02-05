import utils.libs
utils.libs.load()
import pyglet
import utils.save
import game.mastercontroller as master_controller
import utils.registry.registry as registry
import utils.registry.gameinfo as version_info

def main() -> None:
    registry.load()

    save = utils.save.init_save()
    window = pyglet.window.Window(caption=version_info.NAME_SLUG.upper())

    utils.save.apply_settings(save, window)
    master_controller.MasterController(save, window).loop()

if __name__ == "__main__":
    main()