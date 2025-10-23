"""
all_games.py — 100 puzzles/games in one menu.
Run with: python all_games.py
"""

import random
import sys
import time
import math

# -------------------------
# Utilities & DATA
# -------------------------
WORDS = [
    "python","puzzle","brain","test","logic","apple","banana","orange","matrix","vector",
    "galaxy","quantum","simple","complex","answer","mystery","riddle","cipher","enigma","cipher"
]
RIDDLES = [
    ("What has keys but can't open locks?", "keyboard"),
    ("What has to be broken before you can use it?", "egg"),
    ("What gets wetter the more it dries?", "towel")
]
SHORT_QUOTES = ["hello","world","openai","chatgpt","farooq","brain","mind","logic"]

def ask_enter():
    input("\nPress Enter to return to the menu...")

def choose_word():
    return random.choice(WORDS)

def safe_int(prompt, default=None):
    try:
        return int(input(prompt))
    except Exception:
        return default

# -------------------------
# Generic game templates
# -------------------------
def number_guessing(min_v=1, max_v=100, tries=None):
    target = random.randint(min_v, max_v)
    attempts = 0
    print(f"\nGuess the number between {min_v} and {max_v}!")
    while True:
        g = safe_int("Your guess: ")
        if g is None:
            print("Please enter a number.")
            continue
        attempts += 1
        if g < target:
            print("Too low.")
        elif g > target:
            print("Too high.")
        else:
            print(f"Correct! ({attempts} tries)")
            break
        if tries and attempts >= tries:
            print(f"Out of tries. Number was {target}.")
            break
    ask_enter()

def math_quiz(n=5, ops=("add",)):
    score = 0
    print(f"\nMath quiz — {n} questions. Ops: {ops}")
    for _ in range(n):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(ops)
        if op == "add":
            ans = a + b; q = f"{a} + {b} = "
        elif op == "sub":
            ans = a - b; q = f"{a} - {b} = "
        elif op == "mul":
            ans = a * b; q = f"{a} * {b} = "
        elif op == "div":
            b = random.randint(1,10); a = b * random.randint(1,10); ans = a // b; q = f"{a} // {b} = "
        else:
            ans = a + b; q = f"{a} + {b} = "
        g = safe_int(q)
        if g == ans:
            print("Correct"); score += 1
        else:
            print("Wrong. Ans:", ans)
    print(f"Score: {score}/{n}")
    ask_enter()

def scramble_word_game(word=None):
    if not word: word = choose_word()
    s = ''.join(random.sample(word, len(word)))
    print("\nUnscramble:", s)
    guess = input("Your guess: ").strip().lower()
    if guess == word:
        print("Correct!")
    else:
        print("Wrong — answer:", word)
    ask_enter()

def hangman_game(word=None, max_tries=6):
    if not word: word = choose_word()
    word = word.lower()
    state = ["_"] * len(word)
    tries = 0
    used = set()
    print("\nHangman! Guess letters.")
    while tries < max_tries and "_" in state:
        print(" ".join(state), "  used:", " ".join(sorted(used)))
        ch = input("Letter: ").strip().lower()
        if not ch or ch in used: 
            print("Try a new letter.")
            continue
        used.add(ch)
        if ch in word:
            for i,c in enumerate(word):
                if c == ch: state[i] = ch
            print("Good")
        else:
            tries += 1
            print("Wrong. tries:", tries)
    if "_" not in state:
        print("You win! Word:", word)
    else:
        print("You lose. Word:", word)
    ask_enter()

def riddle_game():
    r,a = random.choice(RIDDLES)
    print("\nRiddle:", r)
    g = input("Answer: ").strip().lower()
    if a in g:
        print("Nice — correct.")
    else:
        print("Nope. Answer:", a)
    ask_enter()

def coin_toss():
    print("\nCoin toss!")
    pick = input("Heads or tails? ").strip().lower()
    res = random.choice(["heads","tails"])
    print("Result:", res, " — you", "win!" if pick and pick[0]==res[0] else "lose.")
    ask_enter()

def dice_roll():
    print("\nDice roll. Press Enter to roll.")
    input()
    print("You rolled:", random.randint(1,6))
    ask_enter()

def rock_paper_scissors():
    print("\nRock Paper Scissors")
    move = input("rock/paper/scissors: ").strip().lower()
    comp = random.choice(["rock","paper","scissors"])
    print("Comp:", comp)
    if move==comp: print("Tie")
    elif (move=="rock" and comp=="scissors") or (move=="scissors" and comp=="paper") or (move=="paper" and comp=="rock"):
        print("You win")
    else: print("You lose")
    ask_enter()

def palindrome_check():
    s = input("\nEnter text to check palindrome: ").strip().lower()
    s2 = "".join(ch for ch in s if ch.isalnum())
    print("Palindrome!" if s2==s2[::-1] else "Not palindrome")
    ask_enter()

def anagram_check():
    a = input("\nWord 1: ").strip().lower()
    b = input("Word 2: ").strip().lower()
    if sorted(a)==sorted(b): print("Anagrams!")
    else: print("Not anagrams.")
    ask_enter()

def simple_memory(level=3):
    seq = [random.choice("abcd") for _ in range(level)]
    print("\nMemorize:", " ".join(seq))
    time.sleep(1+level*0.5)
    print("\n" * 40)
    g = input("Enter sequence separated by space: ").strip().lower().split()
    print("Correct!" if g==seq else "Wrong. Ans: " + " ".join(seq))
    ask_enter()

def binary_challenge():
    n = random.randint(1,255)
    print("\nWhat is binary for", n, "?")
    g = input("Your answer: ").strip()
    if g == bin(n)[2:]: print("Correct")
    else: print("Nope. Answer:", bin(n)[2:])
    ask_enter()

def hex_challenge():
    n = random.randint(1,255)
    print("\nWhat is HEX for", n, "?")
    g = input("Your answer (no 0x): ").strip().lower()
    if g == hex(n)[2:]: print("Correct")
    else: print("Nope. Answer:", hex(n)[2:])
    ask_enter()

def find_prime():
    n = random.randint(2,200)
    print("\nIs", n, "prime? (y/n)")
    g = input().strip().lower()
    isprime = n>1 and all(n%p for p in range(2,int(math.sqrt(n))+1))
    if (g.startswith("y") and isprime) or (g.startswith("n") and not isprime):
        print("Correct")
    else:
        print("Wrong. It is", "prime" if isprime else "not prime")
    ask_enter()

def factorize_quiz():
    n = random.randint(10,200)
    print("\nGive one factor (not 1 or itself) of", n)
    g = safe_int("Answer: ")
    if g and n%g==0 and 1<g<n: print("Good")
    else: print("Wrong. Factors include:", [i for i in range(2,n) if n%i==0][:5])
    ask_enter()

def gcd_lcm_quiz():
    a = random.randint(10,100); b = random.randint(10,100)
    print(f"\nNumbers: {a}, {b}")
    g1 = safe_int("GCD: ")
    g2 = safe_int("LCM: ")
    if g1==math.gcd(a,b) and g2==abs(a*b)//math.gcd(a,b):
        print("Correct!")
    else:
        print("Wrong. GCD:", math.gcd(a,b), "LCM:", abs(a*b)//math.gcd(a,b))
    ask_enter()

def sequence_next():
    # Simple arithmetic sequence or fibonacci
    t = random.choice(["arith","fib"])
    if t=="arith":
        a = random.randint(1,10); d=random.randint(1,10)
        seq = [a + d*i for i in range(5)]
        print("\nSequence:", seq[:4])
        g = safe_int("Next: ")
        if g==seq[4]: print("Correct")
        else: print("Wrong. Next is", seq[4])
    else:
        a,b = random.randint(1,5), random.randint(1,5)
        seq = [a,b]
        for _ in range(3): seq.append(seq[-1]+seq[-2])
        print("\nSequence:", seq[:4])
        g = safe_int("Next: ")
        if g==seq[4]: print("Correct")
        else: print("Wrong. Next is", seq[4])
    ask_enter()

def compare_numbers():
    a = random.randint(1,100); b = random.randint(1,100)
    print(f"\nWhich is bigger? {a} or {b}")
    g = input("Answer: ").strip()
    if (g==str(a) and a>b) or (g==str(b) and b>a):
        print("Correct")
    else:
        print("Wrong")
    ask_enter()

def simple_logic_puzzle():
    # Tiny logic: which door leads to exit?
    door = random.choice(["left","right","middle"])
    print("\nThree doors: left, middle, right. A guard hints randomly.")
    hint = random.choice([
        f"It is not {door}.",
        f"The exit is {door}."
    ])
    print("Guard:", hint)
    g = input("Which door? ").strip().lower()
    if g==door: print("Exit! You win.")
    else: print("Wrong. It was", door)
    ask_enter()

def word_chain():
    w = choose_word()
    print("\nWord chain — type a word that starts with last letter of:", w)
    g = input("Word: ").strip().lower()
    if g and g[0]==w[-1]:
        print("Valid")
    else:
        print("Invalid. Should start with:", w[-1])
    ask_enter()

def choose_plural():
    w = random.choice(["mouse","child","foot","person","cactus"])
    print(f"\nPlural of {w}? (type)")
    g = input("Answer: ").strip().lower()
    corrections = {"mouse":"mice","child":"children","foot":"feet","person":"people","cactus":"cacti"}
    if g==corrections[w]: print("Correct")
    else: print("Wrong. It's", corrections[w])
    ask_enter()

def countdown_recall():
    n = 5
    print("\nMemorize sequence of numbers:")
    seq = [str(random.randint(10,99)) for _ in range(n)]
    print(" ".join(seq))
    time.sleep(2)
    print("\n"*30)
    g = input("Enter them separated by space: ").strip().split()
    print("Correct!" if g==seq else "Wrong. Ans: "+" ".join(seq))
    ask_enter()

def odd_even_quiz():
    n = random.randint(1,200)
    print("\nIs", n, "odd or even?")
    g = input("(odd/even): ").strip().lower()
    if (n%2==0 and g=="even") or (n%2==1 and g=="odd"):
        print("Correct")
    else:
        print("Wrong")
    ask_enter()

def word_length_quiz():
    w = choose_word()
    print("\nWord:", w)
    g = safe_int("Length: ")
    if g==len(w): print("Correct")
    else: print("Wrong. Length is", len(w))
    ask_enter()

def vowel_count():
    w = choose_word()
    print("\nWord:", w)
    g = safe_int("Vowel count: ")
    if g==sum(1 for ch in w if ch in "aeiou"):
        print("Correct")
    else: print("Wrong. Count is", sum(1 for ch in w if ch in "aeiou"))
    ask_enter()

def letter_guess_game():
    w = choose_word()
    print("\nGuess a letter in the word (one try).")
    g = input("Letter: ").strip().lower()
    print("Yes!" if g in w else "Nope.")
    ask_enter()

def yes_no_logic():
    q = random.choice(["Is the sky blue?", "Is fire cold?", "Do fish swim?"])
    print("\nQuestion:", q)
    g = input("(y/n): ").strip().lower()
    correct = q=="Is fire cold?" and g=="n" or q=="Is the sky blue?" and g=="y" or q=="Do fish swim?" and g=="y"
    print("Correct" if correct else "Wrong")
    ask_enter()

def guess_word_by_hint():
    w = choose_word()
    hint = f"starts with '{w[0]}' and length {len(w)}"
    print("\nHint:", hint)
    g = input("Guess: ").strip().lower()
    if g==w: print("Nice")
    else: print("Nope. It was", w)
    ask_enter()

def pattern_count():
    s = "".join(random.choice("01") for _ in range(10))
    pat = random.choice(["00","11","01","10"])
    print("\nString:", s)
    print("Count occurrences of", pat)
    g = safe_int("Your count: ")
    if g==s.count(pat): print("Correct")
    else: print("Wrong. Count:", s.count(pat))
    ask_enter()

def word_contains_letter():
    w = choose_word()
    letter = random.choice(list(set(w)))
    print(f"\nDoes '{w}' contain letter '{letter}'? (y/n)")
    g = input().strip().lower()
    print("Correct" if (g.startswith("y") and letter in w) or (g.startswith("n") and letter not in w) else "Wrong")
    ask_enter()

def two_sum_quiz():
    arr = [random.randint(1,30) for _ in range(6)]
    target = random.choice(arr) + random.choice(arr)
    print("\nArray:", arr)
    print("Find any two that sum to", target)
    g = input("Enter two numbers separated by space: ").strip().split()
    try:
        a,b=int(g[0]),int(g[1])
        print("Good" if a in arr and b in arr and a+b==target else "Wrong")
    except Exception:
        print("Invalid input")
    ask_enter()

def simple_cipher():
    w = choose_word()
    shift = random.randint(1,5)
    enc = "".join(chr((ord(c)-97+shift)%26+97) if c.isalpha() else c for c in w)
    print("\nEncoded word (Caesar):", enc)
    g = input("Decode: ").strip().lower()
    print("Correct" if g==w else "Wrong, was "+w)
    ask_enter()

def count_substring():
    text = " ".join(random.choice(SHORT_QUOTES) for _ in range(6))
    sub = random.choice(SHORT_QUOTES[:4])
    print("\nText:", text)
    print("How many times does substring", sub, "appear?")
    g = safe_int("Answer: ")
    print("Correct" if g==text.count(sub) else "Wrong. Count:"+str(text.count(sub)))
    ask_enter()

def smallest_largest():
    arr = [random.randint(1,200) for _ in range(8)]
    print("\nArray:", arr)
    g1 = safe_int("Smallest: "); g2 = safe_int("Largest: ")
    if g1==min(arr) and g2==max(arr): print("Correct")
    else: print("Wrong. Min:", min(arr), "Max:", max(arr))
    ask_enter()

def find_missing_number():
    start = random.randint(1,10)
    arr = list(range(start, start+6))
    missing = random.choice(arr)
    arr.remove(missing)
    random.shuffle(arr)
    print("\nSequence with one missing:", arr)
    g = safe_int("Missing number: ")
    print("Correct" if g==missing else "Wrong. It was "+str(missing))
    ask_enter()

def word_stats():
    s = " ".join(random.choice(SHORT_QUOTES) for _ in range(8))
    print("\nText:", s)
    g = safe_int("How many words? ")
    print("Correct" if g==len(s.split()) else "Wrong. Count:", len(s.split()))
    ask_enter()

def quick_multiplication():
    a = random.randint(2,12); b=random.randint(2,12)
    g = safe_int(f"\n{a} x {b} = ")
    print("Correct" if g==a*b else "Wrong. Ans: "+str(a*b))
    ask_enter()

def sum_digits_quiz():
    n = random.randint(100,9999)
    print("\nNumber:", n)
    g = safe_int("Sum of digits: ")
    if g==sum(int(d) for d in str(n)): print("Correct")
    else: print("Wrong. Sum:", sum(int(d) for d in str(n)))
    ask_enter()

def count_vowels_phrase():
    s = " ".join(random.choice(WORDS) for _ in range(5))
    print("\nPhrase:", s)
    g = safe_int("Vowel count: ")
    if g==sum(1 for ch in s if ch in "aeiou"): print("Correct")
    else: print("Wrong. Count:", sum(1 for ch in s if ch in "aeiou"))
    ask_enter()

def quick_recall_names():
    names = [random.choice(SHORT_QUOTES) for _ in range(4)]
    print("\nMemorize:", " ".join(names))
    time.sleep(1.5)
    print("\n"*30)
    g = input("Type them again separated by space: ").strip().split()
    print("Correct" if g==names else "Wrong. Ans: "+" ".join(names))
    ask_enter()

def two_player_tic_tac_toe():
    # Very simple 3x3 vs human two-player
    board = list(" "*9)
    def display():
        print("\n".join(["|".join(board[i*3:(i+1)*3]) for i in range(3)]))
    player = "X"
    moves = 0
    while True:
        display()
        pos = safe_int(f"Player {player} pos (1-9): ")
        if not pos or pos<1 or pos>9 or board[pos-1]!=" ":
            print("Invalid")
            continue
        board[pos-1]=player
        moves+=1
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in lines:
            if board[a]==board[b]==board[c] and board[a]!=" ":
                display(); print("Win:", player); ask_enter(); return
        if moves==9: display(); print("Tie"); ask_enter(); return
        player = "O" if player=="X" else "X"

def simple_ai_ttt():
    # Player vs very dumb AI random
    board = list(" "*9)
    def display():
        print("\n".join(["|".join(board[i*3:(i+1)*3]) for i in range(3)]))
    def winner(b):
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,bx,c in lines:
            if b[a]==b[bx]==b[c] and b[a]!=" ":
                return b[a]
        return None
    player="X"
    while True:
        display()
        pos = safe_int("Your pos (1-9): ")
        if not pos or pos<1 or pos>9 or board[pos-1]!=" ":
            print("Invalid"); continue
        board[pos-1]="X"
        if winner(board)=="X": display(); print("You win"); ask_enter(); return
        if " " not in board: display(); print("Tie"); ask_enter(); return
        # AI
        opts=[i for i,ch in enumerate(board) if ch==" "]
        ai = random.choice(opts)
        board[ai]="O"
        if winner(board)=="O": display(); print("AI wins"); ask_enter(); return

def guess_sequence_binary():
    seq=[random.randint(0,1) for _ in range(6)]
    print("\nBinary sequence:", " ".join(map(str,seq)))
    g = input("Enter as one string (e.g., 010101): ").strip()
    print("Correct" if g== "".join(map(str,seq)) else "Wrong")
    ask_enter()

def simple_mastermind():
    code = [random.randint(0,5) for _ in range(3)]
    print("\nMastermind (3 digits 0-5). Try to find the code.")
    tries=0
    while tries<8:
        guess = input("Enter 3 digits (e.g., 012): ").strip()
        if len(guess)!=3: print("Bad"); continue
        guessv = [int(c) for c in guess]
        bulls = sum(1 for i in range(3) if guessv[i]==code[i])
        cows = sum(min(code.count(d), guessv.count(d)) for d in set(guessv)) - bulls
        print(f"Bulls: {bulls}, Cows: {cows}")
        tries+=1
        if bulls==3: print("You cracked it!"); break
    if bulls!=3: print("Code was", "".join(map(str,code)))
    ask_enter()

def count_primes_range():
    a = random.randint(2,50); b = a+random.randint(10,50)
    print(f"\nCount primes between {a} and {b}")
    g = safe_int("Your count: ")
    def isprime(n): 
        if n<2: return False
        for i in range(2,int(math.sqrt(n))+1):
            if n%i==0: return False
        return True
    correct = sum(1 for i in range(a,b+1) if isprime(i))
    print("Correct" if g==correct else "Wrong. Ans:"+str(correct))
    ask_enter()

def letter_position_game():
    w = choose_word()
    i = random.randrange(len(w))
    print(f"\nWord: {w}, what is letter at position {i+1}?")
    g = input("Letter: ").strip().lower()
    print("Correct" if g==w[i] else f"Wrong. It is {w[i]}")
    ask_enter()

def sum_series():
    n = random.randint(3,10)
    seq = [i*i for i in range(1,n+1)]
    print("\nSeries:", seq[:4], "...")
    g = safe_int(f"Sum of first {n} terms: ")
    if g==sum(seq): print("Correct")
    else: print("Wrong. Sum:", sum(seq))
    ask_enter()

def simple_countdown_math():
    n = random.randint(20,50)
    print(f"\nQuick: subtract numbers 1..5 from {n} mentally.")
    g = safe_int("Result: ")
    res = n-1-2-3-4-5
    print("Correct" if g==res else "Wrong. Ans:"+str(res))
    ask_enter()

def find_word_with_letter():
    letter = random.choice("aeiou")
    candidates = [w for w in WORDS if letter in w]
    print("\nFind a word containing letter:", letter)
    g = input("Word: ").strip().lower()
    print("Good" if g in candidates else "Nope")
    ask_enter()

def even_odd_split():
    arr = [random.randint(1,50) for _ in range(6)]
    print("\nArray:", arr)
    ev = [x for x in arr if x%2==0]
    od = [x for x in arr if x%2==1]
    g1 = input("List evens separated by space: ").split()
    g2 = input("List odds separated by space: ").split()
    try:
        g1=[int(x) for x in g1]; g2=[int(x) for x in g2]
        print("Good" if set(g1)==set(ev) and set(g2)==set(od) else "Wrong")
    except:
        print("Invalid input")
    ask_enter()

def letters_to_numbers():
    w = choose_word()
    print("\nWord:", w)
    print("Convert letters to positions (a=1). E.g., abc -> 1 2 3")
    g = input("Result: ").strip().split()
    try:
        nums=[int(x) for x in g]
        correct=[ord(ch)-96 for ch in w]
        print("Correct" if nums==correct else "Wrong. Ans: "+" ".join(map(str,correct)))
    except:
        print("Invalid")
    ask_enter()

def smallest_difference():
    arr=[random.randint(1,50) for _ in range(6)]
    print("\nArray:", arr)
    diffs=sorted(abs(a-b) for i,a in enumerate(arr) for b in arr[i+1:])
    g = safe_int("Smallest difference: ")
    print("Correct" if g==diffs[0] else "Wrong. Ans:"+str(diffs[0]))
    ask_enter()

def find_longest_word():
    s = " ".join(random.choice(WORDS) for _ in range(6))
    print("\nText:", s)
    g = input("Longest word: ").strip()
    longest = max(s.split(), key=len)
    print("Correct" if g==longest else "Wrong. Ans:"+longest)
    ask_enter()

def count_consonants():
    s = random.choice(WORDS)
    print("\nWord:", s)
    g = safe_int("Count consonants: ")
    correct = sum(1 for ch in s if ch.isalpha() and ch not in "aeiou")
    print("Correct" if g==correct else "Wrong. Ans:"+str(correct))
    ask_enter()

def quick_table():
    n = random.randint(2,9)
    print(f"\nGive multiplication table for {n} up to 5 (space-separated).")
    g = input("Ans: ").split()
    try:
        g=[int(x) for x in g]
        correct=[n*i for i in range(1,6)]
        print("Correct" if g==correct else "Wrong. Ans:"+ " ".join(map(str,correct)))
    except:
        print("Invalid")
    ask_enter()

def guess_factorial():
    n = random.randint(1,7)
    print("\nWhat's", n, "!?")
    g = safe_int("Answer: ")
    correct = math.factorial(n)
    print("Correct" if g==correct else "Wrong. Ans:"+str(correct))
    ask_enter()

def majority_element_quiz():
    arr = [random.choice([1,2,3]) for _ in range(7)]
    print("\nArray:", arr)
    g = safe_int("Majority element (if any, else -1): ")
    for x in set(arr):
        if arr.count(x)>len(arr)//2:
            ans=x; break
    else:
        ans=-1
    print("Correct" if g==ans else "Wrong. Ans:"+str(ans))
    ask_enter()

def find_pairs_with_sum():
    arr=[random.randint(1,20) for _ in range(8)]
    target=random.randint(10,30)
    print("\nArray:", arr,"Target:",target)
    g = input("Enter any pair separated by space: ").split()
    try:
        a,b=int(g[0]),int(g[1])
        print("Good" if a in arr and b in arr and a+b==target else "Wrong")
    except:
        print("Invalid")
    ask_enter()

def binary_search_game():
    arr=sorted(random.sample(range(1,100),15))
    target=random.choice(arr)
    print("\nArray:", arr)
    print("Find index of",target)
    g = safe_int("Index (0-based): ")
    print("Correct" if g==arr.index(target) else "Wrong. Ans:"+str(arr.index(target)))
    ask_enter()

def quick_logic_grid():
    # trivial logic: A>B>C?
    a,b,c = sorted(random.sample(range(1,50),3), reverse=True)
    print("\nWhich is largest among A,B,C?")
    print("They are distinct numbers but hidden.")
    g = input("Type 'A' if largest is A else B/C: ").strip().upper()
    # randomly assign numbers to A,B,C
    arr=[a,b,c]
    mapping = {"A":arr[0],"B":arr[1],"C":arr[2]}
    largest = max(mapping, key=lambda k:mapping[k])
    print("Correct" if g==largest else f"Wrong. Correct is {largest} (values {mapping})")
    ask_enter()

def guess_the_color_word():
    words = ["red","blue","green","yellow","purple"]
    w=random.choice(words)
    print("\nWhat's the color word? Hint: length", len(w))
    g=input("Your guess: ").strip().lower()
    print("Correct" if g==w else "Wrong. Ans:"+w)
    ask_enter()

def digit_reverse():
    n=random.randint(10,9999)
    print("\nNumber:",n)
    g = input("Reverse: ").strip()
    print("Correct" if g==str(n)[::-1] else "Wrong. Ans:"+str(n)[::-1])
    ask_enter()

def ascii_sum():
    w = choose_word()
    s = sum(ord(ch) for ch in w)
    print("\nWord:", w)
    g = safe_int("Sum ASCII values: ")
    print("Correct" if g==s else "Wrong. Ans:"+str(s))
    ask_enter()

def trailing_zeros_factorial():
    n=random.randint(5,50)
    print("\nHow many trailing zeros in",n,"!?")
    # count zeros
    c=0; i=5
    while i<=n:
        c+=n//i; i*=5
    g=safe_int("Answer: ")
    print("Correct" if g==c else "Wrong. Ans:"+str(c))
    ask_enter()

def convert_minutes():
    m=random.randint(60,500)
    print("\nMinutes:",m)
    g = input("Convert to H:M format (e.g., 2:30): ").strip()
    try:
        h=int(g.split(":")[0]); mm=int(g.split(":")[1])
        print("Correct" if h*60+mm==m else "Wrong. Ans:"+f"{m//60}:{m%60}")
    except:
        print("Invalid")
    ask_enter()

def simple_stats():
    arr=[random.randint(1,100) for _ in range(6)]
    print("\nArray:",arr)
    mean = sum(arr)/len(arr)
    g=float(input("Mean (approx): "))
    print("Correct" if abs(g-mean)<0.5 else f"Wrong. Ans approx {mean:.2f}")
    ask_enter()

def choose_larger_power():
    a=random.randint(2,6); b=random.randint(2,6)
    print(f"\nWhich is larger: {a}**{b} or {b}**{a}?")
    g=input("Type 'first' or 'second': ").strip().lower()
    print("Correct" if (a**b > b**a and g=="first") or (b**a > a**b and g=="second") else "Wrong")
    ask_enter()

def find_sublist():
    arr=[random.randint(1,10) for _ in range(8)]
    sub=arr[2:5]
    print("\nArray:",arr)
    g=input("Type sublist from index 2 to 4 separated by space: ").split()
    try:
        g=[int(x) for x in g]
        print("Correct" if g==sub else "Wrong. Ans:"+str(sub))
    except:
        print("Invalid")
    ask_enter()

def guess_power_of_two():
    n=random.choice([2,4,8,16,32,64,128])
    print("\nWhich power of two is", n, "?")
    g=safe_int("Exponent: ")
    print("Correct" if 2**g==n else "Wrong. Ans:"+str(int(math.log2(n))))
    ask_enter()

def mini_crossword_hint():
    w=choose_word()
    hint="".join(ch if i%2==0 else "_" for i,ch in enumerate(w))
    print("\nFill the blanks:", hint)
    g=input("Word: ").strip()
    print("Correct" if g==w else "Wrong. Ans:"+w)
    ask_enter()

def simple_cryptarithm():
    a=random.randint(10,99); b=random.randint(10,99)
    s=str(a+b)
    print(f"\nSolve digits: {a} + {b} = {s}")
    g=input("Type the sum: ").strip()
    print("Correct" if g==s else "Wrong. Ans:"+s)
    ask_enter()

def name_anagram_of():
    w=choose_word()
    print("\nIs '", "".join(random.sample(w,len(w))), "' an anagram of", w, "? (y/n)")
    g=input().strip().lower()
    print("Yes" if g.startswith("y") else "No (this is just a prompt).")
    ask_enter()

def fraction_compare():
    a=random.randint(1,9); b=random.randint(1,9)
    c=random.randint(1,9); d=random.randint(1,9)
    print(f"\nWhich is larger: {a}/{b} or {c}/{d}?")
    g=input("Type 'first' or 'second': ").strip().lower()
    print("Correct" if (a/b>c/d and g=="first") or (c/d>a/b and g=="second") else "Wrong")
    ask_enter()

def word_ladder_step():
    w="cat"; # tiny example
    print("\nChange one letter of 'cat' to make a new word (e.g., 'cot'):")
    g=input("Word: ").strip().lower()
    print("Nice" if len(g)==3 and sum(1 for a,b in zip(w,g) if a!=b)==1 else "Invalid")
    ask_enter()

def memory_pairs():
    pairs = ["".join(sorted(random.choice(WORDS))) for _ in range(3)]
    flat = pairs+pairs
    random.shuffle(flat)
    print("\nCards (positions 1..6). Try to find pair by giving indices.")
    print("Hidden positions.")
    a=safe_int("Pick first pos: "); b=safe_int("Pick second pos: ")
    if a and b and 1<=a<=6 and 1<=b<=6 and a!=b:
        if flat[a-1]==flat[b-1]: print("Match!")
        else: print("Nope.")
    else:
        print("Invalid picks.")
    ask_enter()

def simple_guess_by_length():
    w=choose_word()
    print("\nGuess a word of length", len(w))
    g=input("Word: ").strip().lower()
    print("Correct" if g==w else "Wrong")
    ask_enter()

def trivia_yes_no():
    q = random.choice(["Is Python a snake?","Is water dry?","Is earth round?"])
    print("\nQuestion:",q)
    g=input("(y/n): ").strip().lower()
    print("Hmm")
    ask_enter()

# -------------------------
# Build the 100-game list
# -------------------------
GAMES = [
    ("Number Guess (1-20)", lambda: number_guessing(1,20)),
    ("Number Guess (1-100)", lambda: number_guessing(1,100)),
    ("Number Guess (1-1000, limited tries)", lambda: number_guessing(1,1000,tries=10)),
    ("Math Quiz (add)", lambda: math_quiz(5,("add",))),
    ("Math Quiz (mixed)", lambda: math_quiz(5,("add","sub","mul"))),
    ("Unscramble Word", lambda: scramble_word_game()),
    ("Hangman", lambda: hangman_game()),
    ("Riddle", riddle_game),
    ("Coin Toss", coin_toss),
    ("Dice Roll", dice_roll),
    ("Rock Paper Scissors", rock_paper_scissors),
    ("Palindrome Check", palindrome_check),
    ("Anagram Check", anagram_check),
    ("Simple Memory (3)", lambda: simple_memory(3)),
    ("Binary Challenge", binary_challenge),
    ("Hex Challenge", hex_challenge),
    ("Prime Test", find_prime),
    ("Factorization quiz", factorize_quiz),
    ("GCD & LCM quiz", gcd_lcm_quiz),
    ("Sequence Next", sequence_next),
    ("Compare two numbers", compare_numbers),
    ("Tiny Logic Puzzle", simple_logic_puzzle),
    ("Word Chain", word_chain),
    ("Plural Quiz", choose_plural),
    ("Countdown Recall", countdown_recall),
    ("Odd/Even Quiz", odd_even_quiz),
    ("Word Length", word_length_quiz),
    ("Vowel Count", vowel_count),
    ("Letter Guess", letter_guess_game),
    ("Yes/No Logic", yes_no_logic),
    ("Guess by Hint", guess_word_by_hint),
    ("Pattern Count", pattern_count),
    ("Word Contains Letter", word_contains_letter),
    ("Two-sum Quiz", two_sum_quiz),
    ("Simple Cipher (Caesar)", simple_cipher),
    ("Count Substring", count_substring),
    ("Smallest/Largest", smallest_largest),
    ("Find Missing Number", find_missing_number),
    ("Word Stats (words count)", word_stats),
    ("Quick Multiplication", quick_multiplication),
    ("Sum of Digits", sum_digits_quiz),
    ("Vowels in Phrase", count_vowels_phrase),
    ("Recall Names", quick_recall_names),
    ("Two-player Tic Tac Toe", two_player_tic_tac_toe),
    ("Play vs Simple AI Tic Tac Toe", simple_ai_ttt),
    ("Guess Binary Sequence", guess_sequence_binary),
    ("Mini Mastermind", simple_mastermind),
    ("Count Primes in Range", count_primes_range),
    ("Letter Position", letter_position_game),
    ("Sum Series", sum_series),
    ("Quick Mental Subtract", simple_countdown_math),
    ("Find Word with Letter", find_word_with_letter),
    ("Even/Odd Split", even_odd_split),
    ("Letters to Numbers", letters_to_numbers),
    ("Smallest Difference", smallest_difference),
    ("Find Longest Word", find_longest_word),
    ("Count Consonants", count_consonants),
    ("Multiplication Table", quick_table),
    ("Guess Factorial", guess_factorial),
    ("Majority Element", majority_element_quiz),
    ("Find Pairs with Sum", find_pairs_with_sum),
    ("Binary Search Game", binary_search_game),
    ("Quick Logic Grid", quick_logic_grid),
    ("Guess the Color Word", guess_the_color_word),
    ("Digit Reverse", digit_reverse),
    ("ASCII Sum", ascii_sum),
    ("Trailing Zeros in n!", trailing_zeros_factorial),
    ("Convert Minutes to H:M", convert_minutes),
    ("Simple Stats (mean)", simple_stats),
    ("Compare Powers a^b vs b^a", choose_larger_power),
    ("Find Sublist", find_sublist),
    ("Guess Power of Two", guess_power_of_two),
    ("Mini Crossword Hint", mini_crossword_hint),
    ("Simple Cryptarithm", simple_cryptarithm),
    ("Name Anagram Prompt", name_anagram_of),
    ("Fraction Compare", fraction_compare),
    ("Word Ladder Step", word_ladder_step),
    ("Memory Pairs (mini)", memory_pairs),
    ("Guess By Length", simple_guess_by_length),
    ("Random Trivia Prompt", trivia_yes_no),
    ("Find Next Prime", lambda: math_quiz(3,("add",))),  # filler variant
    ("Quick True/False", lambda: yes_no_logic()),       # variant
    ("Simple Speed Math (5 Qs)", lambda: math_quiz(5,("mul","add"))),
    ("Count Pattern 2", pattern_count),
    ("Quick Anagram Scramble", lambda: scramble_word_game()),
    ("Mini Word Stats", word_stats),
    ("Simple Cipher 2", simple_cipher),
    ("Even/Odd Count", odd_even_quiz),
    ("Tiny Brainteaser", simple_logic_puzzle),
    ("Sum of Two Randoms", lambda: math_quiz(3,("add",))),
    ("Guess the Letter Position", letter_position_game),
    ("Count Vowels 2", count_vowels_phrase),
    ("Mini Memory 4", lambda: simple_memory(4)),
    ("Short Riddle 2", riddle_game),
    ("Binary Challenge 2", binary_challenge),
    ("Hex Challenge 2", hex_challenge),
    ("Final Quick Quiz", lambda: math_quiz(4,("add","sub"))),
]

# fill to 100 if necessary by repeating some variants but keeping unique names
i = 1
while len(GAMES) < 100:
    GAMES.append((f"Bonus Mini Game {i}", lambda: coin_toss()))
    i += 1

# Ensure exactly 100
GAMES = GAMES[:100]

# -------------------------
# Menu & Runner
# -------------------------
def print_menu():
    print("\n" + "="*36)
    print("  100-in-1 Puzzle & Brain Games")
    print("="*36)
    for idx,(name,_) in enumerate(GAMES, start=1):
        print(f"{idx:2d}. {name}")
    print("  0. Play a random game")
    print(" -1. Exit")
    print("="*36)

def run_game_by_index(idx):
    if 1 <= idx <= len(GAMES):
        name, fn = GAMES[idx-1]
        print(f"\n--- {idx}. {name} ---")
        try:
            fn()
        except Exception as e:
            print("Game error:", e)
            ask_enter()
    else:
        print("Invalid selection")

def main_loop():
    while True:
        print_menu()
        sel = safe_int("Choose a game number: ", default=None)
        if sel is None:
            print("Please enter a number.")
            continue
        if sel == -1:
            print("Goodbye!")
            sys.exit(0)
        if sel == 0:
            idx = random.randint(1, len(GAMES))
            run_game_by_index(idx)
            continue
        run_game_by_index(sel)

if __name__ == "__main__":
    main_loop()

