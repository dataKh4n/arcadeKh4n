score = 0

questions = {
    "What is the capital of France? ": "paris",
    "What is 5 + 7? ": "12",
    "What color are bananas? ": "yellow"
}

for q, a in questions.items():
    ans = input(q).lower()
    if ans == a:
        print("✅ Correct!")
        score += 1
    else:
        print("❌ Wrong!")
print(f"Your score: {score}/{len(questions)}")

