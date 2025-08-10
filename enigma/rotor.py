class Rotor:
    def __init__(self, offset=0):
        # Creates an array of all of the letters
        self.letters = [chr(i + ord('a')) for i in range(26)]
        self.offset = offset % 26
    
    def set_offset(self, offset: int):
        # Set the rotor offset (0-25)
        self.offset = offset % 26
    
    def get_offset(self) -> int:
        # show rotor offset 
        return self.offset
    
    def encrypt(self, message: str) -> str:
        #start encryption. make a list to store data. 
        encrypted = []
        for char in message.lower():
            if char in self.letters:
                # 1) rotor shift whatever offset the user set 
                index = self.letters.index(char)
                new_index = (index + self.offset) % 26
                encrypted.append(self.letters[new_index])
                
            else:
                # allow spaces and punctuation to pass through.
                encrypted.append(char)  # Add spaces and punctuation to list
        
        return ''.join(encrypted) #add spaces to the encryption, where they were before encryption. 
    
    def decrypt(self, encrypted_message: str) -> str:
        #keep track of decrypted words
        decrypted = []
        for char in encrypted_message.lower():
            if char in self.letters:
                current_index = self.letters.index(char)
                # Decrypt, so shift -1 in letters
                base = (current_index - self.offset) % 26
                # orig_index = (current_index - self.offset) % 26
                
                decrypted.append(self.letters[base])

            else:
                # spaces and punctuation stay
                decrypted.append(char)

        return ''.join(decrypted)
    
    def show_position(self):
        return self.offset
