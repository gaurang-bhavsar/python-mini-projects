import random

def number_guessing_game():
    print("🎲 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100...")

    # Generate random number
    number_to_guess = random.randint(1, 100)

    # Number of attempts
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter your guess: "))
        except ValueError:
            print("❌ Please enter a valid number!")
            continue

        attempts += 1

        if guess < number_to_guess:
            print("📉 Too low! Try a higher number.")
        elif guess > number_to_guess:
            print("📈 Too high! Try a lower number.")
        else:
            print(f"🎉 Congratulations! You guessed it in {attempts} attempts!")
            break
    else:
        print(f"\n😞 You've used all {max_attempts} attempts.")
        print(f"The number was: {number_to_guess}")

    print("\nThanks for playing!")

# Run the game
if __name__ == "__main__":
    number_guessing_game()
