import typing
import game.scenes.ingames.night.subscenes.underbed as underbed_subscene

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.night import NightScene

def look_under_bed(scene: "NightScene", logic_data: dict):
    result = scene.loop_subscene(underbed_subscene.UnderBedSubscene, {})
    if result == "exit_to_menu":
        scene._logic_queue.append({"name": "interaction", "data": {"interaction_name": "exit_to_menu"}})