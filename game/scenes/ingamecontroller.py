import game.scenes.ingames.night as night_scene
import game.scenes.ingames.final as final_scene
import game.features.global_.loading as loading_feature
from pyglet.window import Window

class IngameController:
    def __init__(self, window: Window, save: dict) -> None:
        self.scene_name = "night_scene"
        self.scene_obj = None
        self.window = window
        self.save = save

    def loop(self) -> str:
        while True:
            print(f"at controller: {self.__class__.__name__}")
            loading_feature.show(self.window)
            match self.scene_name:
                case "night_scene":
                    self.scene_obj = night_scene.NightScene(self.window, self.save)
                case "final_scene":
                    self.scene_obj = final_scene.FinalScene(self.window, self.save)
                case _:
                    return self.scene_name
            self.scene_name = self.scene_obj.loop()