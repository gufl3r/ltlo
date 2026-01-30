import pyglet
import utils.conversions
from pyglet.window import Window
import utils.path
import json

with open(utils.path.resource_path("config.json"), "r") as f:
    BASE_RESOLUTION = json.load(f)["base_resolution"]

def show(window: Window):
    window.clear()
    pyglet.text.Label(
        text="LOADING",
        x=window.width//2,
        y=window.height//2,
        anchor_x="center",
        anchor_y="center",
        font_size=utils.conversions.convert_size((0, 30), tuple(BASE_RESOLUTION), (window.width, window.height))[1]
    ).draw()
    window.flip()