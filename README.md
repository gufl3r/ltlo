***

# Leave The Light Off (LTLO) & MarionettEngine

![Status](https://img.shields.io/badge/Status-Pre--Alpha-orange) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Engine](https://img.shields.io/badge/Engine-MarionettEngine-red) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

**Leave The Light Off** is a psychological survival horror game about sensory deprivation, memory, and the fear of what you cannot see.

It is powered by the **MarionettEngine**, a custom, philosophy-driven Python framework developed by **Gufl3r**. This repository is a monorepo containing both the agnostic engine core and the specific game implementation.

> **⚠️ DEVELOPMENT STATUS: ORGANIC / PRE-ALPHA**
>
> This project is in active, organic development. The engine and the game are evolving simultaneously. Features described in the "Plan" section may be partially implemented or currently in the prototyping phase.

---

## 📋 Table of Contents

1.  [The Game: Leave The Light Off](#-the-game-leave-the-light-off)
    *   [Premise & Lore](#premise--lore)
    *   [The Golden Rule](#the-golden-rule)
    *   [Core Mechanics](#core-mechanics)
2.  [The Engine: MarionettEngine](#-the-engine-marionettengine)
    *   [The Philosophy](#the-philosophy)
    *   [Architecture Deep Dive](#architecture-deep-dive)
    *   [The "Backstage" (Frame 0)](#the-backstage-frame-0)
3.  [Project Structure](#-project-structure)
4.  [Installation & Usage](#-installation--usage)
5.  [Building for Distribution](#-building-for-distribution)
6.  [Configuration & Persistence](#-configuration--persistence)
7.  [Roadmap & GDD Status](#-roadmap--gdd-status)

---

## 🕯 The Game: Leave The Light Off

### Premise & Lore
You are a child subject in a clandestine sleep laboratory. You have been in an induced coma for 10 days. The "Bedroom" you inhabit is not real—it is a mental simulation constructed by your subconscious to maintain low brain activity (Delta Waves) while an experimental chemical is tested on you.

However, the chemical is destabilizing. The simulation is failing. The "Monsters" are not ghosts; they are the system's aggressive attempts to hide rendering errors and memory corruptions before you notice them.

### The Golden Rule
**"Leave The Light Off."**

*   **The Logic:** Darkness hides the low-poly nature of the simulation.
*   **The Risk:** Turning on the light reveals the "glitches"—wireframe textures, missing assets, and the artificiality of your world.
*   **The Punishment:** The system (manifested as your Parents/Moderators) punishes illumination. They will intervene to force the simulation back into the dark.

### Core Mechanics
*   **The Bed:** Your anchor. You cannot walk; you can only move your head (Look Left/Right) and your hands.
*   **The Blanket (Oxygen vs. Safety):**
    *   Pulling the blanket up makes you invisible to the "Counter" monsters.
    *   **Cost:** Staying covered drains your **Stamina** (simulating oxygen deprivation).
*   **The Leg (Risk vs. Reward):**
    *   Sticking your foot out regains Stamina rapidly.
    *   **Risk:** It acts as a lure for the "Foot Monster" (Greed).
*   **The Lamp:**
    *   Your only defense against the "Front Monster" (Reflex).
    *   Use sparingly; light attracts the "Father" (Moderator), who will confiscate the lamp if provoked.

---

## 🎭 The Engine: MarionettEngine

**MarionettEngine** is built on a strict separation of data and behavior, rejecting traditional Object-Oriented game loops where objects "update themselves."

### The Philosophy

> *"The entities are empty corpses. The systems are the puppeteers. Frame 0 is the backstage."*

1.  **The Corpses (Entities):**
    Entities are strictly Data Classes (`engine.types.scene.Entity`). They contain a drawable (Pyglet sprite/shape), a state dictionary, and tags. They have **no methods**. They do not "think" or "move" on their own.

2.  **The Puppeteers (Systems & Features):**
    Logic resides exclusively in external Systems (e.g., `game/features/night/blanket.py`). These systems observe the scene, calculate physics or logic, and determine what the entities *should* do.

3.  **Coordinated Movement (Transactional Commits):**
    In a puppet show, strings are pulled in harmony. In the code, systems do not modify entities directly. They submit **Commit Configurations** (`EntitiesListByIdConfig`). The Scene applies all changes in a single, atomic transaction at the end of the tick.

### Architecture Deep Dive
*   **Scene:** The container. Manages the Input Queue, Logic Queue, and the Entity List.
*   **Factories:** Generators that produce Entity "corpses" (e.g., UI Buttons, Numeric Steppers).
*   **Relations:** Logic that binds two entities together (e.g., binding a text label's ID to a button's background ID) so they move in unison.

### The "Backstage" (Frame 0)
The engine treats the first frame of an entity's life (`ticks_alive == 0`) as the **Backstage**.
*   **Preparation:** Before an entity can *contracenar* (act/interact), it must be prepped.
*   **Binding:** Relations are resolved here. A button looks for its text; a slider looks for its value label.
*   **Injection:** Only after Frame 0 does the entity enter the main update loop (The Stage).

---

## 📂 Project Structure

The repository is a strict Monorepo separating the generic Engine from the specific Game.

```text
gufl3r-ltlo/
├── engine/                   # MARIONETTENGINE CORE
│   ├── factories/            # Props Dept: Generators for UI/Entities
│   ├── registry/             # Global Configs (Resolutions, Runtime)
│   ├── relations/            # Backstage Logic: Entity binding
│   ├── scenes/               # The Stage: Loop & Render logic
│   ├── systems/              # The Puppeteers: Input, Video, Pause
│   └── utils/                # Tools: Math, Logging, Assets
├── game/                     # LEAVE THE LIGHT OFF (DATA & LOGIC)
│   ├── assets/               # Costumes/Sets: .png, .gif, .mp4, .wav
│   ├── features/             # Specific Acts: Blanket, Lamp, Sight
│   ├── mastercontroller.py   # The Director: State Machine
│   ├── scenes/               # Specific Stages: Night, Menu, Underbed
│   └── systems/              # Game Logic implementation
├── shared/                   # SHARED RESOURCES
│   └── registry/             # JSON Storages (GameInfo, Capacities)
├── main.py                   # Entry Point
└── build.bat                 # Build Script
```

---

## 🛠 Installation & Usage

### Prerequisites
*   **Python 3.10+**
*   **Virtual Environment** (Highly Recommended)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gufl3r/gufl3r-ltlo.git
    cd gufl3r-ltlo
    ```

2.  **Initialize Virtual Environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include `pyglet` (Windowing/Media), `userpaths` (Saves), and `pyinstaller` (Building).*

4.  **Run the Game:**
    ```bash
    python main.py
    ```

---

## 📦 Building for Distribution

To compile the Python code into a standalone executable (Windows):

1.  Ensure the `.venv` is active.
2.  Run the build script:
    ```cmd
    build.bat
    ```
3.  The output will be in the `build/` folder. This bundles the interpreter, assets, and libraries using **PyInstaller**.

---

## ⚙ Configuration & Persistence

*   **Save Files:** Stored in `Documents/Gufler/ltlo_save.json`.
    *   Tracks progress (`night`), settings (`audio`, `resolution`), and flags.
    *   *Note:* Deleting this file resets the game.
*   **Runtime Config:** `shared/registry/storages/runtimeconfig.json`.
    *   Defines the base render resolution (`1280x720`) used for coordinate scaling.
*   **Game Capacities:** `shared/registry/storages/gamecapacities.json`.
    *   Lists supported resolutions (720p up to 4K).
*   **Logs:** Located in `shared/registry/runtime_root/logs/`.
    *   Generated on startup and crash. Useful for debugging "save file corrupted" errors.

---

## 🗺 Roadmap & GDD Status

### ✅ Implemented (Puppets on Stage)
*   **Engine Core:** Full ECS-lite structure, Scenes, Input/Logic Queues.
*   **UI System:** Menus, Settings, Audio Sliders, Resolution switching.
*   **Night Environment:** 360-degree (clamped) looking mechanics.
*   **Blanket Physics:** Tension-based pulling and "held" states.
*   **Stamina System:** Logic for oxygen drain and regen.
*   **The Lamp:** Toggling states and animation syncing.
*   **Video Integration:** Cutscene playback support (ffmpeg).

### 🚧 In Development (Rehearsing)
*   **The Foot:** Visual implementation of the leg extension (Logic exists).
*   **Underbed:** Subscene logic is ready, assets pending.
*   **Sanity/Visual Glitches:** Shaders to implement the "wireframe" effect when lights are on.

### 📝 Planned (The Script)
*   **Monsters:**
    *   *Front Monster:* Fast, glitchy movement.
    *   *Closet Monster:* Slow approach, resets on blanket cover.
*   **Moderators (Parents):** Logic to punish excessive noise or light.
*   **The TV:** Interactive channel switching and "Debug Code" entry (`2-7-1-3`).
*   **Endings:**
    *   *Conformed:* Submit to the simulation.
    *   *Breakthrough:* Crash the simulation via the TV code.

---

**Author:** Gufl3r
**Engine:** MarionettEngine
**License:** Proprietary / All Rights Reserved
