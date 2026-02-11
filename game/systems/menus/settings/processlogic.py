import typing
import utils.save

import game.features.menus.settings.audio as audio_feature
import game.features.menus.settings.fullscreen as fullscreen_feature
import game.features.menus.settings.resolution as resolution_feature
import game.systems.global_.popup as popup_feature
import game.entitymodels.dialog as dialog_entities
import game.types.scenes as scene_types

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

def process_interaction(scene: "SettingsScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "back_to_menu":
            error = utils.save.apply_settings(scene.save, scene.window)
            if error:
                _, message = error
                scene.commit_entities_update_by_id(
                    [
                        scene_types.EntitiesListByIdConfig(
                            lambda _, e=entity: e
                        )
                        for entity in dialog_entities.info_box(
                            name="settings_error",
                            text=message,
                            screen_size=(scene.window.width, scene.window.height),

                            box_size=scene.relative_size(420, 180),
                            padding=scene.relative_axis_value(20, "y"),
                            text_size=scene.relative_axis_value(13, "y"),
                            button_text_size=scene.relative_axis_value(14, "y"),
                            button_size=scene.relative_size(80, 32),
                        )
                    ]
                )
                return
            utils.save.save_settings(scene.save)
            return "menu"

        case "toggle_fullscreen":
            fullscreen_feature.toggle_fullscreen(scene, logic_data)

        case "switch_resolution":
            resolution_feature.switch_resolution(scene, logic_data)

        case "numeric_stepper_change":
            audio_feature.numeric_stepper_change(scene, logic_data)

        case "info_box_ok":
            popup_feature.info_box_ok(scene, logic_data)

def process_natural(scene: "SettingsScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"