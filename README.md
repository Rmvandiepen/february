# Hashiwokakero
February Monthly Coding Challenge
https://en.wikipedia.org/wiki/Hashiwokakero

The goal is to connect all of the islands by drawing a series of bridges between the islands. The bridges must follow certain criteria:
- They must begin and end at distinct islands, travelling a straight line in between.
- They must not cross any other bridges or islands.
- They may only run orthogonally (i.e. they may not run diagonally).
- At most two bridges connect a pair of islands.
- The number of bridges connected to each island must match the number on that island.
- The bridges must connect the islands into a single connected group.

Difficulty levels:
- Mandatory: Take the input file and show the before and after solution
- Optional (Easy): Create an interface where the user can play the before and show the result (check if the user is correct)
- Optional (Hard): Besides the static input file and the interface, create a generator of new puzzles based on the above rules (size of the puzzle can vary, or it can be something like 7x7, 10x10)

Please submit your code to the following repo:
https://gitlab.azerdev.com/native-app-technology/monthly-challenges/february
If you require access, please request it with r.vandiepen@azerion.com

Next to this document you’ll find the file `february_hashi_puzzles.txt`. This file contains 16 puzzles which you can use to validate your program. Each line in the file is a puzzle. 
The first part of the line contains the dimensions eg. 7x7 or 15x15
After this there will be the “S” for start
Then there will be the content of the puzzle. Each position in the grid will be represented either by a 0 (empty cell) or any value from 1 to 8. This value represents the number off bridges connected to that island/cell
The line will end with a line ending

The first 5 puzzles in this file are matching the 5 examples you’ll find in the `examples` dir.
