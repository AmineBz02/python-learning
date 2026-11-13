"""
Project:  Number Guessing Game
Level:    1 — Absolute Beginner (Syntax & Basics)
Author:   Amine Bouazzi
Date:     13/11/2026
Repo:     python-journey / level-01-guessing-game
"""
import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 7


# --- Utilities ---------------------------------------------------------------

def random_number() -> int:
    """Return a random integer in [MIN_NUMBER, MAX_NUMBER]."""
    return random.randint(MIN_NUMBER, MAX_NUMBER)
def validate_input(raw: str) -> int | None:
    """
    Parse and validate a raw input string.

    Returns:
        int   — if raw is a valid integer in [MIN_NUMBER, MAX_NUMBER]
        None  — otherwise (caller decides what message to show)
    """
    raw = raw.strip()
    if not raw.isdigit():
        return None                # handles '', 'abc', '-5', '3.14', '1e3'
    value = int(raw)
    if value < MIN_NUMBER or value > MAX_NUMBER:
        return None
    return value


# --- Game logic --------------------------------------------------------------

def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret.

    Returns:
        "correct"   — guess equals secret
        "too high"  — guess > secret
        "too low"   — guess < secret
    """
    if guess == secret:
        return "correct"
    if guess > secret:
        return "too high"
    return "too low"


# --- Presentation ------------------------------------------------------------

def print_intro() -> None:
    """Print the game banner and short rules."""
    print("=" * 44)
    print("   🎯 Guess the Number (1–100)")
    print("   I'm thinking of a number between 1 and 100.")
    print("   Type your guess and I'll tell you if it's high or low.")
    print("=" * 44)
def get_guess(attempt: int, max_attempts: int | None = None) -> int | None:
    """
    Prompt until a valid guess is received, or the player quits with 'q'.

    Returns:
        int   — a valid guess in [MIN_NUMBER, MAX_NUMBER]
        None  — player typed 'q' (or 'Q') to quit
    """
    prompt = f"Attempt {attempt}"
    if max_attempts is not None:
        prompt += f"/{max_attempts}"
    prompt += " → "

    while True:
        raw = input(prompt)
        if raw.strip().lower() == "q":
            return None
        guess = validate_input(raw)
        if guess is not None:
            return guess
        # figure out which message to show
        if raw.strip().isdigit():
            print(f"  ⚠️  Enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
        else:
            print("  ⚠️  Please enter a number.")
def print_result(attempts: int, won: bool, secret: int,
                 best: int | None = None,
                 reason: str = "exhausted") -> None:
    """
    Print the outcome of a round.

    Args:
        attempts — number of valid guesses made
        won      — True if the player guessed correctly
        secret   — the secret number (revealed on loss/quit)
        best     — best score this session, or None if not tracked yet
        reason   — "exhausted" | "quit" (only used when won is False)
    """
    print("-" * 44)
    if won:
        print(f"🎉 Correct! You guessed it in {attempts} attempt(s).")
        if best is not None and attempts == best:
            print(f"   🥇 New best score: {best} attempt(s)!")
    else:
        if reason == "quit":
            print(f"👋 You quit. The number was {secret}.")
        else:
            print(f"😔 You lost. The number was {secret}.")
        print(f"   You made {attempts}/{MAX_ATTEMPTS} attempt(s).")
    print("-" * 44)
def ask_replay() -> bool:
    """
    Ask the player whether to play another round.

    Returns:
        True  — player wants to play again (y / Y)
        False — player wants to quit (n / N)
    """
    while True:
        raw = input("Play again? (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  ⚠️  Please answer 'y' or 'n'.")
# --- Core --------------------------------------------------------------------

def play_round() -> tuple[bool, int]:
    """
    Play one full round.

    Returns:
        (won, attempts) — won is False if player quit or lost
    """
    secret = random_number()
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        guess = get_guess(attempts + 1, MAX_ATTEMPTS)

        if guess is None:  
            print_result(attempts, won=False, secret=secret)                   # player typed 'q'
            return (False, attempts)

        attempts += 1
        result = check_guess(guess, secret)

        if result == "correct":
            print_result(attempts, won=True, secret=secret)
            return (True, attempts)


        print(f"   {result}")
    # Fell out of loop → out of attempts
    print_result(attempts, won=False, secret=secret, reason="exhausted")
    return (False, attempts)

def main() -> None:
    """Entry point for the Number Guessing Game."""
    print_intro()
    while True:
        play_round()
        if not ask_replay():
            print("Thanks for playing! Goodbye.")
            return 
      



if __name__ == "__main__":
    main()