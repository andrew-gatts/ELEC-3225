from rotor import Rotor
from database import init_db, add_entry, close_db

DB_PATH = "database.db"

def main():
    # Initialize Database
    database = init_db()
    
    message = input("Enter the message to encrypt: ")
    offset = int(input("Enter the rotor offset (1-25): "))

    print(f"{offset}")

    rotor = Rotor(offset)
    encrypted = rotor.encrypt(message)

    crn = add_entry(database, message, encrypted)
    print(f"Saved entry CRN={crn}")

    print(f"Original : {message}")
    print(f"Encrypted: {encrypted}")

    close_db(database)

main()  