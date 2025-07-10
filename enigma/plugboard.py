# Plugboard Class
def plugboard(message, swap1, swap2):
    new_message = []
    for char in message.lower():
        if char is swap1:
            new_message.append(swap2)
        elif char is swap2:
            new_message.append(swap1)
        else:
            new_message.append(char)
    
    return ''.join(new_message)




            


