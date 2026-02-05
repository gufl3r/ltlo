# LTLO

LTLO is a Python-based embedded game engine utilizing the Pyglet framework for rendering and window management. The architecture implements a tightly coupled, custom entity system designed for 2D applications, emphasizing transactional state updates and modular logic injection.

## Architecture

The system operates on a hierarchical state machine pattern, separating the application lifecycle (`MasterController`) from specific game contexts (`Scenes`).

### Core Loop
The execution flow is managed by `MasterController`, which instantiates specific `Scene` controllers (e.g., `MenuController`, `IngameController`).
*   **Time Management:** Frame limiting is handled manually via `time.sleep` with drift correction to maintain target FPS.
*   **Context Switching:** Scenes return string identifiers to the controller to trigger state transitions.

### Entity System
Entities are not strictly ECS-based but rather composition wrappers around Pyglet drawables (Sprites, Shapes, Labels, Animations).

*   **Structure:** An `Entity` class encapsulates the drawable, unique ID, tags, and lifecycle metadata (`ticks_left`).
*   **Logic Injection:** Entities contain no behavioral logic. Logic is applied externally by "Systems" or "Features" which query entities based on `tags` and `id`.
*   **Transactional Updates:** To ensure thread-safety and iteration stability, the entity list is immutable during the update loop. Mutations are handled via a commit system:
    *   `commit_entities_update_by_id`: Accepts a configuration object (`EntitiesListByIdConfig`) defining operations (spawn, destroy, replace).
    *   Operations are queued and resolved at a deterministic point in the frame cycle.
    *   Supports relational positioning (e.g., spawning an entity behind another specific ID).

### Logic Distribution
Logic is stratified into three layers:
1.  **Scenes:** Handle the main loop, event polling, and rendering calls.
2.  **Systems:** Manage initialization (`init_entities`, `init_assets`) and high-level process flow (`process_interaction`, `process_natural`).
3.  **Features:** Isolated modules implementing specific mechanics (e.g., `sight.py`, `audio.py`) that operate on filtered entity subsets.

## Subsystems

### Input Handling
Input events (keyboard, mouse) are captured via Pyglet decorators, normalized into a dictionary format, and pushed to an `_event_queue`. The logic layer consumes this queue, translating raw inputs into semantic "interactions" (e.g., converting a click on a coordinate to a specific entity interaction).

### Media Pipeline
The engine includes a custom media loader relying on FFmpeg.
*   **Dynamic Linking:** FFmpeg binaries are not bundled but expected in `libs/`. The engine dynamically adds this directory to `PATH` at runtime (`utils.libs.load`).
*   **Playback:** Video and audio playback are integrated directly into the `Scene` loop, supporting cutscenes and ambient audio tracks.

### Configuration & Persistence
*   **Runtime Config:** UI offsets and layout metrics are calculated dynamically during initialization or build time (`runtimeconfigextension`), allowing composite entities (like numeric steppers) to resolve internal relative referencing without hardcoded indices.
*   **Save System:** State persistence is handled via JSON serialization to the user's document directory (`utils.save`). It supports versioning and schema validation.

## Build Environment

The project is configured for PyInstaller using `build.bat`.

*   **Dependencies:** Requires `pyglet` and standard library modules.
*   **External Binaries:** FFmpeg shared libraries must be placed in `libs/` for media decoding.
*   **Asset Bundling:** The build process envelopes `assets`, `libs`, and configuration JSONs into a single executable.

## Directory Layout

*   `game/`: Core engine logic and game implementation.
    *   `mastercontroller.py`: Application lifecycle.
    *   `scenes/`: Base `Scene` class and specific implementations.
    *   `systems/`: Initialization and process logic per scene.
    *   `features/`: Modular game mechanics.
    *   `entitymodels/`: Factory functions for entity creation (Prefabs).
    *   `types/`: Dataclasses for strict typing of engine structures.
*   `utils/`: Helper libraries for assets, math, path resolution, and serialization.
*   `libs/`: Native binaries (FFmpeg).