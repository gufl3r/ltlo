import typing

STAMINA_BASE_REGEN = 1/6000
STAMINA_DRAIN_MULTIPLIER = 1/600

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def generate_natural_logic(scene: "NightScene"):
    print(f"{abs(scene.player.stamina)=:.2f}")
    _tick_stamina(scene)

def _tick_stamina(scene: "NightScene"):
    if scene.player.stamina >= 1:
        return
    stamina_regen = STAMINA_BASE_REGEN
    if scene.player.foot_out:
        stamina_regen *= 4
    
    scene.player.stamina += stamina_regen

def cover_consequences(scene: "NightScene", logic_data: dict):
    if scene.player.stamina <= 0:
        return    
    covered_percent: float = logic_data["covered_percent"]
    scene.player.stamina -= covered_percent * STAMINA_DRAIN_MULTIPLIER

def toggle_foot(scene: "NightScene", logic_data: dict):
    scene.player.foot_out = not scene.player.foot_out