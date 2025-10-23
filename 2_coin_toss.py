import random

print("🪙 Coin Toss Game")
choice = input("Heads or Tails? ").lower()
result = random.choice(["heads", "tails"])
print(f"It’s {result}! You {'win' if choice == result else 'lose'}!")

