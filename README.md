# Words War ⚔️

Words War is a simple console-based game that compares two words using their ASCII values. The game evaluates each character position, assigns points based on higher ASCII values, and concludes with a final showdown comparing the total ASCII sum of both words to determine the overall winner.

## 📌 Project Overview

This project demonstrates fundamental programming concepts including:

* Object-Oriented Programming (OOP)
* Input validation
* Loops and conditional logic
* ASCII value comparison
* Score calculation and result evaluation

The game runs entirely in the console and interacts with the user through text input and output.

## 🎮 How It Works

1. The user enters two words of equal length.
2. The program validates that both words have the same number of characters.
3. Each character is compared with its corresponding character using ASCII values.
4. The word with the higher ASCII value at each position earns one point.
5. After all characters are compared, total scores are calculated.
6. A final showdown compares the overall ASCII sum of both words.
7. The word with the higher score (or higher ASCII total in the final showdown) is declared the winner. If both results are equal, the game ends in a draw.

## ✅ Rules

* Both words must be the same length.
* Comparison is done character by character.
* If ASCII values are equal, no points are awarded for that round.
* The final result is based on total points and overall ASCII sum.
