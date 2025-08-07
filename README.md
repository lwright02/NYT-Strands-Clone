# CMSC 14200 Course Project 

# Roles:
- QA: Casey Kemp
- Art: Louis Girard
- GUI: Liam Wright
- TUI: Morgan Sheehan
- Logic: All Members

# How to Play

- Navigate to the root of the Repository before running any commands
- pip install pygame click

- **GUI Commands:**
  - Show preset boards with answers highlighted:
    - `python3 src/gui.py --show -g cs-142`
    - `python3 src/gui.py --show -g on-the-side`
    - `python3 src/gui.py --show -g fore`
  - Play golf game in cheat mode (hint threshold = 0):
    - `python3 src/gui.py -g fore -h 0`
  - Play standard golf game:
    - `python3 src/gui.py -g fore`
  - Launch game with different art frames (if supported):
    - `python3 src/gui.py --art cat0 -g fore`
    - `python3 src/gui.py --art cat1 -g fore`
    - `python3 src/gui.py --art cat2 -g fore`
    - `python3 src/gui.py --art cat3 -g fore`
    - `python3 src/gui.py --art cat4 -g fore`
  - Run random games and play moves:
    - `python3 src/gui.py` (run multiple times)

- **TUI Commands:**  
  *(Replace `gui.py` with `tui.py` in all above commands)*

- **Art Display Commands (GUI):**
  - Run examples with different art categories, frames, and sizes, e.g.:
    - `python3 src/art_gui.py --art cat0 -f 20 -w 250 -h 300`
    - `python3 src/art_gui.py --art cat1 -f 50 -w 300 -h 400`
    - `python3 src/art_gui.py --art cat4`
  
- **Art Display Commands (TUI):**
  - Run examples with different art categories and sizes, e.g.:
    - `python3 src/art_tui.py --art cat0 -f 2 -w 12 -h 8`
    - `python3 src/art_tui.py --art cat3 -f 3 -w 15 -h 11`
    - `python3 src/art_tui.py --art cat4`

- **Notes:**
  - Categories 0–3 render differently based on frame and interior parameters.
  - Category 4 dimensions are implementation-defined.
  - Unsupported categories will print a message and exit.
