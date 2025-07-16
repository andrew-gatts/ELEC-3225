from rotor import Rotor
from plugboard import Plugboard
from database import init_db, add_entry, close_db, print_all_entries
import argparse

DB_PATH = "database.db"

def interractive():
    # Initialize Database
    database = init_db()
    #Testing Rotor Encryption
    message = input("Enter the message to encrypt: ")
    offset = int(input("Enter the rotor offset (1-25): "))
    print(f"{offset}")
    rotor = Rotor(offset)
    encrypted = rotor.encrypt(message)
    print(f"Original : {message}")
    print(f"Encrypted: {encrypted}")


    plugboard1 = Plugboard()
    plugboard1.swap()

    crn = add_entry(database, message, encrypted)
    print(f"Saved entry CRN={crn}")
    close_db(database)

def print_db():
    database = init_db()
    for row in print_all_entries(database):
        print(row)

if __name__ == "__main__":
    # To test the code run `python3 main.py test`
    # otherwise run `python3 main.py`
    # to get a list of the commands run 'python3 main.py ?'
    parser = argparse.ArgumentParser(
        description="ELEC 3225 Enigma machine"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["run", "test", "print"],
        default="run",
        help="'run' for interractive mode, 'test' to run unit tests, 'print' to print the database",
    )
    args = parser.parse_args()

    if args.command == "test":
        import tests
        tests.run_tests()
    elif args.command == "print":
        print_db()
    else:
        interractive()
