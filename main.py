import utils.libs
utils.libs.load()
import pyglet
import utils.save
import game.mastercontroller as master_controller

def main() -> None:
    save = utils.save.init_save()
    window = pyglet.window.Window(caption="LTLO")

    utils.save.apply_settings(save, window)
    master_controller.MasterController(save, window).loop()

if __name__ == "__main__":
    main()