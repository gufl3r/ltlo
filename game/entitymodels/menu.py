import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types

import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types

DOMAIN_PREFIX = "domain:"

def _normalize_list(list_: list | None) -> list:
    return list_ if list_ is not None else []

def numeric_stepper(
    name: str,
    value_text: str,
    position: tuple,
    size: tuple,
    background_color: tuple,
    text_color: tuple,
    text_size: float,
    duration: int,
    tags: list[str],
    hud: bool = True,
    gap: int = 6,
    states: list[scene_types.State] | None = None
) -> list[scene_types.Entity]:

    # -------- validação do domínio --------

    domain_tags = [t for t in tags if t.startswith(DOMAIN_PREFIX)]

    if len(domain_tags) != 1:
        raise ValueError(
            f"numeric_stepper requires exactly ONE '{DOMAIN_PREFIX}<domain>' tag "
            f"(got {domain_tags})"
        )

    domain_tag = domain_tags[0]

    # -------- layout --------
    x, y = position
    w, h = size

    button_w = h
    min_value_w = int(h * 1.5)

    available = w - (button_w * 2) - (gap * 2)
    value_w = max(available, min_value_w)

    total_w = (button_w * 2) + value_w + (gap * 2)
    offset_x = x + (w - total_w) // 2

    entities: list[scene_types.Entity] = []

    # -------- botão - --------
    entities += generic_entities.button(
        name=name,
        text="-",
        position=(offset_x, y),
        size=(button_w, h),
        background_color=background_color,
        text_color=text_color,
        text_size=text_size,
        duration=duration,
        interaction_name="numeric_stepper_change",
        hud=hud,
        tags=[
            domain_tag,
            "numeric_stepper",
            "decrease",
        ],
    )

    entities += generic_entities.button(
        name=name,
        text=value_text,
        position=(offset_x + button_w + gap, y),
        size=(value_w, h),
        background_color=background_color,
        text_color=text_color,
        text_size=text_size,
        duration=duration,
        interaction_name=None,
        hud=hud,
        tags=[
            domain_tag,
            "numeric_stepper",
        ],
    )

    entities += generic_entities.button(
        name=name,
        text="+",
        position=(offset_x + button_w + gap + value_w + gap, y),
        size=(button_w, h),
        background_color=background_color,
        text_color=text_color,
        text_size=text_size,
        duration=duration,
        interaction_name="numeric_stepper_change",
        hud=hud,
        tags=[
            domain_tag,
            "numeric_stepper",
            "increase",
        ],
    )

    return entities
