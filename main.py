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

from bombe.bombe import main as bombe_main
from enigma.enigma import main as enigma_main

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

