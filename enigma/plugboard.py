# Plugboard Class
class Plugboard():

    def __init__(self):
        self.name = "Default Plugboard"
        self.letters = [chr(i + ord('a')) for i in range (26)]
        
    def set_swap(self, swap1, swap2):
        # Create array to hold letter dictionary

        if swap1 in self.letters and swap2 in self.letters:
            # Find positions of the letters
            pos1 = self.letters.index(swap1)
            pos2 = self.letters.index(swap2)
            # Swap them in letters[]
            self.letters[pos1], self.letters[pos2] = self.letters[pos2], self.letters[pos1]

    def swap(self, message):
        alphabet = [chr(i + ord('a')) for i in range (26)]
        new_message = []
        for char in message.lower():
            if char in alphabet:
                pos = alphabet.index(char)
                new_message.append(self.letters[pos])
            else:
                new_message.append(char)
        
        return ''.join(new_message)




            


