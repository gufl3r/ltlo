from pyglet.window import Window, key
import pyglet
import time
import game.types.scenes as scene_types
import utils.detections
import utils.conversions
import utils.ids
import game.entitymodels.generic as generic_entities
import typing
import utils.registry.runtimeconfig as runtime_config
import dataclasses

class Scene:
    FPS = 60  # default, cada tela pode sobrescrever
    ANIMATION_LOOP_TAG = "animation_loop"

    def __init__(self, window: Window, save: dict) -> None:
        self.window = window
        self.save = save
        self.ticks_in_cycle: int = 0
        self.current_cycle: int = 0
        self._event_queue: list = []
        self._logic_queue: list = []
        self._entities: list[scene_types.Entity] = []
        self.video_player: pyglet.media.Player = pyglet.media.Player()
        self.audio_player: pyglet.media.Player = pyglet.media.Player()

        audio_settings = self.save["settings"]["audio"]
        self.video_player.volume = audio_settings["cutscene"] * audio_settings["master"]
        self.audio_player.volume = audio_settings["music"] * audio_settings["master"]

        @self.window.event
        def on_close():
            self._event_queue.append({"name": "close"})

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self._event_queue.append({
                "name": "mouse_press",
                "data": {"position": (x, y), "button": button}
            })

        @self.window.event
        def on_key_press(symbol, modifiers):
            self._event_queue.append({
                "name": "key_press",
                "data": {
                    "symbol": symbol
                }
            })
            if symbol == key.ESCAPE:
                return True # prevent default handler
        
        skip_video_listener = generic_entities.keyboard_listener(
            "enter_listener",
            key.ENTER,
            "skip_video",
            -1
        )

        self.commit_entities_update_by_id(
            [scene_types.EntitiesListByIdConfig(
                anchor_id=None,
                self_id=None,
                relation=None,
                entity_generator=lambda _, e=skip_video_listener: e
            )]
        )

    # ---------- HELPER METHODS ----------

    def play_sound_effect(self, sound_object: pyglet.media.Source):
        audio_settings = self.save["settings"]["audio"]
        disposable_player = sound_object.play()
        disposable_player.seek(0)
        disposable_player.volume = audio_settings["sfx"] * audio_settings["master"]

    def relative_position(self, x: int, y: int) -> tuple[int, int]:
        return utils.conversions.convert_position(
            (x, y),
            runtime_config.BASE_RESOLUTION,
            (self.window.width, self.window.height)
        )
    
    def relative_size(self, width: int, height: int) -> tuple[int, int]:
        return self.relative_position(width, height)
    
    def relative_coordinate(self, value: int, axis: typing.Literal["x", "y"]) -> int:
        return self.relative_position(value, value)[axis == "y"]
    
    def centered_position(self, width: int, height: int) -> tuple[int, int]:
        return (
            (self.window.width - width) // 2,
            (self.window.height - height) // 2
        )
    
    def commit_entities_update_by_id(self, configs: list[scene_types.EntitiesListByIdConfig]):
        commit_trackers: list[scene_types.CommitTracker] = []

        for config in configs:
            # ---- proteção de identidade (bootstrap-safe) ----
            needs_identity = (
                config.relation is not None and
                (
                    config.self_id == 0 or
                    config.anchor_id == 0
                )
            )

            if needs_identity:
                print(
                    "[WARN] Commit skipped: entity without identity "
                    f"(self_id={config.self_id}, anchor_id={config.anchor_id})"
                )
                continue

            # validações estruturais (bugs reais)
            if config.relation == "behind" and not config.anchor_id:
                raise ValueError("Invalid combination: behind relation requires anchor_id")

            if config.relation == "replace" and not config.self_id:
                raise ValueError("Invalid combination: replace relation requires self_id")

            if config.self_id and config.relation != "replace":
                raise ValueError("Invalid combination: self_id requires replace relation")

            if config.relation == "behind" and config.anchor_id == config.self_id:
                raise ValueError("Invalid combination: cannot be behind itself")

            # ---- spawn simples (não depende de identidade) ----
            if not config.relation:
                self._entities.append(config.entity_generator(None))
                continue

            # ---- commit normal ----
            commit_trackers.append(scene_types.CommitTracker(config))


        new_entities = []

        for entity in self._entities:
            no_match = True
            for commit_tracker in commit_trackers:
                if commit_tracker.done:
                    continue
                config: scene_types.EntitiesListByIdConfig = commit_tracker.config
                if entity.id_ == config.anchor_id:
                    commit_tracker.found_anchor = True
                    if config.relation == "behind":
                        new_entities.append(config.entity_generator(entity))
                        new_entities.append(entity)
                        commit_tracker.done = True
                        no_match = False
                        break

                    if config.relation == "replace" and not commit_tracker.found_self:
                        new_entities.append(config.entity_generator(None))
                        new_entities.append(entity)
                        commit_tracker.done = True
                        no_match = False
                        break

                elif entity.id_ == config.self_id:
                    new_entities.append(config.entity_generator(entity))
                    commit_tracker.found_self = True
                    commit_tracker.done = True
                    no_match = False
                    break

            if no_match:
                new_entities.append(entity)

        for commit_tracker in commit_trackers:
            config: scene_types.EntitiesListByIdConfig = commit_tracker.config
            if config.relation == "replace" and not commit_tracker.found_self:
                if config.anchor_id is None:
                    new_entities.append(config.entity_generator(None))

                elif not commit_tracker.found_anchor:
                    raise ValueError(f"Replace failed: Anchor '{config.anchor_id}' not found")

        self._entities = new_entities

    def entity_by_id(self, id_: int):
        for entity in self._entities:
            if entity.id_ == id_:
                return entity
            
    def entities_by_name(self, name: str):
        found_entities = []
        for entity in self._entities:
            if entity.name == name:
                found_entities.append(entity)
        return found_entities
    
    def entities_by_tags(self, required: list[str] | None = None, match: list[str] | None = None):
        found_entities = []

        for entity in self._entities:
            if required:
                if not all(tag in entity.tags for tag in required):
                    continue

            if match:
                if not any(tag in entity.tags for tag in match):
                    continue

            found_entities.append(entity)

        return found_entities

    # ---------- INPUT ----------
    def _process_events(self) -> None:
        self.window.dispatch_events()
        for event in self._event_queue:
            match event["name"]:
                case "close":
                    self._logic_queue.append({"name": "exit"})
                case "mouse_press":
                    for entity in reversed(self._entities):
                        if (
                            entity.interaction_name and
                            utils.detections.point_inside_area(
                                event["data"]["position"],
                                (entity.drawable.position, (entity.drawable.width, entity.drawable.height))
                            )
                        ):
                            self._logic_queue.append({
                                "name": "interaction",
                                "data": {
                                    "interaction_name": entity.interaction_name,
                                    "entity_id": entity.id_
                                }
                            })
                            break
                case "key_press":
                    for entity in self._entities:
                        symbol_prefix = f"{event['data']['symbol']}_"
                        if (
                            entity.interaction_name and
                            entity.interaction_name.startswith(symbol_prefix)
                        ):
                            self._logic_queue.append({
                                "name": "interaction",
                                "data": {"interaction_name": entity.interaction_name.split(f"{event['data']['symbol']}_")[1]}
                            })
                            break

        self._event_queue.clear()

    # ------ VIDEO MANAGER ------

    def _tick_video(self):
        if self.video_player.source:
            if self.video_player.time > self.video_player.source.duration:
                self.video_player.next_source()
                self.after_video(self.video_player)
            texture = self.video_player.texture
            if texture:
                texture.blit(0, 0, width=self.window.width, height=self.window.height)
    
    def _video_process_logic(self):
        for logic in self._logic_queue:
            if logic["name"] == "exit":
                return "exit"
            if logic["name"] == "interaction" and logic["data"]["interaction_name"] == "skip_video":
                self.after_video(self.video_player)
        self._logic_queue.clear()

    # ------ AUDIO MANAGER ------

    def _tick_audio(self):
        if self.audio_player.source and self.audio_player.time > self.audio_player.source.duration:
            self.audio_player.next_source()
            self.after_audio(self.audio_player)

    # ------ MEDIA MANAGER ------

    def _after_media(self, player: pyglet.media.Player) -> None:
        if player.loop:
            player.seek(0)
        else:
            player.next_source()

    # ---------- HOOKS ----------

    def generate_natural_logic(self) -> None:
        pass

    def after_video(self, player) -> None:
        self._after_media(player)

    def after_audio(self, player) -> None:
        self._after_media(player)

    def process_interaction(self, logic_data) -> str | None:
        pass

    def process_natural(self, logic) -> str | None:
        pass

    def resolve_initial_relations(self, i: int, entity: scene_types.Entity):
        return entity.relations

    # ---------- DRAW ----------

    def _draw(self) -> None:
        self.window.clear()
    
        for entity in self._entities:
            entity.drawable.draw()

        self._tick_video()
        self.window.flip()

    # ------- PROCESS LOGIC -------

    def _process_logic(self) -> str | None:
        result = None
        for logic in self._logic_queue:
            if logic["name"] == "interaction":
                result = self.process_interaction(logic["data"])
            else:
                result = self.process_natural(logic)
        if result:
            return result
        self._logic_queue.clear()

    # ------- ANIMATION ENTITY -------

    def _has_on_animation_end(self, drawable) -> bool:
        stack = getattr(drawable, "_event_stack", None)
        if not stack:
            return False

        for level in stack:
            if "on_animation_end" in level:
                return True

        return False

    def _tick_animation(self, entity: scene_types.Entity):
        animation_pause_state = next(state for state in entity.states if state.name == "_animation_pause_frame_index")
        animation_pause_frame_index = animation_pause_state.data["value"]
        if animation_pause_frame_index != -1:
            entity.drawable.frame_index = animation_pause_frame_index
        if not self._has_on_animation_end(entity.drawable):
            @entity.drawable.event
            def on_animation_end(entity=entity):
                if self.ANIMATION_LOOP_TAG not in entity.tags:
                    entity.drawable.frame_index = len(entity.drawable.image.frames)-1

    # ------- UPDATE ENTITIES -------

    def _update_entities(self) -> None:
        new_entities = [[], []]  # world, hud

        for i, entity in enumerate(self._entities):
            if entity.ticks_left == 0:
                continue
            
            if "animated" in entity.tags:
                self._tick_animation(entity)
            new_entity = dataclasses.replace(
                entity,
                ticks_left=entity.ticks_left-1 if entity.ticks_left != -1 else entity.ticks_left, # decreases if not set as permanent
                id_=utils.ids.generate_id() if entity.ticks_alive == 0 else entity.id_,
                relations=self.resolve_initial_relations(i, entity) if entity.ticks_alive == 1 else entity.relations,
                ticks_alive=entity.ticks_alive+1,
            )

            new_entities[new_entity.hud].append(new_entity)

        self._entities = new_entities[0] + new_entities[1]

    # ---------- MAIN LOOP ----------
    def loop(self) -> str:
        frame_time = 1 / self.FPS
        cycle_start = time.perf_counter()

        while True:
            time.sleep(frame_time)
            pyglet.clock.tick()

            self.ticks_in_cycle += 1

            if self.ticks_in_cycle >= self.FPS:
                now = time.perf_counter()
                elapsed = now - cycle_start  # quanto tempo real levou esse ciclo

                # erro relativo do ciclo
                correction = elapsed / 1.0  # 1.0s é o alvo
                frame_time /= correction

                self.ticks_in_cycle = 0
                cycle_start = now
                if not self.video_player.source:
                    self.current_cycle += 1

            self._process_events()
            if not self.video_player.source:
                self._tick_audio()
                self.generate_natural_logic()
                self._update_entities()
                new_scene = self._process_logic()
                if new_scene:
                    return new_scene
            else:
                new_scene = self._video_process_logic()
                if new_scene:
                    return new_scene
            self._draw()