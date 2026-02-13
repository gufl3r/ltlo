import utils.assets
import typing
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import game.types.ingames.night as night_types
import pyglet
import utils.registry.runtimeconfig as runtime_config
import game.features.ingames.night.sight as sight_feature

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def init_assets(scene: "NightScene"):
    scene.assets = utils.assets.asset_path_to_obj(
        images=
        [
            "assets/ingames/night/dark_room.png",

            "assets/ingames/night/vignette.png",
        ],
        animations=
        [
            "assets/ingames/night/lamp_on.gif",
            "assets/ingames/night/lamp_off.gif",

            "assets/ingames/night/blanket.gif"
        ],
        videos=
        [
            "assets/ingames/night/test.mp4"
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
    lamp_position = (room_size[0] - lamp_size[0], 0)
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

    foot_size = scene.relative_size(150, 80)
    foot_position = list(scene.relative_position(10, 100))
    foot_position[0] += int((room_size[0] / 2) - (foot_size[0] / 2))
    foot_hitbox = pyglet.shapes.Box(
        x=foot_position[0], 
        y=foot_position[1], 
        width=foot_size[0], 
        height=foot_size[1], 
        color=(255, 200, 200, 100), 
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

    # lub = look under bed
    lub_size = scene.relative_size(150, 100)
    lub_position = list(scene.relative_position(-300, 80))
    lub_position[0] += int((room_size[0] / 2) - (lub_size[0] / 2))
    lub_hitbox = pyglet.shapes.Box(
        x=lub_position[0], 
        y=lub_position[1], 
        width=lub_size[0], 
        height=lub_size[1], 
        color=(200, 200, 255, 100), 
        thickness=scene.relative_axis_value(2, "x")
    )

    lub_btn = scene_types.Entity(
        drawable=lub_hitbox,
        name="lub_trigger",
        ticks_left=-1,
        interaction_name="look_under_bed",
        hud=False,
        tags=["room_movable"]
    )

    vignette = generic_entities.image(
        name="vignette",
        image=scene.assets["images"]["vignette"],
        position=(0,0),
        size=tuple(scene.save["settings"]["resolution"]),
        duration=-1,
        interaction_name=None,
        hud=True
    )

    black_overlay = scene_types.Entity(
        drawable=pyglet.shapes.Rectangle(0,0,scene.save["settings"]["resolution"][0],scene.save["settings"]["resolution"][1], (0,0,0,0)),
        name="black_overlay",
        ticks_left=-1,
        interaction_name=None,
        hud=True,
    )

    initial_entities = [
        dark_room,
        lamp,
        blanket,
        *look_triggers,
        foot_btn,
        lub_btn,
        generic_entities.layer_anchor("overlay", True),
        vignette,
        black_overlay
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
    scene.play_cutscene(scene.assets["videos"]["test"])

def init_vars(scene: "NightScene") -> None:
    scene.x = 0
    scene.player = night_types.Player()

def post_init(scene: "NightScene"):
    room_width = scene.entities_by_name("dark_room")[0].drawable.width
    window_width = scene.save["settings"]["resolution"][0]

    center_offset = (room_width - window_width) / 2
    
    sight_feature.apply_sight_offset(scene, center_offset)