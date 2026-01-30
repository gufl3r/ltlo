import typing
import utils.save

import game.features.menus.settings.audio as audio_feature
import game.features.menus.settings.fullscreen as fullscreen_feature
import game.features.menus.settings.resolution as resolution_feature

if typing.TYPE_CHECKING:
    from game.scenes.menus.settings import SettingsScene

def process_interaction(scene: "SettingsScene", logic_data: dict):
    match logic_data["interaction_name"]:
        case "back_to_menu":
            utils.save.save_settings(scene.save)
            utils.save.apply_settings(scene.save, scene.window)
            return "menu"

        case "toggle_fullscreen":
            fullscreen_feature.toggle_fullscreen(scene, logic_data)

        case "switch_resolution":
            resolution_feature.switch_resolution(scene, logic_data)

        case "numeric_stepper_change":
            audio_feature.numeric_stepper_change(scene, logic_data)

def process_natural(scene: "SettingsScene", logic: dict):
    match logic["name"]:
        case "exit":
            return "exit"