# 1_guess_the_number.py
# Integrated with highscores.py to save player scores.

import random
from highscores import add_score, get_top_scores

def play_guess():
    attempts_allowed = 5
    number = random.randint(1, 10)
    attempts = 0
    won = False

    print("I'm thinking of a number between 1 and 10.")
    print(f"You have {attempts_allowed} attempts. Make them count!")

    while attempts < attempts_allowed:
        try:
            guess = int(input('Enter your guess (1 - 10): ').strip())
        except ValueError:
            print('Please enter a number.')
            continue
        attempts += 1
        if guess < number:
            print('Too low.')
        elif guess > number:
            print('Too high.')
        else:
            print(f'Correct! You guessed the number in {attempts} attempts.')
            won = True
            break

    if not won:
        print(f"Out of attempts. The number was {number}.")

    # Simple scoring: higher score for fewer attempts; 0 if lost
    score = 0
    if won:
        score = max(0, (attempts_allowed - attempts + 1) * 100)

    print(f"Score: {score}")

    save = input('Save your score to leaderboard? (y/n): ').strip().lower()
    if save == 'y':
        player = input('Enter your name (will be shown on leaderboard): ').strip() or 'Player'
        add_score(player, score, 'guess_the_number')
        print('\nTop 5 for guess_the_number:')
        for e in get_top_scores(game='guess_the_number', limit=5):
            print(f"{e['player']:<12} {e['score']:>6}  {e['date']}")

    again = input('Play again? (y/n): ').strip().lower()
    return again == 'y'

if __name__ == '__main__':
    while play_guess():
        pass
    print('Thanks for playing — feel free to fork this on GitHub!')
