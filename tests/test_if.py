import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.runtime import run

env = None

programs = [
    """
    IF 10 > 5 THEN
        LET x = 100;
    ELSE
        LET x = 0;
    END;
    """,

    "x;",

    """
    IF 10 < 5 THEN
        LET y = 1;
    ELSE
        LET y = 2;
    END;
    """,

    "y;",
]

for program in programs:
    result, env = run(program, env)
    print(result)