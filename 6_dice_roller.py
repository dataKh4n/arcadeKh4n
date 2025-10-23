import random

while True:
    input("Press Enter to roll 🎲...")
    print("You rolled:", random.randint(1, 6))
    if input("Roll again? (y/n): ").lower() != "y":
        break

