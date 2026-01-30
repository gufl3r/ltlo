from pyglet.window import Window

import game.scenes.scene as base_scene

import game.systems.menus.settings.init as init_system
import game.systems.menus.settings.processlogic as process_logic_system
import game.helpers.numericstepper as numeric_stepper_helper
import game.helpers.button as button_helper
import game.types.scenes as scene_types

class SettingsScene(base_scene.Scene):
    FPS = 30

    def __init__(self, window: Window, save: dict) -> None:
        super().__init__(window, save)
        self.assets: dict

        init_system.init_assets(self)
        init_system.init_entities(self, save)

    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)
    
    def resolve_pending_relations(self, i:int, entity: scene_types.Entity):
        relations = []
        relations += numeric_stepper_helper.try_relate(self, i, entity)
        relations += button_helper.try_relate(self, i, entity)

        if relations:
            return relations
        return super().resolve_pending_relations(i, entity)