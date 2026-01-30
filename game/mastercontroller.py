import game.scenes.menucontroller as menu_controller
import game.scenes.ingamecontroller as ingame_controller
from pyglet.window import Window

class MasterController:
    def __init__(self, save: dict, window: Window) -> None:
        self.scene_name = "menu"
        self.scene_obj = None
        self.save = save
        self.window = window

    def loop(self) -> None:
        while True:
            print(f"at controller: {self.__class__.__name__}")
            match self.scene_name:
                case "menu":
                    self.scene_obj = menu_controller.MenuController("main_menu_scene", self.window, self.save)
                case "ingame":
                    self.scene_obj = ingame_controller.IngameController(self.window, self.save)
                case "exit":
                    break
                case _:
                    raise ValueError(f"Unknown scene: {self.scene_name}")
            self.scene_name = self.scene_obj.loop()