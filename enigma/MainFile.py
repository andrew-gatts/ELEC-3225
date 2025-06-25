#Rotor Class
class Rotor():
   
    def __init__(self, in_position):
        answer = in_position

    def show_position(self):
        print("What position would you like the rotor position to be at? (1-26)")
        answer = input()
        if answer == 1:
            Rotor1

        return answer
        
    #def rotate():
        
    Rotor1 = ["A", "B", "C", "D", "E", "F","G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
   
    def setPos(self, position):
        self.position = int(position) % 26

    
rotor1 = Rotor(26)
print(f'Rotor 1 is in position {rotor1.show_position()}')
rotor2 = Rotor(26)
print(f'Rotor 2 is in position {rotor2.show_position()}')
rotor3 = Rotor(26)
print(f'Rotor 3 is in position {rotor3.show_position()}')


#Plugboard Class
class Plugboard():
    def setting1(self):
        print("What letter would you like to swap?")
        swap1 = input()
        print (f'What letter would you like to swap  {swap1}  with?')
        swap2 = input()
        print(f'You are swapping {swap1} with {swap2}')

#Engima Class

class Enigma():
   
     def show_word(self):
        print(("What word would you like to encrypt?"))
        word = input()
        return word
     
enigma = Enigma()
print (f'The word you want to encrypt is {enigma.show_word()}')

Plug = Plugboard()
print (f'Now swapping... {Plug.setting1()}') 
            
