from .rotor import Rotor
from .plugboard import Plugboard
from .database import init_db, add_entry, close_db

DB_PATH = "database.db"

def encrypt_message(text: str, rotors: list[Rotor], plugboard: Plugboard) -> str:
    
    # Apply plugboard first (if configured)
    message = text
    if plugboard is not None:
        message = plugboard.apply_plugboard(message)

    # Then apply rotors in sequence
    out = message
    for r in rotors:
        out = r.encrypt(out)

    # Apply plugboard again at the end (if configured)
    if plugboard is not None:
        out = plugboard.apply_plugboard(out)

    # Add result to the database
    db = init_db(DB_PATH)
    add_entry(db, text, out)
    close_db(db)

    return out

def main():
    print("\n=== Enigma ===")
    # Initialize variables to track setup state
    choice = 1 
    plugboard1 = None
    rotor1 = None
    rotor2 = None
    rotor3 = None
    while choice != 0:
        print("\nMenu:\n" 
              " 1) Set up Plugboard\n"
              " 2) Set Rotors\n"
              " 3) Set Reflector\n"
              " 4) Encrypt Message\n"
              " 5) Decrypt Message\n"
              " 0) Quit ")
        choice = int(input("Select: "))
        match choice: 
            case 1:
                print("----ENTERING PLUGBOARD CONFIG ----\n")
                plugboard1 = Plugboard()
                ask_swap = int(input(" 1.) Configure/View \n 2.) Back to Menu "))
                match ask_swap:
                    case 1: 
                        plugboard1.swap()
                    case 2:
                        pass
            case 2: 
                offset_r1 = int(input("Enter the offset for rotor #1 (0-25): "))
                rotor1 = Rotor(offset_r1)
                offset_r2 = int(input("Enter the offset for rotor #2 (0-25): "))
                rotor2 = Rotor(offset_r2)
                offset_r3 = int(input("Enter the offset for rotor #3 (0-25): "))
                rotor3 = Rotor(offset_r3)
                print("Rotors configured successfully!")
            case 3: 
                print("This is the Set Reflector function")
            case 4:
                if rotor1 is None or rotor2 is None or rotor3 is None:
                    print("Please set up rotors first (option 2)")
                else:
                    print("What message would you like to encrypt: ")
                    in_message = str(input())
                    message = in_message.strip()
                
                    # Use the encrypt function
                    out_message = encrypt_message(message, [rotor1, rotor2, rotor3], plugboard1)
                    
                    print(f"Encrypted message: {out_message}")

                                
            case 5:
                if rotor1 is None or rotor2 is None or rotor3 is None:
                    print("Please set up rotors first (option 2)")
                else:
                    print("What message would you like to decrypt: ")
                    encrypted_message = str(input())
                    # Apply plugboard first (if configured)
                    if plugboard1 is not None:
                        encrypted_message = plugboard1.apply_plugboard(encrypted_message)
                    
                    # Decrypt in reverse order (rotor3 -> rotor2 -> rotor1)
                    message_r3 = rotor3.decrypt(encrypted_message)
                    message_r2 = rotor2.decrypt(message_r3)
                    decrypted_message = rotor1.decrypt(message_r2)
                    
                    # Apply plugboard again at the end (if configured)
                    if plugboard1 is not None:
                        decrypted_message = plugboard1.apply_plugboard(decrypted_message)
                    
                    print(f"Decrypted message: {decrypted_message}")
            case 0:
                print("You are now exiting the program.")
                break
            case _:
                print("Invalid choice. Please select a valid option.")        
      
    print("Goodbye!")

if __name__ == "__main__":
    main()  
