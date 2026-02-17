import pyglet
import engine.factories.generic as generic_entities
import engine.types.scene as scene_types

def _normalize_list(list_: list | None) -> list:
    return list_ if list_ is not None else []

def info_box(
    name: str,
    text: str,
    screen_size: tuple[int, int],
    box_size: tuple[int, int],
    text_size: int,
    duration: int = -1,
    hud: bool = True,
    background_color: tuple[int, int, int] = (140, 200, 140),
    text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
    button_color: tuple[int, int, int] = (40, 120, 40),
    button_text_color: tuple[int, int, int, int] = (255, 255, 255, 255),
    overlay_color: tuple[int, int, int, int] = (0, 0, 0, 100),
    tags: list[str] | None = None,
    states: list[scene_types.State] | None = None,
) -> list[scene_types.Entity]:

    tags = _normalize_list(tags)
    states = _normalize_list(states)

    sw, sh = screen_size
    bw, bh = box_size

    x = (sw - bw) // 2
    y = (sh - bh) // 2

    base = min(bw, bh)
    padding = int(base * 0.08)
    radius = max(int(base * 0.1), 2)

    button_w = int(bw * 0.4)
    button_h = int(bh * 0.18)
    button_text_size = int(text_size * 0.85)

    # ---------- DRAWABLES ----------

    overlay_rect = pyglet.shapes.Rectangle(
        x=0,
        y=0,
        width=sw,
        height=sh,
        color=overlay_color,
    )

    background_rect = pyglet.shapes.RoundedRectangle(
        x=x,
        y=y,
        width=bw,
        height=bh,
        color=background_color,
        radius=radius,
    )

    text_label = pyglet.text.Label(
        text=text,
        x=x + bw // 2,
        y=y + bh - padding,
        width=bw - padding * 2,
        multiline=True,
        anchor_x="center",
        anchor_y="top",
        color=text_color,
        font_size=text_size,
    )

    # ---------- ENTITIES ----------

    overlay_entity = scene_types.Entity(
        drawable=overlay_rect,
        name=name,
        ticks_left=duration,
        interaction_name="block",
        hud=hud,
        tags=tags + ["info_box", "info_box_overlay"],
        states=states
    )

    background_entity = scene_types.Entity(
        drawable=background_rect,
        name=name,
        ticks_left=duration,
        interaction_name=None,
        hud=hud,
        tags=tags + ["info_box", "info_box_background"],
        states=states
    )

    text_entity = scene_types.Entity(
        drawable=text_label,
        name=name,
        ticks_left=duration,
        interaction_name=None,
        hud=hud,
        tags=tags + ["info_box", "info_box_text"],
        states=states
    )

    button_entities = generic_entities.button(
        name=name,
        text="OK",
        position=(x + (bw - button_w) // 2, y + padding),
        size=(button_w, button_h),
        background_color=button_color,
        text_color=button_text_color,
        text_size=button_text_size,
        duration=duration,
        interaction_name="info_box_ok",
        hud=hud,
        tags=tags + ["info_box", "info_box_ok_button"],
        states=states
    )

    # ---------- RETURN EXPLÍCITO ----------

    return [
        overlay_entity,
        background_entity,
        text_entity,
        *button_entities
    ]
