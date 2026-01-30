import utils.path
import utils.assets
import typing
import game.entitymodels.generic as generic_entities
import game.types.scenes as scene_types
import pyglet

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night import NightScene

def init_assets(scene: "NightScene"):
    scene.assets = utils.assets.asset_path_to_obj(
        images=
        [
            utils.path.resource_path("assets/ingames/night/dark_room.png"),
        ],
    )

def init_entities(scene: "NightScene"):
    dark_room_image = scene.assets["images"]["dark_room"]
    width_multiplier = scene.BASE_RESOLUTION[1] / dark_room_image.height
    dark_room = generic_entities.image(
        "office",
        dark_room_image,
        (0,0),
        scene.relative_size(dark_room_image.width * width_multiplier, scene.BASE_RESOLUTION[1]),
        -1,
        None,
        False,
        ["room_movable"]
    )

    look_triggers_size = scene.relative_size(scene.BASE_RESOLUTION[0] * 0.3, scene.BASE_RESOLUTION[1])
    side_w = look_triggers_size[0]
    slow_w = side_w // 2
    fast_w = side_w - slow_w

    look_triggers = [
        # LEFT — fast (externo, na borda)
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

        # LEFT — slow (interno)
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

        # RIGHT — fast (externo, na borda)
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=scene.BASE_RESOLUTION[0] - fast_w,
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

        # RIGHT — slow (interno)
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=scene.BASE_RESOLUTION[0] - fast_w - slow_w,
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
    
    initial_entities = [
        dark_room,
        *look_triggers
    ]

    scene.commit_entities_update_by_id(
        [
            scene_types.EntitiesListByIdConfig(
                relation=None,
                entity_generator=lambda _old, e=e: e
            )
            for e in initial_entities
        ]
    )

def init_media(scene: "NightScene"):
    pass

def init_vars(self) -> None:
    pass