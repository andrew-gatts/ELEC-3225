class Rotor:
    def __init__(self, offset=0):

        # Cleaner implementation from https://stackoverflow.com/questions/16060899/alphabet-range-in-python
        # Creates an array of all of the letters
        self.letters = [chr(i + ord('a')) for i in range (26)]
        self.offset = offset % 26
    
    def set_offset(self, offset: int):
        # Set the rotor offset (0-25)
        self.offset = offset % 26
    
    def get_offset(self) -> int:
        # Get rotor offset for debug
        return self.offset
    
    def encrypt(self, message: str) -> str:
        encrypted_message = []
        for char in message.lower():
            if char in self.letters:
                # Current index spot
                current_pos = self.letters.index(char)
                # Calculate new position with wraparound
                new_pos = (current_pos + self.offset) % 26
                encrypted_message.append(self.letters[new_pos])
            else:
                # Encrypt Message, add new letters to new value
                encrypted_message.append(char)
                
        return ''.join(encrypted_message)
    
    def show_position(self):
        return self.offset
    
