#Engima Class
import plugboard
class Enigma():
   
    def show_word(self):
        print(("What word would you like to encrypt?"))
        word = input()
        return word
     
enigma = Enigma()
print (f'The word you want to encrypt is {enigma.show_word()}')

Plug = plugboard.Plugboard()
print (f'Now swapping... {Plug.setting1()}') 