import pygame
import random

pygame.init()

# Load sounds with error handling
try:
    win_sound = pygame.mixer.Sound("win.wav")
    lose_sound = pygame.mixer.Sound("lose.wav")
    wrong_guess_sound = pygame.mixer.Sound("wrong.wav")
    correct_guess_sound = pygame.mixer.Sound("correct.wav")
    hint_sound = pygame.mixer.Sound("hint.wav")
    pygame.mixer.music.load("background.wav")
    pygame.mixer.music.play(1)  # Loop background music
except pygame.error:
    print("Warning: Some sound files are missing. Sounds will be disabled.")
    win_sound = lose_sound = wrong_guess_sound = correct_guess_sound = hint_sound = None

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

# Word categories
WORDS = {
    "Easy": ["CAT", "DOG", "SUN", "MOON", "TREE", "FISH", "BOOK", "BALL", "LAMP", "BIRD"],
    "Medium": ["PYTHON", "HANGMAN", "COMPUTER", "PROGRAM", "KEYBOARD", "MONITOR", "LAPTOP", "PRINTER"],
    "Hard": ["ALGORITHM", "DEVELOPER", "JAVASCRIPT", "NEURALNET", "DATABASE", "FUNCTION", "RECURSION"]
}

# Score tracking
score = {"Wins": 0, "Losses": 0}

# Load score from file
def load_score():
    try:
        with open("score.txt", "r") as file:
            wins, losses = map(int, file.read().split())
            score["Wins"] = wins
            score["Losses"] = losses
    except FileNotFoundError:
        pass

# Save score to file
def save_score():
    with open("score.txt", "w") as file:
        file.write(f"{score['Wins']} {score['Losses']}")

# Draw gallows
def draw_gallows():
    pygame.draw.line(screen, BLACK, (150, 400), (250, 400), 5)  # Base
    pygame.draw.line(screen, BLACK, (200, 400), (200, 150), 5)  # Pole
    pygame.draw.line(screen, BLACK, (200, 150), (150, 150), 5)  # Beam
    pygame.draw.line(screen, BLACK, (150, 150), (150, 180), 5)  # Rope

# Draw hangman
def draw_hangman(wrong_guesses):
    positions = [
        (pygame.draw.circle, (150, 200), 20, 3),  # Head
        (pygame.draw.line, (150, 220), (150, 280), 3),  # Body
        (pygame.draw.line, (150, 230), (120, 260), 3),  # Left arm
        (pygame.draw.line, (150, 230), (180, 260), 3),  # Right arm
        (pygame.draw.line, (150, 280), (120, 330), 3),  # Left leg
        (pygame.draw.line, (150, 280), (180, 330), 3)  # Right leg
    ]
    for i in range(wrong_guesses):
        part = positions[i]
        part[0](screen, BLACK, *part[1:])

# Draw keyboard
def draw_keyboard(used_letters):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_x, start_y = 50, 500
    spacing = 30
    for i, letter in enumerate(keys):
        color = RED if letter in used_letters else GRAY
        pygame.draw.rect(screen, color, (start_x + (i % 13) * spacing, start_y + (i // 13) * 50, 25, 25))
        text = small_font.render(letter, True, BLACK)
        screen.blit(text, (start_x + (i % 13) * spacing + 5, start_y + (i // 13) * 50 + 5))

# Choose difficulty
#def choose_difficulty():
   # screen.fill(WHITE)
    #text = font.render("Choose Difficulty: 1-Easy, 2-Medium, 3-Hard", True, BLACK)
    #screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    #pygame.display.flip()
def choose_difficulty():
    screen.fill(WHITE)
    title_text = font.render("Select Difficulty", True, BLACK)
    easy_text = small_font.render("1 - Easy", True, GREEN)
    medium_text = small_font.render("2 - Medium", True, YELLOW)
    hard_text = small_font.render("3 - Hard", True, RED)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 200))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 250))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 300))
    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "1":
                    return "Easy"
                elif event.unicode == "2":
                    return "Medium"
                elif event.unicode == "3":
                    return "Hard"

# Confirm quit
def confirm_quit():
    screen.fill(WHITE)
    text = font.render("Are you sure you want to quit? (Y/N)", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.unicode.lower() == 'y':
                    return True
                elif event.unicode.lower() == 'n':
                    return False

# Main game loop
def main_game(difficulty):
    global score
    word = random.choice(WORDS[difficulty])
    MAX_GUESSES = {"Easy": 6, "Medium": 6, "Hard": 6}[difficulty]
    displayed_word = ["_" for _ in word]
    used_letters = set()
    wrong_guesses = 0
    hints_used = 0
    revealed_letters = set()

    running = True
    while running:
        screen.fill(WHITE)
        draw_gallows()
        draw_hangman(wrong_guesses)
        draw_keyboard(used_letters)

        display_text = font.render(" ".join(displayed_word), True, BLACK)
        screen.blit(display_text, (WIDTH // 2 - display_text.get_width() // 2, HEIGHT // 2 - 50))

        used_text = small_font.render("Used: " + " ".join(sorted(used_letters)), True, RED)
        screen.blit(used_text, (20, 20))

        remaining_guesses_text = small_font.render(f"Remaining Guesses: {MAX_GUESSES - wrong_guesses}", True, GREEN)
        screen.blit(remaining_guesses_text, (20, 50))

        hint_text = small_font.render(f"Press 0 for hint ({2 - hints_used} left)", True, BLUE)
        screen.blit(hint_text, (20, 80))

        if "_" not in displayed_word:
            if win_sound:
                win_sound.play()
            score["Wins"] += 1
            result_text = font.render("You Win!", True, YELLOW)
        elif wrong_guesses >= MAX_GUESSES:
            if lose_sound:
                lose_sound.play()
            score["Losses"] += 1
            result_text = font.render(f"You Lose! Word: {word}", True, RED)
        else:
            result_text = None

        if result_text:
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 50))
            restart_text = small_font.render("Press R to restart or Q to quit", True, BLACK)
            continue_text1 = small_font.render("Press ", True, BLACK)
            continue_text2 = small_font.render("R", True, GREEN)
            continue_text3 = small_font.render(" to continue or ", True, BLACK)
            continue_text4 = small_font.render("Q", True, RED)
            continue_text5 = small_font.render(" to exit", True, BLACK)


            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

        score_text = small_font.render(f"Wins: {score['Wins']}  Losses: {score['Losses']}", True, BLACK)
        screen.blit(score_text, (WIDTH - 350, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if result_text:
                    if event.unicode.lower() == 'r':
                        return True
                    elif event.unicode.lower() == 'q':
                        if confirm_quit():
                            return False
                elif event.unicode.isalpha():
                    letter = event.unicode.upper()
                    if letter not in used_letters:
                        used_letters.add(letter)
                        if letter in word:
                            if correct_guess_sound:
                                correct_guess_sound.play()
                            for i, char in enumerate(word):
                                if char == letter:
                                    displayed_word[i] = letter
                        else:
                            if wrong_guess_sound:
                                wrong_guess_sound.play()
                            wrong_guesses += 1
                elif event.unicode == "0" and hints_used < 2:
                    hints_used += 1
                    if hint_sound:
                        hint_sound.play()
                    available_letters = [c for c in word if c not in displayed_word and c not in used_letters and c not in revealed_letters]
                    if available_letters:
                        revealed_letter = random.choice(available_letters)
                        revealed_letters.add(revealed_letter)
                        for i, char in enumerate(word):
                            if char == revealed_letter:
                                displayed_word[i] = char

# Main program
load_score()
while True:
    difficulty = choose_difficulty()
    if difficulty is None:
        break
    if not main_game(difficulty):
        break
save_score()
pygame.quit()
