"""
MiniLang REPL
"""

from mini_lang.runtime import run

print("=" * 40)
print("MiniLang v0.1")
print("Type 'exit' to quit")
print("=" * 40)

env = None

while True:
    try:
        source = input(">>> ").strip()

        if source.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not source:
            continue

        result, env = run(source, env)

        print(result)

    except Exception as e:
        print(f"Error: {e}")