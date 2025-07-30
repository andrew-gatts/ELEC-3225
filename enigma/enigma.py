from rotor import Rotor
from plugboard import Plugboard
from database import init_db, add_entry, close_db
DB_PATH = "database.db"

def main():
    choice = int(input("Welcome to Enigma! What would you like to do?\n 1.) Set up Plugboard\n 2.) Set Rotors\n 3.) Set Reflector\n 4.) Encrypt Message\n 5.) Decrypt Message\n 6.) Exit "))
    # Initialize variables to track setup state
    plugboard1 = None
    rotor1 = None
    rotor2 = None
    rotor3 = None
    while choice != 6:  
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
                
                    # Apply plugboard first (if configured)
                    if plugboard1 is not None:
                        message = plugboard1.apply_plugboard(message)
                    
                    # Then apply rotors in sequence
                    message_r1 = rotor1.encrypt(message)
                    print(f"\n\n----- FIRST ROTOR: {message} --> {message_r1}")
                    message_r2 = rotor2.encrypt(message_r1)

                    print(f"\n\n ----- SECOND ROTOR: {message_r1} --> {message_r2}")
                    message_r3 = rotor3.encrypt(message_r2)
                    print(f"\n \n ----- THIRD ROTOR: {message_r2} --> {message_r3}")
                    
                    # Apply plugboard again at the end (if configured)
                    if plugboard1 is not None:
                        message_r3 = plugboard1.apply_plugboard(message_r3)
                    
                    print(f"Encrypted message: {message_r3}")
            
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
            case 6:
                print("You are now exiting the program.")
                break
            case _:
                print("Invalid choice. Please select a valid option.")
        
        choice = int(input("\n 1.) Set up Plugboard\n 2.) Set Rotors\n 3.) Set Reflector\n 4.) Encrypt Message\n 5.) Decrypt Message\n 6.) Exit "))

    print("Goodbye!")
main()  