class Rotor:
    def __init__(self, offset=0):
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
        encrypted = []
        for ch in message.lower():
            if ch in self.letters:
                # 1) basic Caesar shift
                index = self.letters.index(ch)
                new_index = (index + self.offset) % 26
                enc = self.letters[new_index]

                # 2) if it would duplicate the last encrypted char, bump it one more
                if encrypted and encrypted[-1] == enc:
                    new_index = (new_index + 1) % 26
                    encrypt = self.letters[new_index]

                encrypted.append(encrypt)
            else:
                # non-letters pass through
                encrypted.append(encrypt)

        return ''.join(encrypted)
    
    def decrypt(self, encrypted_message: str) -> str:
        decrypted = []
        for char in encrypted_message.lower():
            if char in self.letters:
                cur_index = self.letters.index(ch)

                # normal reverse shift
                orig_idx = (cur_index - self.offset) % 26

                # detect if this was the “skipped duplicate” case
                if decrypted:
                    prev = decrypted[-1]
                    prev_enc_index = (self.letters.index(prev) + self.offset) % 26
                    skip_enc_index = (prev_enc_index + 1) % 26

                    # if our ch matches that “skipped‐to” codepoint,
                    # undo from cur_idx-1 instead of straight reverse
                    if cur_index == skip_enc_index:
                        orig_index = (cur_index - 1 - self.offset) % 26

                decrypted.append(self.letters[orig_idx])
            else:
                decrypted.append(char)

        return ''.join(decrypted)

    
    def show_position(self):
        return self.offset