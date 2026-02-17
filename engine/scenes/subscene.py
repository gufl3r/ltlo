from pyglet.window import Window

import engine.scenes.scene as base_scene

class SubScene(base_scene.Scene):
    def __init__(self, window: Window, save: dict, data: dict) -> None:
        super().__init__(window, save)
        self.data: dict = data