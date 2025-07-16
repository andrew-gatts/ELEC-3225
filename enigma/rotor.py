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
                encrypted_char = self.letters[new_index]
                
                # 2) if current inputted char is the same as index-1, it is a repeat. shift rotor again.
                if encrypted and encrypted[-1] == encrypted_char:
                    new_index = (new_index + 1) % 26
                    encrypted_char = self.letters[new_index]  #Update current inputted word to avoid repeats. Move repeats +1 in Rotors. 
                encrypted.append(encrypted_char)  #Add char to list. We keep track of this to be able to decrypt later. 
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
                orig_index = (current_index - self.offset) % 26
                
                # one we decrypt, check for duplicates. 
                if decrypted:
                    prev = decrypted[-1] 
                    if prev in self.letters:  # Only check if prev is a letter
                        prev_encrypted_index = (self.letters.index(prev) + self.offset) % 26
                        skip_enc_index = (prev_encrypted_index + 1) % 26
                        # if our char matches that "skipped‐to" codepoint,
                        # undo from cur_index-1 instead of straight reverse
                        if current_index == skip_enc_index:
                            orig_index = (current_index - 1 - self.offset) % 26
                decrypted.append(self.letters[orig_index])
            else:
                # spaces and punctuation stay
                decrypted.append(char)

        return ''.join(decrypted)
    
    def show_position(self):
        return self.offset