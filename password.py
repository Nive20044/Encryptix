import random
import string

def generate_password(length):
    # Define the characters to use in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate the password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    # Prompt the user for the password length
    try:
        length = int(input("Enter the desired length for the password: "))
        
        # Ensure length is a positive number
        if length <= 0:
            print("Please enter a positive integer.")
            return
        
        # Generate and display the password
        password = generate_password(length)
        print(f"Generated Password: {password}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
