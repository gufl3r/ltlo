import pyglet
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types


def info_box(
    name: str,
    text: str,
    screen_size: tuple[int, int],

    # ---- valores RELATIVOS (obrigatórios) ----
    box_size: tuple[int, int],
    padding: int,
    text_size: int,
    button_text_size: int,
    button_size: tuple[int, int],

    # ---- comportamento ----
    duration: int = -1,
    hud: bool = True,

    # ---- estilo (identidade padrão) ----
    background_color: tuple[int, int, int] = (140, 200, 140),      # verde claro
    text_color: tuple[int, int, int, int] = (0, 0, 0, 255),        # preto
    button_color: tuple[int, int, int] = (40, 120, 40),            # verde escuro
    button_text_color: tuple[int, int, int, int] = (255, 255, 255, 255),
    overlay_color: tuple[int, int, int, int] = (0, 0, 0, 100),     # overlay translúcido
    tags: list[str] | None = None,
) -> list[scene_types.Entity]:

    tags = tags or []

    sw, sh = screen_size
    bw, bh = box_size
    button_w, button_h = button_size

    x = (sw - bw) // 2
    y = (sh - bh) // 2

    radius = max(min(bw, bh) * 0.1, 2)

    entities: list[scene_types.Entity] = []

    # -------- overlay modal (bloqueia clique) --------
    overlay = pyglet.shapes.Rectangle(
        x=0,
        y=0,
        width=sw,
        height=sh,
        color=overlay_color,
    )

    entities += [
        scene_types.Entity(
            drawable=overlay,
            name=name,
            ticks_left=duration,
            interaction_name="block",
            hud=hud,
            tags=tags + ["info_box", "info_box_overlay"],
        )
    ]

    # -------- fundo da caixa --------
    box_rect = pyglet.shapes.RoundedRectangle(
        x=x,
        y=y,
        width=bw,
        height=bh,
        color=background_color,
        radius=radius,
    )

    entities += [
        scene_types.Entity(
            drawable=box_rect,
            name=name,
            ticks_left=duration,
            interaction_name=None,
            hud=hud,
            tags=tags + ["info_box", "info_box_background"],
        )
    ]

    # -------- texto --------
    label = pyglet.text.Label(
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

    entities += [
        scene_types.Entity(
            drawable=label,
            name=name,
            ticks_left=duration,
            interaction_name=None,
            hud=hud,
            tags=tags + ["info_box", "info_box_text"],
        )
    ]

    # -------- botão OK --------
    btn_x = x + (bw - button_w) // 2
    btn_y = y + padding

    entities += generic_entities.button(
        name=name,
        text="OK",
        position=(btn_x, btn_y),
        size=(button_w, button_h),
        background_color=button_color,
        text_color=button_text_color,
        text_size=button_text_size,
        duration=duration,
        interaction_name="info_box_ok",
        hud=hud,
        tags=tags + ["info_box", "info_box_ok_button"],
    )

    return entities
