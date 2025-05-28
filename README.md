# CMSC 14200 Course Project

Team members:
QA: Casey Kemp (ckemp)
Art: Louis Girard (louisgirard)
GUI: Liam Wright (liamw)
TUI: Morgan Sheehan (mcsheehan)

## Revisions

### Game Logic

Issue with loading invalid game files.
Your code should:
1. Detect and handle invalid boards, including those with short answers.
2. Validate whether a strand path exceeds the board boundaries.
3. Ensure that the starting position of each strand is within the board's bounds.

To address this feedback, we edited the initialization of StrandsGame. Lines
303-305 now check for short answers. The satrting position is validated now in
lines 310-312, and we ensure each strand doesn't exceed the boundary by calling
"self._board.get_letter(pos)" in line 321, as it throws an error if it receives
and input position off the board. 

Issue with hint feature. 
This component should be included in the next milestone.

To address this feedback, we changed the logic for the way hints work. Now, if
you submit a word that is a dictionary word but not a theme word, you get a 
point added to your hint meter, and if you have more points than the hint 
threshold, you can request a hint. The logic for this is implemented across
several functions, namely those below line 417. 

### GUI
This component received two S scores in Milestone 2.

### TUI

This component received two S scores in Milestone 2. 

### Art

This component received two S scores in Milestone 2.

### QA

This component received two S scores in Milestone 2. 


## Enhancements

### FEATURE-1

Implemented a TUI-SPECIAL. The special game file is called customized.txt and 
can be found in assets. There is also a customized frame for this game. 

### FEATURE-2

Implemented a full scoring system into the game logic and surfaced it in both GUI and TUI:

+10 points for each new theme word found

+5 points for each new non-theme dictionary word

–2 points for each “Too short” or “Not in word list” attempt

–5 points each time you use a hint successfully

### FEATURE-3

Implemented a title screen for GUI
