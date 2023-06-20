# Mancala Game

This is a Python implementation of the Mancala game. Mancala is a two-player strategy game that involves moving stones (seeds) across pits on a board. The objective of the game is to capture more seeds than the opponent.

![Mancala Demo](MancalaDemo.gif)


## Requirements

- Python 3.x
- Pygame library

## How to Play

1. Run the `game.py` script to start the game.
2. The game will display a graphical interface where you can interact with various screens.
3. The initial screen is the Game Mode Screen, where you can select the game mode (e.g., Player vs. Player, Player vs. AI).
4. After selecting the game mode, you will be prompted to enter the names of the players.
5. Once the players' names are entered, the game screen will appear, showing the board and the current player's turn.
6. To make a move, click on one of the pits on your side of the board. The seeds will be distributed counterclockwise to the subsequent pits.
7. If the last seed lands in your store, you get an extra turn. Otherwise, the turn switches to the other player.
8. The game continues until one player has no more seeds on their side of the board.
9. The game will then display the End Screen, showing the winner and the final scores.
10. From the End Screen, you can choose to play again, go back to the main menu, or exit the game.

## Features

- Player vs. Player mode: Two human players can compete against each other on the same computer.
- Player vs. AI mode: Play against an AI opponent with adjustable difficulty levels.
- Interactive graphical interface: The game provides a visually appealing interface using the Pygame library.
- Game rules enforcement: The game enforces the rules of Mancala, ensuring a fair and accurate gameplay experience.
- Instructions screen: The game includes an instructions screen that provides guidance on how to play.
