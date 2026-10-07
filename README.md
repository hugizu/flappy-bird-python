# Flappy Bird 

Flappy Bird clone built with Python and Pygame.

The project includes animated bird movement, randomly generated pipes, collision detection, score tracking, and a restart system.

## Features

- Animated bird character
- Gravity and jumping mechanics
- Mouse control
- Random pipe positions and gap sizes
- Collision detection
- Score counter
- Scrolling ground
- Game-over screen
- Restart button

## Technologies Used

- Python
- Pygame

## Controls

- Left mouse button: make the bird flap
- Restart button: restart the game after losing

## How It Works

The bird is affected by gravity and falls unless the player makes it flap.

Pipes are generated automatically and move from right to left. Their vertical position and gap size are randomized.

The player earns one point every time the bird successfully passes through a pair of pipes.

The game ends when the bird:

- Hits a pipe
- Hits the ground
- Flies above the top of the screen

After a game over, the player can press the restart button to start again.

## What I Practiced

- Object-oriented programming
- Python classes
- Pygame sprites and sprite groups
- Collision detection
- User input handling
- Game loops
- Animation
- Random generation
- Basic game state management
  
## How to Run

Install Pygame:

pip install pygame

Then run:

python main.py

## Author
Lada Savitskaya
Computer Science student at KIMEP University.
