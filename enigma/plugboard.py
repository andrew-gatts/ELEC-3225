# Plugboard Class
class Plugboard():

    def __init__(self):
        self.name = "Default Plugboard"
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                       'u', 'v', 'w', 'x', 'y', 'z']
        
    def swap(self):
        choice = int((input("What would you like to do? \n 1.)Swap Letters \n 2.)Exit the Plugboard Config")))

        while choice == 1:
                swapped_letters = []
                swap1 = input("What letter would you like to swap?")
                swap2 = input(f'What letter would you like to swap  {swap1}  with?')
                print(f'You are swapping {swap1} with {swap2}')
                if swap1 in self.letters and swap2 in self.letters:
            # Find positions of the letters
                    pos1 = self.letters.index(swap1)
                    pos2 = self.letters.index(swap2)
                    # Swap them in letters[]
                    self.letters[pos1], self.letters[pos2] = self.letters[pos2], self.letters[pos1]
                    # Track the swap
                    swapped_letters.append((swap1, swap2))
                    print(f"Swapped {swap1} and {swap2}")
                    for i in range (0,26):
                        print(f"{self.letters[i]}")    

                choice = int(input("What would you like to do? \n 1.)Swap Letters \n 2.)Exit the Plugboard Config"))
                
        return self.letters






            


