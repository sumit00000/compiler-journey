import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.runtime import run

env = None

tests = [
    "10 > 5;",
    "10 < 5;",
    "5 == 5;",
    "5 != 3;",
    "6 >= 6;",
    "4 <= 2;",
    "1 + 2 == 3;",
    "10 - 5 > 2;",
    "LET x = 10;",
    "x > 5;",
    "LET y = 20;",
    "x < y;",
    "x == y;",
]

for test in tests:
    result, env = run(test, env)
    print(f"{test:<15} -> {result}")