import dataclasses
import typing
import engine.types.scene as scene_types

STAMINA_BASE_REGEN = 1/6000
STAMINA_DRAIN_MULTIPLIER = 1/600

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.night import NightScene

def generate_natural_logic(scene: "NightScene"):
    _tick_stamina(scene)
    _update_overlay(scene)

def _tick_stamina(scene: "NightScene"):
    if scene.player.stamina >= 1:
        return
    stamina_regen = STAMINA_BASE_REGEN
    if scene.player.foot_out:
        stamina_regen *= 4
    
    scene.player.stamina += stamina_regen

def _update_overlay(scene: "NightScene"):
    if scene.player.stamina >= 1 or scene.player.stamina <= 0:
        return
    def alpha_changed_black(entity: scene_types.Entity):
            drawable = entity.drawable
            drawable.color = (0,0,0,int(255*(1-scene.player.stamina)))
            return dataclasses.replace(
                entity,
                drawable=drawable
            )
    black_overlay_id: int = scene.cached_ids["black_overlay"]
    scene.commit_entities_update_by_id([
        scene_types.EntityInitializerConfig(
            self_id=black_overlay_id,
            relation="replace",
            entity_generator=alpha_changed_black,
        )
    ])

def cover_consequences(scene: "NightScene", logic_data: dict):
    if scene.player.stamina <= 0:
        return
    covered_percent: float = logic_data["covered_percent"]
    scene.player.stamina -= covered_percent * STAMINA_DRAIN_MULTIPLIER

def toggle_foot(scene: "NightScene", logic_data: dict):
    scene.player.foot_out = not scene.player.foot_out