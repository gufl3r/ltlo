import utils.assets
import typing
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import game.types.ingames.night as night_types
import pyglet
import utils.registry.runtimeconfig as runtime_config

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def init_assets(scene: "NightScene"):
    scene.assets = utils.assets.asset_path_to_obj(
        images=
        [
            "assets/ingames/night/dark_room.png",
        ],
        animations=
        [
            "assets/ingames/night/lamp_on.gif",
            "assets/ingames/night/lamp_off.gif",

            "assets/ingames/night/blanket.gif"
        ]
    )

def init_entities(scene: "NightScene"):
    dark_room_asset = scene.assets["images"]["dark_room"]
    width_multiplier = runtime_config.BASE_RESOLUTION[1] / dark_room_asset.height
    room_size = (scene.relative_axis_value(dark_room_asset.width * width_multiplier, "x"), scene.save["settings"]["resolution"][1])
    dark_room = generic_entities.image(
        "dark_room",
        dark_room_asset,
        (0,0),
        room_size,
        -1,
        None,
        False,
        ["room_movable"]
    )

    look_triggers_size = (scene.save["settings"]["resolution"][0] * 0.3, scene.save["settings"]["resolution"][1])
    side_w = look_triggers_size[0]
    slow_w = side_w // 4
    fast_w = side_w - slow_w
    look_triggers = [
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=0,
                y=0,
                width=fast_w,
                height=look_triggers_size[1],
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_fast", "look_left"]
        ),

        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=fast_w,
                y=0,
                width=slow_w,
                height=look_triggers_size[1],
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_slow", "look_left"]
        ),

        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=scene.save["settings"]["resolution"][0] - fast_w,
                y=0,
                width=fast_w,
                height=look_triggers_size[1],
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_fast", "look_right"]
        ),

        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=scene.save["settings"]["resolution"][0] - fast_w - slow_w,
                y=0,
                width=slow_w,
                height=look_triggers_size[1],
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_slow", "look_right"]
        ),
    ]

    lamp_asset: pyglet.image.animation.Animation = scene.assets["animations"]["lamp_off"]
    lamp_size = scene.relative_size(lamp_asset.get_max_width(), lamp_asset.get_max_height())
    lamp_position = scene.relative_position(room_size[0] - lamp_size[0], 0)
    lamp = generic_entities.animated(
        name="lamp",
        animation=lamp_asset,
        position=lamp_position,
        size=lamp_size,
        duration=-1,
        interaction_name="toggle_lamp",
        hud=False,
        tags=["room_movable"],
        states=[scene_types.State("turned_on", {"value": False})]
    )

    blanket = generic_entities.animated(
        name="blanket",
        animation=scene.assets["animations"]["blanket"],
        position=(0,-scene.save["settings"]["resolution"][1]),
        size=tuple(scene.save["settings"]["resolution"]),
        duration=-1,
        interaction_name="use_blanket",
        hud=True,
        states=[scene_types.State("held", {"value": False})]
    )

    foot_size = scene.relative_size(120, 80)
    foot_position = list(scene.relative_position(240, 80))
    foot_position[0] += int((room_size[0] / 2) - (foot_size[0] / 2))
    foot_hitbox = pyglet.shapes.Box(
        x=foot_position[0], 
        y=foot_position[1], 
        width=foot_size[0], 
        height=foot_size[1], 
        color=(255, 255, 255, 100), 
        thickness=scene.relative_axis_value(2, "x")
    )

    foot_btn = scene_types.Entity(
        drawable=foot_hitbox,
        name="foot_trigger",
        ticks_left=-1,
        interaction_name="toggle_foot",
        hud=False,
        tags=["room_movable"]
    )
    initial_entities = [
        dark_room,
        lamp,
        blanket,
        *look_triggers,
        foot_btn
    ]

    scene.commit_entities_update_by_id(
        [
            scene_types.EntitiesListByIdConfig(
                relation=None,
                entity_generator=lambda _, e=e: e
            )
            for e in initial_entities
        ]
    )

def init_media(scene: "NightScene"):
    pass

def init_vars(scene: "NightScene") -> None:
    scene.x = 0
    scene.player = night_types.Player()