# Plugboard Class
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