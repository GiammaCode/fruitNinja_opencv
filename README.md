# Fruit Ninja with Computer Vision

A computer vision-based interactive game that brings the classic "Fruit Ninja" experience to your webcam. The player can slice fruits and avoid bombs using real-time hand tracking, without the need for controllers. This project demonstrates computer vision techniques applied to a fun and interactive game environment.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Future Improvements](#future-improvements)
- [License](#license)

## Project Overview
The objective of this project is to create an interactive, vision-based version of the game "Fruit Ninja" using Python and OpenCV. The player can interact with the game by moving their hand over fruits and bombs displayed on the screen. The game demonstrates how to use computer vision for hand tracking, image processing, and UI overlays in a real-time environment.

## Technologies Used

- **Python**: For overall scripting and program logic.
- **OpenCV**:
  - **Video Capture**: Captures video frames from the webcam.
  - **Image Processing**: Converts frames to grayscale, detects faces and hands, and applies image overlays.
  - **Cascade Classifiers (Haar)**: For detecting faces and eyes, enabling interactive overlays.
- **MediaPipe (or OpenCV Hand Tracking Alternative)**:
  - Tracks hand movements, allowing the player to slice fruits and interact with the game without any physical controllers.
- **UI Overlay with OpenCV**:
  - Interactive screens (menu, game, and game-over screen).
  - Displays score, "Game Over" message on the player’s forehead, and semi-transparent background images for aesthetic effects.

## Features

### Menu Screen
- **Start Button**: A pulsating button that appears on the menu screen. The player can hover over the button with their hand to start the game.
- **Semi-Transparent Background**: A partially opaque background image overlays the menu, giving it a polished look.

### Gameplay
- **Fruit Slicing**: Fruits appear randomly and fall from the top of the screen. The player can slice them by moving their hand over the fruits.
- **Bomb Avoidance**: Bombs occasionally appear, and slicing a bomb will deduct points from the score.
- **Score Display**: The current score is displayed on the screen, updating in real-time as fruits and bombs are sliced.

### Game Over Screen
- **Face Tracking**: When the score goes below zero, the game displays "Game Over" on the player's forehead using real-time face tracking.
- **Final Score**: The final score is displayed below the "Game Over" message, providing feedback on the player's performance.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/fruit-ninja-opencv.git
   cd fruit-ninja-opencv
   
2. **Install dependency**
   ```bash
   pip install -r requirements.txt