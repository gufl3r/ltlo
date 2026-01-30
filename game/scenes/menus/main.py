from pyglet.window import Window

import game.scenes.scene as base_scene

import game.systems.menus.main.init as init_system
import game.systems.menus.main.processlogic as process_logic_system

class MainMenuScene(base_scene.Scene):
    FPS = 30

    def __init__(self, window: Window, save: dict) -> None:
        super().__init__(window, save)
        self.assets: dict

        init_system.init_assets(self)
        init_system.init_entities(self)

    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)
