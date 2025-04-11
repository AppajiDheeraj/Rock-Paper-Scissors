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

📁 Resources/<br>
├── BG.png # Game background image <br>
├── 1.png # Rock image (AI move) <br>
├── 2.png # Paper image (AI move) <br>
├── 3.png # Scissors image (AI move) <br>
├── countdown.wav # Countdown sound <br>
├── win.wav # Player win sound <br>
├── lose.wav # AI win sound <br>
├── draw.wav # Draw sound <br>

📄 rock_paper_scissors.py # Main game script

---

## 🚀 How to Run

1. **Clone this repo** or download the code.
2. Install dependencies:

```bash
pip install opencv-python cvzone numpy pygame
```
Place your assets in a folder named Resources/ (see structure above).

Run the game:

```bash
python rock_paper_scissors.py
```
---

##🕹️ Controls<br>
Press S to start a round.<br>

Press R to reset scores.<br>

Press ESC to exit the game.<br>

---

##✋ Hand Gestures<br>
| Gesture       | Fingers Up         | Move     |
|---------------|--------------------|----------|
| ✊ Rock        | [0, 0, 0, 0, 0]    | ROCK     |
| ✋ Paper       | [1, 1, 1, 1, 1]    | PAPER    |
| ✌️ Scissors    | [0, 1, 1, 0, 0]    | SCISSORS |

---

##🧠 AI Logic <br>
First 3 rounds: AI plays randomly. <br>

After 3 rounds: AI tries to detect player patterns and choose counter moves. <br>

If no valid gesture is detected, AI wins that round. <br>

---

##📸 Screenshots <br>
<!-- Add screenshots if you want -->

---

##🤝 Credits <br>
cvzone by Murtaza's Workshop <br>

OpenCV community <br>

Sound effects: Free from online libraries <br>

---

##📜 License <br>
This project is open source and free to use.
