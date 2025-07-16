# Bombe
from os import name
from array import * 

# Set rotor position
class Rotor:
    def __init__(self, array):
        self.array = array
        self.position = 0

    def setPosition(self, position):
        self.position = int(position) % 26

    def forward(self, letter_char):
        shiftInput = (letter_char + self.position) % 26
        return (self.array[shiftInput] - self.position) % 26

    def backward(self, letter_char):
        return (self.array.index((letter_char + self.position) % 26) - self.position) % 26

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == 0
    

def assign_starts(rotor_1, rotor_2, rotor_3):

#new settings every day for rotors
    print("Set starting positions for the rotors")
    set_r1 = input("Set rotor 1 to desired starting point. Enter a number from 0-25: ")
    rotor_1.setPosition(set_r1)

    set_r2 = input("Set rotor 2 to desired starting point. Enter a number from 0-25:  ")
    rotor_2.setPosition(set_r2)
    
    set_r3 = input("Set rotor 3 to desired starting point. Enter a number from 0-25: ")
    rotor_3.setPosition(set_r3)

def run(letter, rotor_1, rotor_2, rotor_3, reflector):
    letter = rotor_1.forward(letter)
    letter = rotor_2.forward(letter)
    letter = rotor_3.forward(letter)
# message reflected and sent back through rotors
    letter = reflector.forward(letter)
    letter = rotor_3.backward(letter)
    letter = rotor_2.backward(letter)
    letter = rotor_1.backward(letter)

#rotors will rotate after each letter is encrypted    
    if rotor_1.rotate():
        if rotor_2.rotate(): 
            rotor_3.rotate()
        pass
    return letter

#******thinking about getting rid of this section altogether
  def array_Match():
    message_crypt=input("Type in the enigma message you wish to decrypt: ")
    guess_length=input("What do you think the message is?
    
    cryptLength=len([ele for ele in message_crypt if ele.isalpha()])
    guess_length=len([ele for ele in decoder_machine if ele.isalpha()])
    
    length_difference= cryptLength-guess_length
    print(length_difference )
    poss_combo = []
    
    for y in range (length_difference+1):
        for x in range (y, guess_length+y):
            if (message_crypt[x] != decoder_machine[x-y]):
             poss_combo.append([message_crypt[x], decoder_machine[x-y]])
    print (poss_combo)    
    return poss_combo

def add_mapping(plugboardMap, letter1, letter2):
    if letter1 in plugboardMap or letter2 in plugboardMap:
        return False
    plugboardMap[letter1] = letter2
    plugboardMap[letter2] = letter1
    return True

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
plugboard = {}  
crib = array_Match()


# basic plugboard settings
array_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
array_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
array_3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
reflectArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
rotor_1 = Rotor(array_1)
rotor_2 = Rotor(array_2)
rotor_3 = Rotor(array_3)
reflector = Rotor(reflectArray)

for i in range (26):
    plugboardGuess = alphabet[i] 
            
    
    for f in range (len(crib)):

        if (plugboardGuess == crib[f][0]) :
            continue
        print ("Mapping Guess: ")
        print (plugboardGuess, crib[f][0])
        match = False
       
        #Check if plugboard guess already exists in mapping
        if (plugboardGuess in plugboardGuess and plugboardGuess[plugboardGuess] == crib[f][0]) 

            match = True
            print("Mapping already exitsts:", plugboardGuess, crib[f][0])
            continue
            break
            
        if match: 
            continue
            if add_mapping(plugboard, plugboardGuess, crib[f][0]):
                print("Mapping added: ", plugboardGuess, crib[f][0])
            else:
                print("Mapping already exists or invalid: ", plugboardGuess, crib[f][0])
