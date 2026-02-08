import utils.path
import utils.assets
import typing
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import pyglet
import json
import utils.registry.gameinfo as game_info

if typing.TYPE_CHECKING:
    from game.scenes.menus.main import MainMenuScene

def init_assets(scene: "MainMenuScene"):
    scene.assets = utils.assets.asset_path_to_obj(
        images=[
            "assets/menus/main/bg.png"
        ]
    )

def init_entities(scene: "MainMenuScene"):
    button_size = scene.relative_size(200, 80)

    center_x = scene.window.width // 2
    center_y = scene.window.height // 2

    button_spacing = button_size[1] * 1.4
    top_button_y = center_y - button_spacing * 0.2

    version_font_size = scene.relative_size(0, 12)[1]

    # ---------- BACKGROUND ----------
    scene_bg = generic_entities.image(
        "scene_bg",
        scene.assets["images"]["bg"],
        (0, 0),
        (scene.window.width, scene.window.height),
        -1,
        None,
        True
    )

    # ---------- VERSION LABEL ----------
    version_label = scene_types.Entity(
        pyglet.text.Label(
            game_info.GAME_VERSION,
            x=scene.window.width - 12,
            y=12,
            anchor_x="right",
            anchor_y="bottom",
            font_size=version_font_size,
            color=(255, 255, 255, 30)
        ),
        "version_label",
        -1,
        None,
        True
    )

    # ---------- BUTTONS ----------
    start_button = generic_entities.button(
        "start_button",
        text="START GAME",
        position=(
            center_x - button_size[0] // 2,
            top_button_y
        ),
        size=button_size,
        background_color=(0, 150, 200),
        text_color=(0, 0, 0, 255),
        text_size=button_size[1] * 0.16,
        duration=-1,
        interaction_name="start_game"
    )

    settings_button = generic_entities.button(
        "settings_button",
        text="SETTINGS",
        position=(
            center_x - button_size[0] // 2,
            top_button_y - button_spacing
        ),
        size=button_size,
        background_color=(0, 150, 200),
        text_color=(0, 0, 0, 255),
        text_size=button_size[1] * 0.15,
        duration=-1,
        interaction_name="open_settings"
    )

    # ---------- ENTITY COMMIT ----------
    initial_entities = [
        scene_bg,
        version_label,
        *start_button,
        *settings_button
    ]

    scene.commit_entities_update_by_id(
        [
            scene_types.EntitiesListByIdConfig(
                relation=None,
                entity_generator=lambda _old, e=e: e
            )
            for e in initial_entities
        ]
    )