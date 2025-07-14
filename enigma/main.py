import sys
import argparse

from rotor import Rotor
from plugboard import plugboard
from database import init_db, add_entry, close_db

DB_PATH = "database.db"

def interractive():
    # Initialize Database
    database = init_db()
    #Testing Rotor Encryption
    message = input("Enter the message to encrypt: ")

    # Plugboard
    swap1 = input("What letter would you like to swap? ")
    swap2 = input(f'What letter would you like to swap {swap1} with? ')
    pbencrypted = plugboard(message, swap1, swap2)
    print(pbencrypted)

    # Rotor
    offset = int(input("Enter the rotor offset (1-25): "))
    print(f"{offset}")
    rotor = Rotor(offset)
    encrypted = rotor.encrypt(pbencrypted)
    print(f"Original : {message}")
    print(f"Encrypted: {encrypted}")
    
    # Database Entry
    crn = add_entry(database, message, encrypted)
    print(f"Saved entry CRN={crn}")
    close_db(database)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ELEC 3225 Enigma machine"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["run", "test"],
        default="run",
        help="'run' for interractive mode, 'test' to run unit tests",
    )
    args = parser.parse_args()

    if args.command == "test":
        import tests
        tests.run_tests()
    else:
        interractive()