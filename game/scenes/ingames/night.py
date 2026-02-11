from pyglet.window import Window
import game.scenes.scene as base_scene
import game.types.ingames.night as night_types
import game.systems.ingames.night.init as init_system
import game.systems.ingames.night.processlogic as process_logic_system
import game.features.ingames.night.sight as sight_feature
import game.features.ingames.night.blanket as blanket_feature
import game.features.ingames.night.player as player_feature

class NightScene(base_scene.Scene):
    FPS = 60

    def __init__(self, window: Window, save: dict) -> None:
        super().__init__(window, save)
        self.assets: dict
        self.x: int
        self.player: night_types.Player

        init_system.init_assets(self)
        init_system.init_vars(self)
        init_system.init_entities(self)
        init_system.init_media(self)

    def generate_natural_logic(self) -> None:
        sight_feature.generate_natural_logic(self)
        blanket_feature.generate_natural_logic(self)
        player_feature.generate_natural_logic(self)

    def after_video(self, player) -> None:
        super().after_video(player)
    
    def after_audio(self, player) -> None:
        super().after_audio(player)

    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_release_interaction(self, logic_data):
        return process_logic_system.process_release_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)