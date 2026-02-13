import game.systems.default.video.video.init as init_system
import game.systems.default.video.video.processlogic as process_logic_system
import pyglet

import game.subscenes.subscene as base_subscene

class VideoSubScene(base_subscene.SubScene):
    def __init__(self, window: base_subscene.Window, save: dict, data: dict) -> None:
        super().__init__(window, save, data)

        self.video_player: pyglet.media.Player

        init_system.init_entities(self)
        init_system.init_vars(self)
        init_system.init_media(self)

    def _draw(self) -> None:
        self.window.clear()

        if not self.video_player.source:
            return
        texture = self.video_player.texture
        if texture:
            texture.blit(0, 0, width=self.window.width, height=self.window.height)

        self.window.flip()

    def generate_natural_logic(self) -> None:
        if not self.video_player.source:
            return
        if self.video_player.time > self.video_player.source.duration:
            self._logic_queue.append({"name": "video_end"})

    def after_audio(self, player) -> None:
        super().after_audio(player)

    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_release_interaction(self, logic_data):
        return process_logic_system.process_release_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)