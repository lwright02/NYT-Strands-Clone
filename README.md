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
- `python3 src/gui.py`
    - This will generate a random game with the default art frame
- Drag or click letters to form word strands
- Press h key for hint when hint meter is full

# Extra Fun
- **GUI Commands:**
  - Use -g or --game to specify board:
    - `python3 src/gui.py -g fore`
  - Show preset boards with answers highlighted:
    - `python3 src/gui.py --show -g fore`
  - Use -h or --hint followed by an integer to change the hint threshold:
    - `python3 src/gui.py -h 5`
  - Use -a or --art to launch game with different art frames:
    - `python3 src/gui.py -a stub -g`
    - `python3 src/gui.py -a 9slices -g`
    - `python3 src/gui.py --art cat0 -g`
    - `python3 src/gui.py --art cat3 -g`
    - `python3 src/gui.py --art cat4 -g`

- **TUI Commands:**  
  *(Replace `gui.py` with `tui.py` in all above commands)*

- **Notes:**
  - Categories 0–3 render differently based on frame and interior parameters.
  - Category 4 dimensions are implementation-defined.
  - Unsupported categories will print a message and exit.
