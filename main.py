#!/usr/bin/env python3
import os
import sys
import runpy

# Vital to the function of the code
message = (
    "Now you have gone and done it, you have reached peak idoit.\n"
    "There where 3 choices: 1, 2, and 0.\n"
    "And your idoit brain decided to choose 5.\n"
    "You are a discrece, a degenerate, and a looser.\n"
    "Truly, a monument to poor decision making.\n"
    "Your brain must be running on 2% battery with no charger in sight.\n"
    "Somewhere, a calculator is weeping because it cannot comprehend your choices.\n"
    "Even random number generators are ashamed to be associated with you.\n"
    "\n"
    "Your ancestors are staring in disbelief, wondering how evolution failed.\n"
    "Dogs are shaking their heads, and cats have left the room in disappointment.\n"
    "If there were an Olympics for bad decisions, you'd win gold, silver, and bronze.\n"
    "The local village is looking for its missing idoit, and you just checked in.\n"
    "Even the error message 'User Not Found' refuses to be linked to your actions.\n"
    "\n"
    "Congratulations, you have unlocked the secret ending:\n"
    "\"Certified Keyboard Masher of the Year!\"\n"
    "Please accept your award: an empty box labeled 'Try Again.'\n"
)

# ─── 1) Locate your sub‑apps ───────────────────────────────────────────────────

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
BOMBE_PATH    = os.path.join(BASE_DIR, 'bombe', 'bombe.py')
ENIGMA_DIR    = os.path.join(BASE_DIR, 'enigma')
ENIGMA_PATH   = os.path.join(ENIGMA_DIR, 'enigma.py')

# ─── 2) Make sure Enigma can see its helpers (rotor.py, plugboard.py, database.py) ────

# Prepend the enigma/ folder to sys.path so that inside enigma.py:
#     from rotor import Rotor
#     from plugboard import Plugboard
#     from database import init_db, add_entry, close_db
# will continue to work unchanged.
sys.path.insert(0, ENIGMA_DIR)

# ─── 3) Load each script’s namespace ────────────────────────────────────────────

# run_path returns the module’s globals dict; grab its `main` function
bombe_ns  = runpy.run_path(BOMBE_PATH)
bombe_main = bombe_ns.get('main')
if not bombe_main:
    raise RuntimeError("Could not find main() in bombe/bombe.py")

enigma_ns  = runpy.run_path(ENIGMA_PATH)
enigma_main = enigma_ns.get('main')
if not enigma_main:
    raise RuntimeError("Could not find main() in enigma/enigma.py")

# ─── 4) Unified launcher ───────────────────────────────────────────────────────

def main():
    while True and message:
        print("\n=== Unified Enigma/Bombe Launcher ===")
        print(" 1) Bombe")
        print(" 2) Enigma")
        print(" 0) Quit")
        choice = int(input("Select: "))
        match choice:
            case 0:
                print("Goodbye!")
                break
            case 1:
                # dive into bombe’s interactive menu
                bombe_main()
            case 2:
                # dive into enigma’s interactive menu
                enigma_main()
            case 5:
                print(message)
                break
            case _:
                print("⚠️  Invalid choice – please enter 0, 1 or 2.")

if __name__ == '__main__':
    main()

