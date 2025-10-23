import random

choices = ["rock", "paper", "scissors"]
user = input("Choose rock, paper, or scissors: ").lower()
comp = random.choice(choices)

print(f"You chose {user}, computer chose {comp}.")

if user == comp:
    print("It's a tie!")
elif (user == "rock" and comp == "scissors") or \
     (user == "scissors" and comp == "paper") or \
     (user == "paper" and comp == "rock"):
    print("You win!")
else:
    print("You lose!")

