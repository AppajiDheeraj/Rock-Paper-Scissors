# Rock-Paper-Scissors

# ✊✋✌️ Rock Paper Scissors - AI vs You (Hand Gesture Controlled Game)

A fun computer vision-powered **Rock Paper Scissors** game where you play against an AI using just your **hand gestures and webcam**! Built with Python, OpenCV, and CVZone.

https://user-images.githubusercontent.com/your-demo.gif <!-- Optional: Add your demo gif if you have one -->

---

## 🎮 Features

- 🖐️ Real-time hand gesture detection (Rock, Paper, Scissors)
- 🤖 Smart AI with adaptive strategy based on player patterns
- 🧠 Pattern recognition to improve AI decisions
- 🕹️ Smooth game interface with scores, animations, and visual feedback
- 🔊 Optional sound effects (Countdown, Win/Lose/Draw)
- 🔁 Reset option and multiple round play

---

## 🧰 Tech Stack

- **Python**
- **OpenCV**
- **CVZone** (Hand detection)
- **NumPy**
- **Pygame** (for sound effects)
- **Enum** (to manage game states and moves)

---

## 📂 Folder Structure

📁 Resources/ 
├── BG.png # Game background image 
├── 1.png # Rock image (AI move)
├── 2.png # Paper image (AI move) 
├── 3.png # Scissors image (AI move) 
├── countdown.wav # Countdown sound 
├── win.wav # Player win sound 
├── lose.wav # AI win sound 
├── draw.wav # Draw sound

📄 rock_paper_scissors.py # Main game script

yaml
Copy
Edit

---

## 🚀 How to Run

1. **Clone this repo** or download the code.
2. Install dependencies:

```bash
pip install opencv-python cvzone numpy pygame
```
Place your assets in a folder named Resources/ (see structure above).

Run the game:

bash
Copy
Edit
python rock_paper_scissors.py
🕹️ Controls
Press S to start a round.

Press R to reset scores.

Press ESC to exit the game.

✋ Hand Gestures
Gesture	Fingers Up	Move
✊ Rock	[0, 0, 0, 0, 0]	ROCK
✋ Paper	[1, 1, 1, 1, 1]	PAPER
✌️ Scissors	[0, 1, 1, 0, 0]	SCISSORS

🧠 AI Logic
First 3 rounds: AI plays randomly.

After 3 rounds: AI tries to detect player patterns and choose counter moves.

If no valid gesture is detected, AI wins that round.

📸 Screenshots
<!-- Add screenshots if you want -->

🤝 Credits
cvzone by Murtaza's Workshop

OpenCV community

Sound effects: Free from online libraries

📜 License
This project is open source and free to use.
