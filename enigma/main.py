import sqlite3
import rotor
import plugboard  
def main():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
              'u', 'v', 'w', 'x', 'y', 'z']
    
    for i in range(len(letters)):
        print(f"{i + 1}) {letters[i]} \n")
    # Create and use rotor
    rotor1 = rotor.Rotor()
    # Test encryption
    rotor1.encrypt()
    print(f"Your rotor is in position {rotor1.show_position()}!") 

main()  