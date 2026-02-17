import typing
import pyglet
import engine.factories.generic as generic_entities
import engine.types.scene as scene_types

if typing.TYPE_CHECKING:
    from engine.scenes.engine.default.subscenes.pause import PauseSubScene


def init_entities(scene: "PauseSubScene"):

    resume_game_listener = generic_entities.keyboard_listener(
        "esc_listener",
        pyglet.window.key.ESCAPE,
        "resume_game",
        -1
    )

    sw, sh = scene.save["settings"]["resolution"]

    # Caixa levemente maior para respirar melhor
    box_w, box_h = scene.relative_size(380, 280)

    x = (sw - box_w) // 2
    y = (sh - box_h) // 2

    base = min(box_w, box_h)

    # Sistema proporcional igual ao info_box
    padding = int(base * 0.08)
    radius = max(int(base * 0.1), 2)

    button_w = box_w - padding * 2
    button_h = int(base * 0.18)
    spacing = int(base * 0.12)

    title_font_size = int(base * 0.14)
    button_text_size = int(base * 0.09)

    overlay_color = (0, 0, 0, 100)
    container_color = (140, 200, 140)
    btn_resume_color = (40, 120, 40)
    btn_exit_color = (160, 60, 60)

    # ---------- OVERLAY ----------
    overlay = scene_types.Entity(
        drawable=pyglet.shapes.Rectangle(
            x=0, y=0,
            width=sw, height=sh,
            color=overlay_color
        ),
        name="pause_overlay",
        ticks_left=-1,
        interaction_name="block",
        hud=True,
    )

    # ---------- BACKGROUND ----------
    container_bg = scene_types.Entity(
        drawable=pyglet.shapes.RoundedRectangle(
            x=x, y=y,
            width=box_w,
            height=box_h,
            color=container_color,
            radius=radius
        ),
        name="pause_container_bg",
        ticks_left=-1,
        interaction_name=None,
        hud=True,
    )

    # ---------- TÍTULO ----------
    title_y = y + box_h - padding

    title = scene_types.Entity(
        drawable=pyglet.text.Label(
            text="PAUSED",
            x=x + box_w // 2,
            y=title_y,
            anchor_x="center",
            anchor_y="top",
            font_size=title_font_size,
            color=(0, 0, 0, 255),
        ),
        name="pause_title",
        ticks_left=-1,
        interaction_name=None,
        hud=True,
    )

    # ---------- BOTÕES ----------
    buttons_data = [
        ("RESUME", "resume_game", btn_resume_color),
        ("EXIT TO MENU", "exit_to_menu", btn_exit_color),
    ]

    total_buttons_height = (
        button_h * len(buttons_data)
        + spacing * (len(buttons_data) - 1)
    )

    # === ÁREA RESERVADA PARA TÍTULO ===
    title_area_height = title_font_size + padding
    content_top = y + box_h - padding - title_area_height
    content_bottom = y + padding

    available_height = content_top - content_bottom

    start_y = content_bottom + (available_height - total_buttons_height) // 2

    btn_x = x + padding

    buttons_entities = []

    for i, (text, interaction, color) in enumerate(buttons_data):
        btn_y = start_y + i * (button_h + spacing)

        buttons_entities += generic_entities.button(
            name=f"pause_button_{interaction}",
            text=text,
            position=(btn_x, btn_y),
            size=(button_w, button_h),
            background_color=color,
            text_color=(255, 255, 255, 255),
            text_size=button_text_size,
            duration=-1,
            interaction_name=interaction,
            hud=True,
        )

    entities_to_add = [
        resume_game_listener,
        overlay,
        container_bg,
        title,
        *buttons_entities
    ]

    scene.commit_entities_update_by_id([
        scene_types.EntitiesListByIdConfig(
            relation=None,
            entity_generator=lambda _, e=e: e
        )
        for e in entities_to_add
    ])
