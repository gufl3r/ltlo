import engine.factories.generic as generic_entities
import engine.types.scene as scene_types

DOMAIN_PREFIX = "domain:"

def _normalize_list(list_: list | None) -> list:
    return list_ if list_ is not None else []

def numeric_stepper(
    name: str,
    value_text: str,
    position: tuple[int, int],
    size: tuple[int, int],
    background_color: tuple[int, int, int],
    text_color: tuple[int, int, int, int],
    text_size: float,
    duration: int,
    tags: list[str],
    hud: bool = True,
    states: list[scene_types.State] | None = None,
) -> list[scene_types.Entity]:

    states = _normalize_list(states)

    # -------- validação do domínio --------

    domain_tags = [t for t in tags if t.startswith(DOMAIN_PREFIX)]

    if len(domain_tags) != 1:
        raise ValueError(
            f"numeric_stepper requires exactly ONE '{DOMAIN_PREFIX}<domain>' tag "
            f"(got {domain_tags})"
        )

    domain_tag = domain_tags[0]

    # -------- layout base --------

    x, y = position
    w, h = size

    button_w = h
    gap = max(int(h * 0.15), 2)
    min_value_w = int(h * 1.5)

    available = w - (button_w * 2) - (gap * 2)
    value_w = max(available, min_value_w)

    total_w = (button_w * 2) + value_w + (gap * 2)
    offset_x = x + (w - total_w) // 2

    # -------- decrease --------

    decrease_button_entities = generic_entities.button(
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
        states=states
    )

    # -------- value --------

    value_button_entities = generic_entities.button(
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
        states=states
    )

    # -------- increase --------

    increase_button_entities = generic_entities.button(
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
        states=states
    )

    # -------- retorno explícito --------

    return [
        *decrease_button_entities,
        *value_button_entities,
        *increase_button_entities,
    ]
