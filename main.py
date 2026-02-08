import utils.libs
utils.libs.load()
import utils.registry.registry as registry
registry.load()
import pyglet
import utils.save
import game.mastercontroller as master_controller
import utils.registry.gameinfo as game_info

def main() -> None:
    save = utils.save.init_save()
    window = pyglet.window.Window(caption=game_info.NAME_SLUG.upper(), style=pyglet.window.Window.WINDOW_STYLE_TRANSPARENT)
    pyglet.gl.glClearColor(0.0, 0.0, 0.0, 1.0)

    utils.save.apply_settings(save, window)
    master_controller.MasterController(save, window).loop()

if __name__ == "__main__":
    main()