Full level-01-guessing-game/README.md
markdown
# 🎯 Number Guessing Game

A terminal game where you try to guess a random number between **1 and 100**
in **7 attempts or fewer**. After each guess you get a hint — *too high* or
*too low* — until you win, run out of attempts, or quit.

Built as **Level 1** of my [Python Journey](../README.md).

---

## ✨ Features

- Random secret number (1–100) generated per round
- Hint after each guess: `too high` / `too low`
- **7-attempt cap** — win or lose, the round ends
- Input validation — no crash on letters, empty input, or out-of-range values
- Type `q` at any time to quit a round
- Replay after each round without restarting the script

---

## 🚀 How to run

Requires **Python 3.10+**. No dependencies — standard library only.

```bash
cd level-01-guessing-game
python main.py
🎮 Example session
text
============================================
   🎯 Guess the Number (1–100)
   You have 7 attempts.
   Type 'q' at any time to quit the round.
============================================
Attempt 1/7 → 50
   too high
Attempt 2/7 → 25
   too low
Attempt 3/7 → 37
   too high
Attempt 4/7 → 33
🎉 Correct! You guessed it in 4 attempt(s).
--------------------------------------------
Play again? (y/n): n
👋 Thanks for playing!
Losing looks like this:

text
Attempt 7/7 → 50
   too high
--------------------------------------------
😔 You lost. The number was 23.
   You made 7/7 attempt(s).
--------------------------------------------
```
## 🔧 How it works

The whole game lives in one file, main.py, split into three layers:

Layer	Functions	Role
Utilities	random_number, validate_input	Pure helpers
Game logic	check_guess	Pure — compares guess to secret
Presentation	print_intro, get_guess, print_result, ask_replay	All I/O
Core	play_round, main	Orchestrates a round + replay loop
The pure functions (check_guess, validate_input) contain no print() or
input() calls — they'll be easy to unit-test when we get to Level 8.

## 📚 What I learned

Pure functions are gold. check_guess(guess, secret) returns
"correct" / "too high" / "too low" with zero side effects — no
printing, no input, no state. Easy to reason about, easy to reuse.

Validate at the boundary. All user input goes through
validate_input() + get_guess(), so the rest of the code only ever
sees valid integers. The game has a single crash-free entry point for input.

Loop guards beat manual breaks. while attempts < MAX_ATTEMPTS plus
a post-loop print_result(reason="exhausted") is cleaner than checking
the limit inside the loop on every iteration — the exit condition lives
in one place.

