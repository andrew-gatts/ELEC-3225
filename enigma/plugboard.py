# Plugboard Class
class Plugboard():

    def __init__(self):
        self.name = "Default Plugboard"
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                       'u', 'v', 'w', 'x', 'y', 'z']
        
    def setting1(self):
        swap1 = input("What letter would you like to swap?")
        print (f'What letter would you like to swap  {swap1}  with?')
        swap2 = input(f'You are swapping {swap1} with {swap2}')

        if swap1 in self.letters and swap2 in self.letters:
                s = swap2.replace(swap1)
                return s






            


