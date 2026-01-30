import game.scenes.menus.main as main_scene
import game.scenes.menus.settings as settings_scene
import game.scenes.menus.credits as credits_scene
import game.features.global_.loading as loading_feature
from pyglet.window import Window

class MenuController:
    def __init__(self, scene_name: str, window: Window, save: dict) -> None:
        self.scene_name = scene_name
        self.scene_obj = None
        self.window = window
        self.save = save

    def loop(self) -> str:
        while True:
            print(f"at controller: {self.__class__.__name__}")
            loading_feature.show(self.window)
            match self.scene_name:
                case "main_menu_scene":
                    self.scene_obj = main_scene.MainMenuScene(self.window, self.save)
                case "settings_scene":
                    self.scene_obj = settings_scene.SettingsScene(self.window, self.save)
                case "credits_scene":
                    self.scene_obj = credits_scene.CreditsScene(self.window, self.save)
                case _:
                    return self.scene_name
            self.scene_name = self.scene_obj.loop()