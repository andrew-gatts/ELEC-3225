from rotor import Rotor
from plugboard import Plugboard
from database import init_db, add_entry, close_db

DB_PATH = "database.db"

def main():
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

    # Plugboard
    swap1 = input("What letter would you like to swap? ")
    swap2 = input(f'What letter would you like to swap {swap1} with? ')
    # Create plugboard class
    plugboard1 = Plugboard()
    plugboard1.set_swap(swap1, swap2)
    pbencrypted = plugboard1.swap(encrypted)
    print(pbencrypted)
    
    # Database Entry
    crn = add_entry(database, message, pbencrypted)
    print(f"Saved entry CRN={crn}")
    close_db(database)

main()  