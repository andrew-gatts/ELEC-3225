# Plugboard Class
class Plugboard():

    def __init__(self):
        self.name = "Default Plugboard"
        # self.letters = [chr(i + ord('a')) for i in range (26)]

    def swap(self, message, swap1, swap2):
        new_message = []
        for char in message.lower():
            if char is swap1:
                new_message.append(swap2)
            elif char is swap2:
                new_message.append(swap1)
            else:
                new_message.append(char)
        
        return ''.join(new_message)




            


