from pyglet.window import Window
import game.scenes.scene as base_scene

class CreditsScene(base_scene.Scene):
    FPS = 30

    def __init__(self, window: Window, save: dict) -> None:
        super().__init__(window, save)