import sqlite3
#Plugboard Class
# class Plugboard():
#     def setting1(self):
#         print("What letter would you like to swap?")
#         swap1 = input()
#         print (f'What letter would you like to swap  {swap1}  with?')
#         swap2 = input()
#         print(f'You are swapping {swap1} with {swap2}')

# #Engima Class

# class Enigma():
   
#      def show_word(self):
#         print(("What word would you like to encrypt?"))
#         word = input()
#         return word
     
# enigma = Enigma()
# print (f'The word you want to encrypt is {enigma.show_word()}')

# Plug = Plugboard()
# print (f'Now swapping... {Plug.setting1()}') 
class Rotor:
    def __init__(self):
        self.name = "Default Rotor"
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                       'u', 'v', 'w', 'x', 'y', 'z']
        self.offset = 0;
    
    def encrypt(self):
        message = input("What is your message you want to encrypt? ").lower()
        self.offset = int(input("How big would you like your offset? (Ex: 1 shifts A->B): "))
        encrypted_message = ""
        
        for char in message:
            if char in self.letters:
                # Current index spot
                current_pos = self.letters.index(char)
                # Calculate new position with wraparound
                new_pos = (current_pos + self.offset) % 26
                encrypted_message += self.letters[new_pos]
            else:
                # Encrypt Message, add new letters to new value
                encrypted_message += char
        
        print(f"Original: {message}")
        print(f"Encrypted: {encrypted_message}")
        return encrypted_message
    
    def show_position(self):
        return self.offset
        
        
    
def main():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
              'u', 'v', 'w', 'x', 'y', 'z']
    
    for i in range(len(letters)):
        print(f"{i + 1}) {letters[i]} \n")
    # Create and use rotor
    rotor1 = Rotor()
    # Test encryption
    rotor1.encrypt()
    print(f"Your rotor is in position {rotor1.show_position()}!") 

main()  