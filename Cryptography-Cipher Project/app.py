# Constants for readability (ASCII values)
A_LOWER = 97 # ord('a')
Z_LOWER = 122 # ord('z')
ALPHABET_SIZE = 26

# --- Helper Function for Cipher Logic ---

def _process_char(char, shift_amount):
    """
    Processes a single alphabetic character based on a given shift.
    Maintains original case (upper/lower).
    """
    if not char.isalpha():
        return char

    # Determine the base (ord('a') or ord('A'))
    base = A_LOWER
    
    # Calculate the new position (0-25)
    char_index = ord(char.lower()) - base
    new_index = (char_index + shift_amount) % ALPHABET_SIZE
    
    # Convert back to the new character
    new_char = chr(new_index + base)
    
    # Restore original case
    return new_char.upper() if char.isupper() else new_char

# --- Original Ciphers (Refactored) ---

def caesar_cipher(text, shift, mode='encrypt'):
    """Encrypts or decrypts text using the Caesar cipher."""
    result = ''
    # Decryption is just a negative shift
    shift_amount = shift if mode == 'encrypt' else -shift
    
    for char in text:
        result += _process_char(char, shift_amount)
        
    return result

def vigenere_cipher(text, keyword, mode='encrypt'):
    """Encrypts or decrypts text using the Vigenère cipher."""
    result = ''
    keyword = ''.join(filter(str.isalpha, keyword)).lower()
    if not keyword:
        return text

    keyword_len = len(keyword)
    keyword_index = 0

    for char in text:
        if char.isalpha():
            # Calculate the shift for the current keyword letter (0-25)
            shift = ord(keyword[keyword_index % keyword_len]) - A_LOWER
            
            # Determine overall shift amount based on mode
            shift_amount = shift if mode == 'encrypt' else -shift
            
            result += _process_char(char, shift_amount)
            
            # Only advance the keyword index for alphabetic characters
            keyword_index += 1
        else:
            result += char
            
    return result

def atbash_cipher(text):
    """Encrypts text using the Atbash cipher (self-reciprocal)."""
    result = ''
    for char in text:
        if char.isalpha():
            # Atbash calculates the distance from 'a' and subtracts it from 'z'
            # Formula: new_char_ord = (Z_LOWER + A_LOWER) - ord(char.lower())
            
            # This can be simplified to: 122 - (ord(char.lower()) - 97)
            
            new_char_ord = Z_LOWER - (ord(char.lower()) - A_LOWER)
            new_char = chr(new_char_ord)
            
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
            
    return result

# --- NEW CIPHER ADDITION: Rail Fence Cipher (Complex) ---

def rail_fence_cipher(text, rails, mode='encrypt'):
    """
    Encrypts or decrypts text using the Rail Fence cipher (transposition cipher).
    
    Args:
        text (str): The plaintext or ciphertext.
        rails (int): The number of rails (rows) for the fence.
        mode (str): 'encrypt' or 'decrypt'.
        
    Returns:
        str: The resulting ciphertext or plaintext.
    """
    if rails <= 1:
        return text

    # Strip non-alphabetic characters (Transposition ciphers often work only on letters)
    letters = ''.join(filter(str.isalpha, text))
    if not letters:
        return text
    
    text_len = len(letters)
    
    # 1. Create the rail matrix and fill the zig-zag pattern
    fence = [['\n'] * text_len for _ in range(rails)]
    row, direction = 0, 1 # direction: 1 for down, -1 for up
    
    for i in range(text_len):
        if row == 0:
            direction = 1 # Move down
        elif row == rails - 1:
            direction = -1 # Move up
        
        # Place holder or character
        fence[row][i] = letters[i] if mode == 'encrypt' else '*'
        
        row += direction
    
    # --- ENCRYPTION LOGIC ---
    if mode == 'encrypt':
        result = []
        for r in range(rails):
            for c in range(text_len):
                if fence[r][c] != '\n':
                    result.append(fence[r][c])
        
        # Re-insert non-alphabetic characters in their original positions (best effort)
        final_result = list(text)
        result_idx = 0
        for i, char in enumerate(final_result):
            if char.isalpha():
                final_result[i] = result[result_idx]
                result_idx += 1
        return "".join(final_result)
        
    # --- DECRYPTION LOGIC ---
    elif mode == 'decrypt':
        # 2. Mark the positions where characters originally went ('*')
        index = 0
        for r in range(rails):
            for c in range(text_len):
                if fence[r][c] == '*':
                    fence[r][c] = letters[index]
                    index += 1
        
        # 3. Read the matrix in zig-zag order to reconstruct the original text
        result = []
        row, direction = 0, 1
        
        for i in range(text_len):
            if row == 0:
                direction = 1
            elif row == rails - 1:
                direction = -1
            
            result.append(fence[row][i])
            
            row += direction
        
        # Re-insert non-alphabetic characters
        final_result = list(text)
        result_idx = 0
        for i, char in enumerate(final_result):
            if char.isalpha():
                final_result[i] = result[result_idx]
                result_idx += 1
        return "".join(final_result)
    
    else:
        return "Invalid mode for Rail Fence."


# --- Main Menu (Updated) ---

def main():
    while True:
        print("\n===== Cryptography-Cipher Project =====")
        print("1. Caesar Cipher (Substitution)")
        print("2. Vigenère Cipher (Polyalphabetic)")
        print("3. Atbash Cipher (Substitution)")
        print("4. Rail Fence Cipher (Transposition)") # New option
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("Enter the text: ")
            try:
                shift = int(input("Enter the shift value: "))
                mode = input("Choose mode (encrypt/decrypt): ").lower()
                print(f"Result: {caesar_cipher(text, shift, mode)}")
            except ValueError:
                print("Invalid shift value.")

        elif choice == '2':
            text = input("Enter the text: ")
            keyword = input("Enter the keyword: ")
            mode = input("Choose mode (encrypt/decrypt): ").lower()
            print(f"Result: {vigenere_cipher(text, keyword, mode)}")

        elif choice == '3':
            text = input("Enter the text: ")
            print(f"Result: {atbash_cipher(text)}")

        elif choice == '4': # New Cipher Block
            text = input("Enter the text: ")
            try:
                rails = int(input("Enter the number of rails (rows): "))
                mode = input("Choose mode (encrypt/decrypt): ").lower()
                print(f"Result: {rail_fence_cipher(text, rails, mode)}")
            except ValueError:
                print("Invalid rail count.")
        
        elif choice == '5':
            print("Exiting Cryptography-Cipher Project. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
