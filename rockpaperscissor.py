import random
import time
import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from enum import Enum

class GameState(Enum):
    WAITING = 0
    COUNTDOWN = 1
    SHOW_RESULT = 2

class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    NONE = 0
    
    @staticmethod
    def from_fingers(fingers):
        if fingers == [0, 0, 0, 0, 0]:
            return Move.ROCK
        elif fingers == [1, 1, 1, 1, 1]:
            return Move.PAPER
        elif fingers == [0, 1, 1, 0, 0]:
            return Move.SCISSORS
        return Move.NONE
    
    def beats(self, other):
        return ((self == Move.ROCK and other == Move.SCISSORS) or
                (self == Move.PAPER and other == Move.ROCK) or
                (self == Move.SCISSORS and other == Move.PAPER))

class RockPaperScissorsGame:
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        
        # Initialize hand detector
        self.detector = HandDetector(maxHands=1)
        
        # Game state variables
        self.state = GameState.WAITING
        self.timer = 0
        self.initial_time = 0
        self.countdown_duration = 3
        self.scores = [0, 0]  # [AI, Player]
        self.round_history = []
        self.player_move = Move.NONE
        self.ai_move = Move.NONE
        self.round_result = ""
        
        # Load resources
        self.bg_image = cv2.imread("Resources1/BG.png")
        self.move_images = {
            Move.ROCK: cv2.imread('Resources1/1.png', cv2.IMREAD_UNCHANGED),
            Move.PAPER: cv2.imread('Resources1/2.png', cv2.IMREAD_UNCHANGED),
            Move.SCISSORS: cv2.imread('Resources1/3.png', cv2.IMREAD_UNCHANGED)
        }
        
        # Visual effects
        self.animation_frames = 0
        self.animation_max = 10
        self.winner_color = (0, 255, 0)  # Green for winner highlight
        
        # Load sound effects if pygame is available
        try:
            import pygame
            pygame.mixer.init()
            self.sounds = {
                "countdown": pygame.mixer.Sound("Resources1/countdown.wav"),
                "win": pygame.mixer.Sound("Resources1/win.wav"),
                "lose": pygame.mixer.Sound("Resources1/lose.wav"),
                "draw": pygame.mixer.Sound("Resources1/draw.wav")
            }
            self.sound_enabled = True
        except (ImportError, FileNotFoundError):
            self.sound_enabled = False
    
    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def get_ai_move(self):
        # Smart AI: Initially random, but after a few rounds, starts to detect patterns
        if len(self.round_history) < 3:
            return Move(random.randint(1, 3))
        
        # Check if player has patterns
        last_moves = [history[0] for history in self.round_history[-3:]]
        
        # If player used the same move twice in a row, counter their next likely move
        if last_moves[-1] == last_moves[-2]:
            # Choose the move that would beat their last move
            if last_moves[-1] == Move.ROCK:
                return Move.PAPER
            elif last_moves[-1] == Move.PAPER:
                return Move.SCISSORS
            elif last_moves[-1] == Move.SCISSORS:
                return Move.ROCK
        
        # Otherwise, choose randomly
        return Move(random.randint(1, 3))
    
    def determine_winner(self):
        if self.player_move == Move.NONE:
            self.scores[0] += 1  # AI wins if player made no valid move
            return "AI Wins! No valid move detected."
        
        if self.player_move == self.ai_move:
            return "Draw!"
        
        if self.player_move.beats(self.ai_move):
            self.scores[1] += 1
            return "Player Wins!"
        else:
            self.scores[0] += 1
            return "AI Wins!"
    
    def handle_key_events(self):
        key = cv2.waitKey(1)
        
        if key == ord('s'):
            self.state = GameState.COUNTDOWN
            self.initial_time = time.time()
            if self.sound_enabled:
                self.play_sound("countdown")
                
        elif key == ord('r'):
            self.scores = [0, 0]
            self.round_history = []
            
        elif key == 27:  # ESC key
            return False
            
        return True
    
    def process_hand_input(self):
        success, img = self.cap.read()
        if not success:
            return None
            
        # Resize and crop for better display
        img_scaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
        img_scaled = img_scaled[:, 80:480]
        
        # Find hands and determine player move
        hands, img_scaled = self.detector.findHands(img_scaled)
        
        if self.state == GameState.COUNTDOWN and time.time() - self.initial_time > self.countdown_duration:
            if hands:
                hand = hands[0]
                fingers = self.detector.fingersUp(hand)
                self.player_move = Move.from_fingers(fingers)
            else:
                self.player_move = Move.NONE
                
            self.ai_move = self.get_ai_move()
            self.round_result = self.determine_winner()
            self.round_history.append((self.player_move, self.ai_move))
            self.state = GameState.SHOW_RESULT
            self.animation_frames = 0
            
            # Play appropriate sound
            if "Draw" in self.round_result:
                self.play_sound("draw")
            elif "Player Wins" in self.round_result:
                self.play_sound("win")
            else:
                self.play_sound("lose")
                
        return img_scaled
    
    def draw_game_interface(self, img_scaled):
        # Start with background
        result_image = self.bg_image.copy()
        
        # Place the webcam feed
        result_image[234:654, 795:1195] = img_scaled
        
        # Draw scores
        cv2.putText(result_image, str(self.scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(result_image, str(self.scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        
        # Draw game state specific elements
        if self.state == GameState.WAITING:
            cv2.putText(result_image, "Press 'S' to start", (480, 435), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            cv2.putText(result_image, "Press 'R' to reset", (480, 465), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            
        elif self.state == GameState.COUNTDOWN:
            elapsed = time.time() - self.initial_time
            countdown = self.countdown_duration - int(elapsed)
            cv2.putText(result_image, str(countdown), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            
            # Visual prompt for player
            prompt_text = "Show your move!"
            cv2.putText(result_image, prompt_text, (800, 680), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
            
        elif self.state == GameState.SHOW_RESULT:
            # Show AI move with animation effect
            if self.animation_frames < self.animation_max:
                scale = 0.8 + 0.2 * (self.animation_frames / self.animation_max)
                self.animation_frames += 1
            else:
                scale = 1.0
                # Reset to waiting state after showing result for a while
                if time.time() - self.initial_time > self.countdown_duration + 3:
                    self.state = GameState.WAITING
            
            # Apply AI move image with scaling effect
            ai_img = cv2.resize(self.move_images[self.ai_move], (0, 0), None, scale, scale)
            result_image = cvzone.overlayPNG(result_image, ai_img, (149, 310))
            
            # Show player's move name
            player_move_text = f"You chose: {self.player_move.name}"
            cv2.putText(result_image, player_move_text, (820, 620), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
            
            # Show round result with winner highlight
            if "Player Wins" in self.round_result:
                highlight_color = self.winner_color
                highlight_box = (795, 234, 1195, 654)  # Player camera area
            elif "AI Wins" in self.round_result:
                highlight_color = self.winner_color
                highlight_box = (149, 310, 349, 510)  # AI move area
            else:
                highlight_color = (255, 255, 0)  # Yellow for draw
                highlight_box = None
            
            # Draw winner highlight
            if highlight_box:
                cv2.rectangle(result_image, (highlight_box[0], highlight_box[1]), 
                             (highlight_box[2], highlight_box[3]), highlight_color, 3)
            
            # Show result text
            cv2.putText(result_image, self.round_result, (530, 680), 
                       cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        
        return result_image
    
    def run(self):
        while True:
            # Process hand input
            img_scaled = self.process_hand_input()
            if img_scaled is None:
                break
                
            # Draw game interface
            result_image = self.draw_game_interface(img_scaled)
            
            # Display result
            cv2.imshow("Rock Paper Scissors Game", result_image)
            
            # Handle key events
            if not self.handle_key_events():
                break
                
        self.cap.release()
        cv2.destroyAllWindows()

# Run the game
if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()