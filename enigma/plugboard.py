# Plugboard Class
class Plugboard():

    def __init__(self):
        self.name = "Default Plugboard"
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                       'u', 'v', 'w', 'x', 'y', 'z']
        
    def swap(self):
        while True:
            choice = int(input("What would you like to do? \n 1.) Swap Letters \n 2.) Show current configuration \n 3.) Reset to default \n 4.) Exit plugboard config: "))
            
            match choice:
                case 1:
                    swap1 = input("What letter would you like to swap? ").lower()
                    swap2 = input(f'What letter would you like to swap {swap1} with? ').lower()
                    print(f'You are swapping {swap1} with {swap2}')
                    
                    if swap1 in self.letters and swap2 in self.letters:
                        # Find positions of the letters
                        pos1 = self.letters.index(swap1)
                        pos2 = self.letters.index(swap2)
                        # Swap them in letters[]
                        self.letters[pos1], self.letters[pos2] = self.letters[pos2], self.letters[pos1]
                        print(f"Swapped {swap1} and {swap2}")
                        print("Current plugboard configuration:")
                        self.show_config()
                    else:
                        print("Invalid letters. Please enter letters a-z.")
                
                case 2:
                    print("Current plugboard configuration:")
                    self.show_config()
                
                case 3:
                    self.reset()
                    print("Plugboard reset to default (a-z)")
                
                case 4:
                    print("Exiting plugboard configuration")
                    break
                
                case _:
                    print("Invalid choice. Please select 1-4.")
    
    def reset(self):
        """Reset plugboard to default a-z configuration"""
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                       'u', 'v', 'w', 'x', 'y', 'z']
    
    def show_config(self):
        """Show current plugboard configuration in a readable format"""
        print("Position: ", end="")
        for i in range(26):
            print(f"{chr(ord('a') + i):2}", end=" ")
        print()
        print("Maps to:  ", end="")
        for i in range(26):
            print(f"{self.letters[i]:2}", end=" ")
        print()
        
        # Show active swaps
        swaps = []
        for i in range(26):
            original = chr(ord('a') + i)
            if self.letters[i] != original:
                # Only show each swap once
                if original < self.letters[i]:
                    swaps.append(f"{original}↔{self.letters[i]}")
        
        if swaps:
            print(f"Active swaps: {', '.join(swaps)}")
        else:
            print("No active swaps (default configuration)")
    
    def apply_plugboard(self, message):
        """Apply plugboard swaps to a message"""
        result = []
        for char in message.lower():
            if char.isalpha():
                # Find the index of the original letter
                original_index = ord(char) - ord('a')
                # Get the swapped letter from our letters array
                swapped_char = self.letters[original_index]
                result.append(swapped_char)
            else:
                # Non-letter characters pass through unchanged
                result.append(char)
        return ''.join(result)