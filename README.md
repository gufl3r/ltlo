Here is the updated `README.md`. I have rewritten the architecture and introduction sections to reflect the **MarionettEngine** philosophy, emphasizing the "puppeteer" design pattern where entities are passive data containers controlled by central systems.

***

# Leave The Light Off (LTLO) & MarionettEngine

![Status](https://img.shields.io/badge/Status-In%20Development-orange) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Engine](https://img.shields.io/badge/Engine-MarionettEngine-red)

**Leave The Light Off** is a survival horror game about managing exposure and light in a hostile bedroom environment. It is powered by **MarionettEngine**, a custom Python framework designed by **Gufl3r**.

This repository is a monorepo containing both the engine core and the game implementation.

---

## 🎭 The Philosophy: MarionettEngine

> *"Every movement is coordinated. Everything happens at once. The entities are just empty corpses waiting for the strings to be pulled."*

Unlike traditional Object-Oriented game engines where objects update themselves, **MarionettEngine** treats Entities as passive data containers ("corpses"). They possess no logic, no methods, and no will of their own.

*   **The Stage (Scene):** Holds the state of the world.
*   **The Puppeteers (Systems & Features):** External logic modules that calculate what should happen next.
*   **The Strings (Transactional Commits):** The engine gathers all calculated changes and applies them in a single, coordinated transaction at the end of the tick. This ensures distinct separation between data and behavior.

---

## 📂 Project Structure

```text
gufl3r-ltlo/
├── engine/           # MarionettEngine Core
│   ├── factories/    # Generators for constructing entity "corpses" (UI, Sprites)
│   ├── registry/     # Global configuration states
│   ├── relations/    # Logic for binding entities (e.g., tying a Button to a Label)
│   ├── scenes/       # The Stage managers
│   ├── systems/      # The Puppeteers (Pause, Video, Input handling)
│   └── utils/        # Math, Logging, Asset loading
├── game/             # Leave The Light Off (Game Data)
│   ├── assets/       # Visuals and Audio
│   ├── features/     # Specific mechanics (Blanket physics, Sanity drain, Lamp logic)
│   ├── mastercontroller.py  # High-level state machine
│   └── scenes/       # Game-specific stages (Menu, Night, Underbed)
├── shared/           # Shared Data
│   └── registry/     # Game Capacities and Runtime Configs
├── main.py           # Entry point
└── build.bat         # Windows Build Script
```

---

## 🛠 Installation & Setup

### Prerequisites
*   **Python 3.10+**
*   **Virtual Environment** (Recommended)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gufl3r/gufl3r-ltlo.git
    cd gufl3r-ltlo
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include `pyglet` for windowing/rendering and `userpaths` for save management.*

---

## 🚀 Running the Game

To execute the project in development mode:

```bash
python main.py
```

---

## ⚙ Engine Architecture

### 1. Entities (The Corpses)
Located in `engine.types.scene`, an Entity is a strict Data Class. It contains:
*   `drawable`: The raw Pyglet object (Sprite, Label, Shape).
*   `states`: A list of data payloads (e.g., `held: True`, `stamina: 0.5`).
*   `tags`: String identifiers for grouping.
*   **No Logic:** An entity never "thinks".

### 2. Systems & Features (The Logic)
Logic is isolated in `game/features/` or `game/systems/`.
*   **Example:** The *Blanket Feature* checks the mouse position, calculates tension, and generates a *new* version of the Blanket Entity with updated coordinates.

### 3. Transactional Updates (The Coordination)
The Scene does not modify entities in place during the logic loop. Instead, features submit "Commit Configurations" via `scene.commit_entities_update_by_id()`.
*   **Replace:** Swap an old entity corpse for a new one.
*   **Behind:** Spawn a new entity behind an existing anchor.
*   All changes are applied simultaneously at the end of the cycle, preventing race conditions and ensuring frame-perfect synchronization.

---

## 🎮 Game: Leave The Light Off

A psychological horror game focusing on resource management and sensory deprivation.

### Mechanics
*   **The Blanket:** Your primary shield. Hold it to hide, but doing so drains your limited **Stamina**.
*   **The Leg:** Sticking your leg out regenerates stamina rapidly but leaves you vulnerable.
*   **The Lamp:** Your only source of light. Toggling it impacts visibility and entity aggression.
*   **Sanity:** Listen to audio cues. If the room changes, you must react.

### Controls

| Action | Input |
| :--- | :--- |
| **Look Around** | Move Mouse to screen edges |
| **Interact** | Left Mouse Click |
| **Pull Blanket** | Click & Drag Mouse Down |
| **Pause** | `ESC` |
| **Skip Video** | `ENTER` or `SPACE` |

---

## 📦 Building

To compile the engine and game into a standalone executable (Windows):

```cmd
build.bat
```
This utilizes **PyInstaller** to bundle the Python interpreter, dependencies, and assets into `build/leavethelightoff.exe`.

---

## 💾 Persistence

*   **Saves:** Stored in your User Documents folder (`Documents/Gufler/ltlo_save.json`).
*   **Logs:** Runtime logs are generated in `shared/registry/runtime_root/logs` for debugging crashes or logic errors.

---

**Author:** Gufl3r
**Status:** In Development (dev1.0.0)