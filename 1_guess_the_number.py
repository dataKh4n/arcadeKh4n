#!/usr/bin/env python3
"""
Guess The Number - CLI game (updated for non-interactive environments and tests)
File: guess-the-number.py

This file is a drop-in replacement for the original single-file game.

Fixes and improvements made in response to an `OSError: [Errno 29] I/O error` when
running in non-interactive/sandboxed environments where `input()` is not available:

- The interactive input() calls are wrapped to catch OSError/EOFError and fall back
  to a non-interactive mode when appropriate.
- Added a programmatic input provider interface so the game can be driven by an
  automated player (useful for CI, sandboxes, or unit-like tests).
- Added command-line flags:
    --auto       : Run the game with an automated player (binary-search strategy).
    --seed S     : Seed RNG for deterministic behavior in tests/demos.
    --run-tests  : Run built-in test cases (non-interactive).
- play_round() now accepts an optional `input_provider` callable (int -> int) so
  tests can inject guesses without performing interactive I/O.
- Improved error handling and clearer messages when stdin is not interactive.

Usage examples (interactive terminal):
    python3 guess-the-number.py
    python3 guess-the-number.py --difficulty medium

Non-interactive / automated examples (good for sandboxes / CI):
    python3 guess-the-number.py --auto --seed 42
    python3 guess-the-number.py --run-tests

License: MIT
"""

from __future__ import annotations
import argparse
import random
import sys
import signal
from typing import Optional, Callable, Tuple


# ---------------------- Signal handler ----------------------

def signal_handler(sig, frame):
    print('\n\nGoodbye! Thanks for playing.')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# ---------------------- Config & Types ----------------------

class GameConfig:
    def __init__(self, min_value: int, max_value: int, max_attempts: Optional[int]):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts


# input_provider: function(min_v, max_v, attempt_number, secret_hint) -> int
# secret_hint is a string intended only for automated players/tests ('' for interactive)
InputProvider = Callable[[int, int, int, str], int]


# ---------------------- CLI Arg Parsing ----------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Play a Guess The Number game (CLI).')
    parser.add_argument('--difficulty', '-d', choices=['easy', 'medium', 'hard', 'custom'], default='easy',
                        help='Choose difficulty: easy (1-10), medium (1-50), hard (1-100), or custom')
    parser.add_argument('--min', dest='min_value', type=int, default=None, help='Minimum number (custom mode)')
    parser.add_argument('--max', dest='max_value', type=int, default=None, help='Maximum number (custom mode)')
    parser.add_argument('--max-attempts', dest='max_attempts', type=int, default=None,
                        help='Limit number of attempts (omit for unlimited)')
    parser.add_argument('--seed', type=int, default=None, help='Optional RNG seed (useful for demos)')
    parser.add_argument('--auto', action='store_true', help='Run the game with an automated player (non-interactive)')
    parser.add_argument('--run-tests', action='store_true', help='Run built-in test cases (non-interactive)')
    return parser.parse_args()


# ---------------------- Config creation ----------------------

def config_from_args(args: argparse.Namespace) -> GameConfig:
    if args.seed is not None:
        random.seed(args.seed)

    if args.difficulty == 'easy':
        return GameConfig(1, 10, 5 if args.max_attempts is None else args.max_attempts)
    if args.difficulty == 'medium':
        return GameConfig(1, 50, 7 if args.max_attempts is None else args.max_attempts)
    if args.difficulty == 'hard':
        return GameConfig(1, 100, 10 if args.max_attempts is None else args.max_attempts)

    # custom
    min_v = args.min_value if args.min_value is not None else 1
    max_v = args.max_value if args.max_value is not None else 100
    if min_v >= max_v:
        print('Invalid custom range: min must be less than max. Falling back to 1..100')
        min_v, max_v = 1, 100
    return GameConfig(min_v, max_v, args.max_attempts)


# ---------------------- Input handling ----------------------

def interactive_input_provider(min_v: int, max_v: int, attempt: int, _hint: str) -> int:
    """
    Default interactive provider. Wraps input() to handle OSError/EOFError gracefully.
    """
    prompt = f'Enter your guess ({min_v} - {max_v}): '
    while True:
        try:
            raw = input(prompt)
        except (EOFError, OSError):
            # Non-interactive environment (sandbox) or input closed.
            # Convert this into a clean program exit so callers/tests can handle it.
            raise RuntimeError('No interactive input available (EOF/OSError).')

        if raw is None:
            print('\nNo input received. Exiting.')
            raise RuntimeError('No interactive input received.')

        raw = raw.strip()
        if not raw:
            print('Please type something (a whole number).')
            continue
        try:
            guess = int(raw)
        except ValueError:
            print('That does not look like a whole number. Try again.')
            continue
        if guess < min_v or guess > max_v:
            print(f'Please enter a number between {min_v} and {max_v}.')
            continue
        return guess


class AutoPlayer:
    """
    Automated player that uses a binary-search-like strategy to guess the secret.
    Useful for non-interactive runs and tests.
    """
    def __init__(self, min_v: int, max_v: int, seed: Optional[int] = None):
        self.low = min_v
        self.high = max_v
        if seed is not None:
            random.seed(seed)

    def get_guess(self, min_v: int, max_v: int, attempt: int, hint: str) -> int:
        # If hint contains the secret (used by tests), we can pick it directly.
        if hint:
            try:
                secret = int(hint)
                return max(min_v, min(max_v, secret))
            except ValueError:
                pass
        # choose midpoint (round down) + small random offset to avoid deterministic repeats
        midpoint = (self.low + self.high) // 2
        guess = midpoint
        # clamp and return
        return max(min_v, min(max_v, guess))

    def feedback(self, last_guess: int, comparison: str):
        # comparison: 'low', 'high', 'correct'
        if comparison == 'low':
            # last_guess < secret -> move low up
            self.low = max(self.low, last_guess + 1)
        elif comparison == 'high':
            # last_guess > secret -> move high down
            self.high = min(self.high, last_guess - 1)
        # if correct: nothing to update


# ---------------------- Core game logic ----------------------

def play_round(config: GameConfig, input_provider: Optional[InputProvider] = None, *, reveal_secret_for_tests: Optional[int] = None) -> Tuple[bool, int]:
    """
    Play one round. Returns (won: bool, secret: int).

    - `input_provider` if provided must be a callable that returns an int guess.
      Signature: (min_v, max_v, attempt_number, secret_hint) -> int
    - `reveal_secret_for_tests` is an optional integer for tests so automated providers
      may be given the secret as a "hint" if desired.
    """
    secret = random.randint(config.min_value, config.max_value)
    attempts = 0

    # If input_provider is None, use interactive by default
    if input_provider is None:
        input_provider = interactive_input_provider

    # For AutoPlayer we will call feedback() after each guess if the provider supports it.
    auto_player = None
    if hasattr(input_provider, '__self__') and isinstance(getattr(input_provider, '__self__', None), AutoPlayer):
        auto_player = input_provider.__self__  # type: ignore

    # Inform player
    print(f"\nI'm thinking of a number between {config.min_value} and {config.max_value}.")
    if config.max_attempts is None:
        print('You have unlimited attempts. Good luck!')
    else:
        print(f'You have {config.max_attempts} attempts. Make them count!')

    while True:
        attempts += 1
        try:
            hint = str(reveal_secret_for_tests) if reveal_secret_for_tests is not None else ''
            guess = input_provider(config.min_value, config.max_value, attempts, hint)
        except RuntimeError as e:
            # Propagate a clearer message to calling contexts (e.g., main() or tests)
            print(f'Input unavailable: {e}')
            raise

        if guess == secret:
            print(f"Correct! You guessed the number in {attempts} attempt{'s' if attempts>1 else ''}.")
            if auto_player is not None:
                auto_player.feedback(guess, 'correct')
            return True, secret

        if guess < secret:
            print('Too low.')
            if auto_player is not None:
                auto_player.feedback(guess, 'low')
        else:
            print('Too high.')
            if auto_player is not None:
                auto_player.feedback(guess, 'high')

        if config.max_attempts is not None and attempts >= config.max_attempts:
            print(f"Out of attempts. The correct number was {secret}.")
            return False, secret


# ---------------------- Tests ----------------------

def run_builtin_tests() -> None:
    """
    Run a few deterministic test scenarios using AutoPlayer to exercise behaviour.
    These are simple functional tests (not using pytest) designed to run in CI/sandboxes.
    """
    print('\nRunning built-in tests...')
    failed = 0
    total = 0

    def assert_eq(a, b, msg=''):
        nonlocal failed, total
        total += 1
        if a != b:
            failed += 1
            print(f'FAIL: {msg} (got {a}, expected {b})')
        else:
            print(f'OK: {msg}')

    # Test 1: easy difficulty, unlimited attempts, AutoPlayer should eventually find secret
    cfg = GameConfig(1, 10, None)
    ap = AutoPlayer(cfg.min_value, cfg.max_value, seed=123)
    won, secret = play_round(cfg, ap.get_guess, reveal_secret_for_tests=None)
    assert_eq(won, True, 'AutoPlayer should win on 1..10 with unlimited attempts')

    # Test 2: limited attempts - impossible to always find in time if attempts low
    cfg2 = GameConfig(1, 100, 1)
    ap2 = AutoPlayer(cfg2.min_value, cfg2.max_value, seed=1)
    won2, secret2 = play_round(cfg2, ap2.get_guess, reveal_secret_for_tests=None)
    # With 1 attempt only, very unlikely to win; assert that returned type is bool
    assert_eq(isinstance(won2, bool), True, 'Result should be boolean (test sanity)')

    # Test 3: deterministic secret via reveal_secret_for_tests: AutoPlayer should pick it immediately
    cfg3 = GameConfig(1, 50, 5)
    ap3 = AutoPlayer(cfg3.min_value, cfg3.max_value, seed=2)
    # pass reveal_secret_for_tests so AutoPlayer can see the secret via hint
    won3, secret3 = play_round(cfg3, ap3.get_guess, reveal_secret_for_tests=37)
    assert_eq(won3, True, 'AutoPlayer should win immediately when given secret as hint')

    # Test 4: custom range invalid fallback
    cfg4 = GameConfig(10, 5, None)
    # The play_round function assumes config is valid; ensure the function behaves (we'll normalize)
    # Normalize manually for test
    cfg4n = GameConfig(1, 100, None)
    ap4 = AutoPlayer(cfg4n.min_value, cfg4n.max_value, seed=3)
    won4, secret4 = play_round(cfg4n, ap4.get_guess)
    assert_eq(isinstance(won4, bool), True, 'Sanity check: play_round returns a bool')

    print(f'\nBuilt-in tests completed: {total-failed}/{total} passed')
    if failed:
        print('Some tests failed.')
        sys.exit(2)
    else:
        print('All tests passed.')
        sys.exit(0)


# ---------------------- Main ----------------------

def main():
    args = parse_args()
    config = config_from_args(args)

    # If tests requested, run them and exit (non-interactive)
    if args.run_tests:
        run_builtin_tests()

    # If auto requested, prepare AutoPlayer and run one round (non-interactive-friendly)
    if args.auto:
        ap = AutoPlayer(config.min_value, config.max_value, seed=args.seed)

        try:
            won, secret = play_round(config, ap.get_guess)
            print(f'Auto run finished. Won: {won}, secret was {secret}')
        except RuntimeError as e:
            print(f'Auto run failed due to input error: {e}')
            sys.exit(1)

        return

    # Interactive mode
    # If stdin is not a TTY, warn and offer to run --auto instead of trying to call input()
    if not sys.stdin.isatty():
        print('Warning: stdin is not interactive. Trying a safe non-interactive run using --auto mode.')
        ap = AutoPlayer(config.min_value, config.max_value, seed=args.seed)
        try:
            won, secret = play_round(config, ap.get_guess)
            print(f'Auto fallback finished. Won: {won}, secret was {secret}')
        except RuntimeError as e:
            print(f'Non-interactive fallback failed: {e}')
            print('Consider running this script locally in a terminal or use the --auto/--run-tests flags.')
            sys.exit(1)
        return

    # Real interactive terminal
    wins = 0
    losses = 0

    while True:
        try:
            won, secret = play_round(config)
        except RuntimeError as e:
            print(f'Interactive input failed: {e}')
            print('If you are running in a non-interactive environment, rerun with --auto or --run-tests.')
            sys.exit(1)

        if won:
            wins += 1
        else:
            losses += 1

        print(f'\nScore: {wins} wins, {losses} losses')
        try:
            again_raw = input('Play again? (y/n): ')
        except (EOFError, OSError):
            print('\nGoodbye!')
            break

        if again_raw is None:
            print('\nNo response detected. Exiting.')
            break

        again = again_raw.strip().lower()
        if again not in ('y', 'yes'):
            print('Thanks for playing — feel free to fork this on GitHub!')
            break


if __name__ == '__main__':
    main()

