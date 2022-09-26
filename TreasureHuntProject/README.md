Treasure Hunt - A Python Project
================
This Python project is still under development and is still in its infancy.
The core idea is functional without any bugs.


The project is a treasure hunt game
where the user has to find the treasure by inputting the direction
and the number of steps to move in the given direction.

How it works:
The program creates a file in a given path.
The file contains the numbers 0 to 9,
each repeated for a random number of times.
After the number 9, the program writes the word "TREASURE" and then
proceeds to write the same numbers in revere order, from 9 to 0,
again - for a random number of times.

Once the treasure is found,
the program will ask the user for name and ID,
compare the user's score to other scores in the file, if they exist,
and notify the user if he/she has entered the top 10 high scores.

The program will keep track of the top 10 high scores with a csv file
and will update it every time a new high score is achieved using a temp csv file.