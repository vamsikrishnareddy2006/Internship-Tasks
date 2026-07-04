# Number Guessing Game

import random

def check_guess(secret, guess):
    if guess == secret:
        return "Correct! 🎉"
    elif guess < secret:
        return "Too low! Try higher."
    else:
        return "Too high! Try lower."

# Generate a random number between 1 and 10
secret = random.randint(1, 10)

print("Welcome to the Number Guessing Game!")
print("Guess the number between 1 and 10.")
print("You have 3 attempts.\n")

for attempt in range(1, 4):
    guess = int(input(f"Attempt {attempt}: Enter your guess: "))
    result = check_guess(secret, guess)
    print(result)

    if guess == secret:
        print("Congratulations! You won! 🎉")
        break
else:
    print("\nGame Over!")
    print("The correct number was:", secret)