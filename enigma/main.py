from rotor import Rotor
from plugboard import Plugboard
from database import init_db, add_entry, close_db
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
