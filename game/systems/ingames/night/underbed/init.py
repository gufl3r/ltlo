import typing
import engine.factories.generic as generic_entities
import engine.types.scene as scene_types
import engine.registry.runtimeconfig as runtime_config
import pyglet

if typing.TYPE_CHECKING:
    from game.scenes.ingames.night.subscenes.underbed import UnderBedSubscene

def init_vars(scene: "UnderBedSubscene"):
    scene.assets = scene.data["assets"]
    scene.x = 0
    scene.y = 0

def init_entities(scene: "UnderBedSubscene"):
    under_bed_asset = scene.assets["images"]["under_bed"]
    height_multiplier = runtime_config.BASE_RESOLUTION[0] / under_bed_asset.width
    under_bed_size = (scene.save["settings"]["resolution"][0],scene.relative_axis_value(under_bed_asset.height * height_multiplier, "y"))

    under_bed = generic_entities.image(
        name="under_bed",
        image=under_bed_asset,
        position=(0, 0),
        size=under_bed_size,
        duration=-1,
        interaction_name=None,
        hud=False,
        tags=["movable"]
    )

    look_triggers_vertical_size = (scene.save["settings"]["resolution"][0], scene.save["settings"]["resolution"][1] * 0.3)

    top_h = look_triggers_vertical_size[1]   # altura total da zona vertical
    slow_h = top_h // 4                      # slow = 25% da zona
    fast_h = top_h - slow_h                  # fast = 75% da zona

    look_triggers_vertical = [
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=0,
                y=scene.save["settings"]["resolution"][1] - fast_h,  # começa no topo da tela
                width=look_triggers_vertical_size[0],
                height=fast_h,
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_fast", "look_up"]
        ),
        
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=0,
                y=scene.save["settings"]["resolution"][1] - fast_h - slow_h,
                width=look_triggers_vertical_size[0],
                height=slow_h,
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_slow", "look_up"]
        ),
        
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=0,
                y=0,  # começa no fundo da tela
                width=look_triggers_vertical_size[0],
                height=fast_h,
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_fast", "look_down"]
        ),
        
        scene_types.Entity(
            pyglet.shapes.Rectangle(
                x=0,
                y=fast_h,
                width=look_triggers_vertical_size[0],
                height=slow_h,
                color=(0, 0, 0, 0)
            ),
            "look_trigger",
            -1,
            None,
            True,
            tags=["look_slow", "look_down"]
        ),
    ]

    eub_size = scene.relative_size(1240, 60)
    eub_position = list(scene.relative_position(20, 20))
    eub_hitbox = pyglet.shapes.Box(
        x=eub_position[0], 
        y=eub_position[1], 
        width=eub_size[0], 
        height=eub_size[1], 
        color=(200, 200, 255, 100), 
        thickness=scene.relative_axis_value(2, "x")
    )

    eub_btn = scene_types.Entity(
        drawable=eub_hitbox,
        name="lub_trigger",
        ticks_left=-1,
        interaction_name="exit_under_bed",
        hud=False,
        tags=["movable"]
    )

    initial_entities = [
        under_bed,
        eub_btn,
        *look_triggers_vertical
    ]

    scene.commit_entities_update_by_id([scene_types.EntityInitializerConfig(entity_generator=lambda _, e=e: e) for e in initial_entities])

def post_init(scene: "UnderBedSubscene"):
    under_bed = scene.entities_by_name("under_bed")[0]
    scene.cached_ids["under_bed"] = under_bed.id_

    for entity in scene._entities:
        if entity.name == "look_trigger":
            side = "up" if "look_up" in entity.tags else "down"
            speed = "fast" if "look_fast" in entity.tags else "slow"
            
            key = f"look_{side}_{speed}"
            scene.cached_ids[key] = entity.id_