# Leave The Light Off (LTLO) & MarionettEngine

![Status](https://img.shields.io/badge/Status-Pre--Alpha-orange) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Engine](https://img.shields.io/badge/Engine-MarionettEngine-red) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

**Leave The Light Off** is a psychological survival horror game about sensory deprivation, resource management, and the childhood fear of what lies in the dark.

It is powered by the **MarionettEngine**, a custom, philosophy-driven Python framework developed by **Gufl3r**. This repository is a monorepo containing both the agnostic engine core and the specific game implementation.

> **⚠️ DEVELOPMENT STATUS: ORGANIC / PRE-ALPHA**
>
> This project is in active, organic development. The engine and the game are evolving simultaneously. Features described below may be partially implemented or currently in the prototyping phase.

---

## 📋 Table of Contents

1.  [The Game: Leave The Light Off](#-the-game-leave-the-light-off)
    *   [Premise](#premise)
    *   [The Golden Rule](#the-golden-rule)
    *   [Mechanics](#mechanics)
2.  [The Engine: MarionettEngine](#-the-engine-marionettengine)
    *   [The Philosophy](#the-philosophy)
    *   [The "Backstage" (Frame 0)](#the-backstage-frame-0)
    *   [Architecture Deep Dive](#architecture-deep-dive)
3.  [Project Structure](#-project-structure)
4.  [Installation & Usage](#-installation--usage)
5.  [Building for Distribution](#-building-for-distribution)
6.  [Configuration & Persistence](#-configuration--persistence)
7.  [Roadmap](#-roadmap)

---

## 🕯 The Game: Leave The Light Off

### Premise
You wake up in a room that feels familiar, yet terrifyingly wrong. You are paralyzed in bed, unable to run, unable to fight. You can only look around, move your hands, and manage your limited protection.

Something is in the room with you. It moves when you aren't looking. It changes when the lights are on.

### The Golden Rule
**"Leave The Light Off."**

Your instinct screams for light, but in this place, the light is not your ally. Illumination reveals things that should not be seen—distortions in the world that attract unwanted attention from the "Moderators." To survive the night, you must embrace the darkness, even if it terrifies you.

### Mechanics
*   **The Bed:** Your anchor. You are confined here. You can look Left and Right to monitor the room's entrances.
*   **The Blanket (Oxygen vs. Safety):**
    *   Pulling the blanket up makes you effectively invisible to certain threats.
    *   **Cost:** Staying covered drains your **Stamina** (simulating oxygen deprivation). If you run out of air, you will be forced to uncover yourself, gasping.
*   **The Leg (Risk vs. Reward):**
    *   Sticking your foot out from under the covers regenerates Stamina rapidly.
    *   **Risk:** It acts as a lure. Something under the bed is waiting for a slip-up.
*   **The Lamp:**
    *   A tool of last resort. It can ward off specific entities that thrive in shadow.
    *   **Consequence:** Overuse attracts the "Father," a presence that enforces the darkness.

---

## 🎭 The Engine: MarionettEngine

**MarionettEngine** is built on a strict separation of data and behavior, rejecting traditional Object-Oriented game loops where objects "update themselves."

### The Philosophy

> *"The entities are empty corpses. The systems are the puppeteers. Frame 0 is the backstage."*

1.  **The Corpses (Entities):**
    Entities are strictly Data Classes (`engine.types.scene.Entity`). They contain a drawable (Pyglet sprite/shape), a state dictionary, and tags. They have **no methods**. They do not "think," "move," or "decide" anything on their own.

2.  **The Puppeteers (Systems & Features):**
    Logic resides exclusively in external Systems (e.g., `game/features/night/blanket.py`). These systems observe the scene, calculate physics or logic based on the data, and determine what the entities *should* do next.

3.  **Coordinated Movement (Transactional Commits):**
    In a puppet show, strings are pulled in harmony. In the code, systems do not modify entities directly in real-time. They submit **Commit Configurations** (`EntityInitializerConfig`). The Scene applies all changes in a single, atomic transaction at the end of the tick, ensuring frame-perfect synchronization.

### The "Backstage" (Frame 0)
The engine treats the first frame of an entity's life (`ticks_alive == 0`) as the **Backstage**.

*   **Preparation:** Before an entity acts (*contracena*), it enters the stage frozen.
*   **Binding:** Relations are resolved here. A UI Button looks for its Text Label; a Slider looks for its Value Display.
*   **Injection:** Only after this preparation phase does the entity enter the main update loop (The Stage).

### Architecture Deep Dive
*   **Scene:** The container. Manages the Input Queue, Logic Queue, and the Entity List.
*   **Factories:** Generators that produce Entity "corpses" (e.g., UI Buttons, Numeric Steppers).
*   **Relations:** Logic that binds two entities together (e.g., binding a text label's ID to a button's background ID) so they move in unison without being the same object.

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
*   **Runtime Config:** `shared/registry/storages/runtimeconfig.json`.
    *   Defines the base render resolution (`1280x720`) used for coordinate scaling.
*   **Game Capacities:** `shared/registry/storages/gamecapacities.json`.
    *   Lists supported resolutions (720p up to 4K).
*   **Logs:** Located in `shared/registry/runtime_root/logs/`.
    *   Generated on startup and crash. Essential for debugging.

---

## 🗺 Roadmap

### ✅ Implemented (Puppets on Stage)
*   **Engine Core:** Full ECS-lite structure, Scenes, Input/Logic Queues.
*   **UI System:** Menus, Settings, Audio Sliders, Resolution switching.
*   **Night Environment:** 360-degree (clamped) looking mechanics.
*   **Blanket Physics:** Tension-based pulling and "held" states.
*   **Stamina System:** Logic for oxygen drain and regen.
*   **The Lamp:** Toggling states and animation syncing.
*   **Video Integration:** Cutscene playback support.

### 🚧 In Development (Rehearsing)
*   **The Foot:** Visual implementation of the leg extension mechanics.
*   **Underbed:** Logic for checking beneath the bed (Subscene architecture ready).
*   **Atmosphere:** Visual distortion effects for when the lamp is active.

### 📝 Planned (The Script)
*   **Entity AI:** Behaviors for the "Front," "Closet," and "Bed" entities.
*   **The Moderators:** Logic for the parental figures (Mother/Father) interventions.
*   **The TV:** Interactive channel switching mechanics.
*   **Progression:** 5-Night structure with escalating difficulty and narrative reveals.

---

**Author:** Gufl3r
**Engine:** MarionettEngine
**License:** Proprietary / All Rights Reserved
