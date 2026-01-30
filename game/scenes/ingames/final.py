from pyglet.window import Window
import game.scenes.scene as base_scene


class FinalScene(base_scene.Scene):
    FPS = 60

    def __init__(self, window: Window, save: dict) -> None:
        super().__init__(window, save)