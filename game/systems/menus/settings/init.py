import utils.path
import utils.assets
import typing
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import pyglet
import game.entitymodels.menu as menu_entities

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

def init_assets(scene: "SettingsScene"):
    scene.assets = utils.assets.asset_path_to_obj(
        images=[
            utils.path.resource_path("assets/menus/main/bg.png")
        ]
    )

def init_entities(scene: "SettingsScene", save: dict):
    # ---------- BASE METRICS ----------
    button_size = scene.relative_size(200, 80)
    audio_button_size = scene.relative_size(40, 40)

    center_x = scene.window.width // 2
    center_y = scene.window.height // 2

    # columns
    column_offset = int(scene.window.width * 0.18)

    audio_width = audio_button_size[0] * 2.5
    audio_x = center_x - column_offset - audio_width // 2
    video_x = center_x + column_offset - button_size[0] // 2

    # audio layout
    audio_top_y = int(scene.window.height * 0.62)
    audio_spacing = audio_button_size[1] * 1.7
    label_offset_y = audio_button_size[1] * 0.95
    label_font_size = audio_button_size[1] * 0.32

    # video layout
    video_spacing = button_size[1] * 1.25
    video_top_y = center_y + video_spacing * 0.5

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

    # ---------- MAIN BUTTONS ----------
    back_to_menu_button = generic_entities.button(
        "back_to_menu_button",
        text="APPLY & BACK TO MENU",
        position=(
            center_x - button_size[0] // 2,
            center_y - button_size[1] * 3
        ),
        size=button_size,
        background_color=(0, 150, 200),
        text_color=(0, 0, 0, 255),
        text_size=button_size[1] * 0.15,
        duration=-1,
        interaction_name="back_to_menu"
    )

    fullscreen_toggle_button = generic_entities.button(
        "fullscreen_toggle_button",
        text="FULLSCREEN",
        position=(video_x, video_top_y),
        size=button_size,
        background_color=(0, 255, 0) if save["settings"]["fullscreen"] else (255, 0, 0),
        text_color=(0, 0, 0, 255),
        text_size=button_size[1] * 0.14,
        duration=-1,
        interaction_name="toggle_fullscreen"
    )

    change_resolution_button = generic_entities.button(
        "resolution_switch_button",
        text=f"{save['settings']['resolution'][0]}x{save['settings']['resolution'][1]}",
        position=(video_x, video_top_y - video_spacing),
        size=button_size,
        background_color=(0, 150, 200),
        text_color=(0, 0, 0, 255),
        text_size=button_size[1] * 0.14,
        duration=-1,
        interaction_name="switch_resolution"
    )

    # ---------- AUDIO HELPERS ----------
    def audio_row(name, label, value, index):
        y = audio_top_y - index * audio_spacing

        stepper = menu_entities.numeric_stepper(
            name=name,
            value_text=f"{int(value * 100)}%",
            position=(audio_x, y),
            size=(audio_width, audio_button_size[1]),
            background_color=(0, 150, 200),
            text_color=(0, 0, 0, 255),
            text_size=audio_button_size[1] * 0.42,  # porcentagem ajustada
            duration=-1,
            hud=True,
            tags=[f"domain:{name.split("_")[0]}"]
        )

        label_entity = scene_types.Entity(
            pyglet.text.Label(
                label,
                x=audio_x + audio_width // 2,
                y=y + label_offset_y,
                anchor_x="center",
                anchor_y="bottom",
                font_size=label_font_size,
                color=(255, 255, 255, 200)
            ),
            f"{name}_label",
            -1,
            None,
            True
        )

        return label_entity, stepper

    master_label, master_stepper = audio_row(
        "master_audio",
        "MASTER VOLUME",
        save["settings"]["audio"]["master"],
        0
    )

    music_label, music_stepper = audio_row(
        "music_audio",
        "MUSIC / AMBIENCE",
        save["settings"]["audio"]["music"],
        1
    )

    sfx_label, sfx_stepper = audio_row(
        "sfx_audio",
        "SFX",
        save["settings"]["audio"]["sfx"],
        2
    )

    cutscene_label, cutscene_stepper = audio_row(
        "cutscene_audio",
        "CUTSCENE",
        save["settings"]["audio"]["cutscene"],
        3
    )

    # ---------- ENTITY COMMIT ----------
    initial_entities = [
        scene_bg,
        *back_to_menu_button,
        *fullscreen_toggle_button,
        *change_resolution_button,

        master_label, *master_stepper,
        music_label, *music_stepper,
        sfx_label, *sfx_stepper,
        cutscene_label, *cutscene_stepper
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