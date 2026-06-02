# Tetris2048-Game 🎮

**Tetris2048-Game** is a hybrid game that combines the falling-block mechanics of **Tetris** with the merging-number gameplay of **2048**.

> Built with **Python**, **Pygame**, and a lightweight drawing utility (`lib/stddraw.py`).

---

## ✨ Features

- Classic **Tetris** movement and rotation
- **Hard drop** support (spacebar)
- 2048-style **merge mechanics** (equal numbers combine)
- Score system based on merges and cleared rows
- Next-piece preview panel
- Pause menu + restart option
- Win condition when reaching **2048 tile**

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| ← / → | Move piece left/right |
| ↓ | Move down (soft drop) |
| ↑ | Rotate piece |
| Space | Hard drop |
| P | Pause / Resume |
| R | Restart (only while paused) |

---

## 🚀 Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/alirkal34-jpg/Tetris2048-Game.git
cd Tetris2048-Game
```

### 2) Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run the game

```bash
python Tetris_2048.py
```

---

## 📦 Dependencies

- Python 3.8+
- pygame
- numpy

---

## 🗂️ Project Structure

```
Tetris2048-Game/
│
├── Tetris_2048.py          # Main game loop + UI screens
├── game_grid.py            # Grid logic, merges, scoring, clearing rows
├── tetromino.py            # Tetromino shapes, movement, rotation
├── tile.py                 # Tile values + rendering
├── point.py                # Simple Point helper
│
├── lib/                    # Drawing & graphics helpers
│   ├── stddraw.py
│   ├── picture.py
│   └── color.py
│
├── images/                 # Menu + pause images
└── .vscode/                # VSCode settings
```

---

## ✅ Quality Notes

This project demonstrates:

- Object-oriented design
- Separation of concerns (grid, tile, tetromino, UI)
- Clean modular structure
- Readable code and documentation

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- Inspired by **Tetris** (falling-block puzzle classic)
- Inspired by **2048** (number merging puzzle)

---

## 👤 Author

Developed by **alirkal34-jpg**.

If you'd like to collaborate or provide feedback, feel free to open an issue or pull request.
