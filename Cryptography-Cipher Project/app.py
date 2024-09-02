def caesar_cipher(text, shift, mode='encrypt'):
    result = ''
    for char in text:
        if char.isalpha():
            shift_amount = shift if mode == 'encrypt' else -shift
            new_char = chr((ord(char.lower()) - 97 + shift_amount) % 26 + 97)
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result

def vigenere_cipher(text, keyword, mode='encrypt'):
    result = ''
    keyword_repeated = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(keyword_repeated[i].lower()) - 97
            shift_amount = shift if mode == 'encrypt' else -shift
            new_char = chr((ord(char.lower()) - 97 + shift_amount) % 26 + 97)
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result

def atbash_cipher(text):
    result = ''
    for char in text:
        if char.isalpha():
            new_char = chr(122 - (ord(char.lower()) - 97))
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result

def main():
    while True:
        print("\n===== Cryptography-Cipher Project =====")
        print("1. Caesar Cipher")
        print("2. Vigenère Cipher")
        print("3. Atbash Cipher")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("Enter the text: ")
            shift = int(input("Enter the shift value: "))
            mode = input("Choose mode (encrypt/decrypt): ").lower()
            print(f"Result: {caesar_cipher(text, shift, mode)}")

        elif choice == '2':
            text = input("Enter the text: ")
            keyword = input("Enter the keyword: ")
            mode = input("Choose mode (encrypt/decrypt): ").lower()
            print(f"Result: {vigenere_cipher(text, keyword, mode)}")

        elif choice == '3':
            text = input("Enter the text: ")
            print(f"Result: {atbash_cipher(text)}")

        elif choice == '4':
            print("Exiting Cryptography-Cipher Project. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
