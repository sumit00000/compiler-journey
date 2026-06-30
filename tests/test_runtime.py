import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.runtime import run

env = None

programs = [
    "LET x = 10;",
    "x + 5;",
    "LET y = x * 2;",
    "y + 1;",
    "-5 + 20;",
]

for program in programs:
    result, env = run(program, env)
    print(f"{program} -> {result}")