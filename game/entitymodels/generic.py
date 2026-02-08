import pyglet as pyglet
import game.types.scenes as scene_types


def _normalize_list(list_: list | None) -> list:
    return list_ if list_ is not None else []


def button(
    name: str,
    text: str,
    position: tuple,
    size: tuple,
    background_color: tuple,
    text_color: tuple,
    text_size: float,
    duration: int,
    interaction_name: str | None,
    hud: bool = True,
    text_offset: tuple = (0, 0),
    tags: list[str] | None = None,
    states: list[scene_types.State] | None = None
) -> list[scene_types.Entity]:

    tags = _normalize_list(tags)
    states = _normalize_list(states)

    x, y = position
    w, h = size

    cx = x + w // 2 + text_offset[0]
    cy = y + h // 2 + text_offset[1]

    bordered_rectangle = pyglet.shapes.RoundedRectangle(
        x=x,
        y=y,
        width=w,
        height=h,
        color=background_color,
        radius=max(min(w, h) * 0.1, 2)
    )

    label = pyglet.text.Label(
        text=text,
        x=cx,
        y=cy,
        anchor_x="center",
        anchor_y="center",
        color=text_color,
        font_size=text_size,
        weight="medium"
    )

    return [
        scene_types.Entity(
            bordered_rectangle,
            name,
            duration,
            interaction_name,
            hud,
            tags=tags + ["button_rect"],
            states=states
        ),
        scene_types.Entity(
            label,
            name,
            duration,
            None,
            hud,
            tags=tags + ["button_label"],
            states=states
        )
    ]

def image(
    name: str,
    image: pyglet.image.AbstractImage,
    position: tuple,
    size: tuple,
    duration: int,
    interaction_name: str | None,
    hud: bool,
    tags: list[str] | None = None,
    states: list[scene_types.State] | None = None
) -> scene_types.Entity:

    tags = _normalize_list(tags)
    states = _normalize_list(states)

    x, y = position
    w, h = size

    sprite = pyglet.sprite.Sprite(image, x=x, y=y)
    sprite.scale_x = w / image.width
    sprite.scale_y = h / image.height

    return scene_types.Entity(
        sprite,
        name,
        duration,
        interaction_name,
        hud,
        tags=tags,
        states=states
    )


def animated(
    name: str,
    animation: pyglet.image.animation.Animation,
    position: tuple,
    size: tuple,
    duration: int,
    interaction_name: str | None,
    hud: bool,
    tags: list[str] | None = None,
    states: list[scene_types.State] | None = None
) -> scene_types.Entity:

    tags = _normalize_list(tags)
    states = _normalize_list(states)

    x, y = position
    w, h = size

    sprite = pyglet.sprite.Sprite(img=animation, x=x, y=y)
    sprite.scale_x = w / sprite.width
    sprite.scale_y = h / sprite.height

    return scene_types.Entity(
        sprite,
        name,
        duration,
        interaction_name,
        hud,
        tags=tags + ["animated"],
        states=states + [scene_types.State("_animation_pause_frame_index", {"value": -1})]
    )


def keyboard_listener(
    name: str,
    key_symbol: int,
    interaction_name: str,
    duration: int = -1,
    tags: list[str] | None = None,
    states: list[scene_types.State] | None = None
) -> scene_types.Entity:

    tags = _normalize_list(tags)
    states = _normalize_list(states)

    rectangle = pyglet.shapes.Rectangle(
        x=0,
        y=0,
        width=0,
        height=0,
        color=(0, 0, 0)
    )

    return scene_types.Entity(
        rectangle,
        name,
        duration,
        f"{key_symbol}_{interaction_name}",
        False,
        tags=tags,
        states=states
    )


def layer_anchor(
    name: str,
    hud: bool = False,
    tags: list[str] | None = None
) -> scene_types.Entity:

    tags = _normalize_list(tags)

    rectangle = pyglet.shapes.Rectangle(0, 0, 0, 0, color=(0, 0, 0))

    return scene_types.Entity(
        drawable=rectangle,
        name=name,
        ticks_left=-1,
        interaction_name=None,
        hud=hud,
        tags=tags
    )
