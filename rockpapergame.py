import random

# Function to get the computer's choice
def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

# Function to determine the winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return 'user'
    else:
        return 'computer'

# Function to display the result
def display_result(user_choice, computer_choice, result):
    print(f"\nUser choice: {user_choice}")
    print(f"Computer choice: {computer_choice}")
    
    if result == 'tie':
        print("It's a tie!")
    elif result == 'user':
        print("You win!")
    else:
        print("Computer wins!")

# Main game loop
def play_game():
    user_score = 0
    computer_score = 0

    while True:
        user_choice = input("\nEnter rock, paper, or scissors (or 'quit' to exit): ").lower()
        
        if user_choice == 'quit':
            print(f"Final Scores - You: {user_score}, Computer: {computer_score}")
            break
        
        if user_choice not in ['rock', 'paper', 'scissors']:
            print("Invalid choice. Please choose rock, paper, or scissors.")
            continue
        
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        
        if result == 'user':
            user_score += 1
        elif result == 'computer':
            computer_score += 1

        display_result(user_choice, computer_choice, result)
        print(f"Current Scores - You: {user_score}, Computer: {computer_score}")

# Run the game
play_game()
