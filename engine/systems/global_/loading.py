import pyglet
import engine.utils.conversions
from pyglet.window import Window
import engine.registry.runtimeconfig as runtime_config

def show(window: Window):
    window.clear()

    pyglet.text.Label(
        text="LOADING",
        x=window.width//2,
        y=window.height//2,
        anchor_x="center",
        anchor_y="center",
        font_size=engine.utils.conversions.convert_size((0, 30), tuple(runtime_config.BASE_RESOLUTION), (window.width, window.height))[1]
    ).draw()
    
    window.flip()