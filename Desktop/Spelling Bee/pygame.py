import random

# Word list (you can add more)
word_list = ["elephant", "giraffe", "computer", "chocolate", "banana", "pencil", "butterfly"]

def shuffle_word(word):
    word_letters = list(word)
    random.shuffle(word_letters)
    return ''.join(word_letters)

def play_game():
    print("🎮 Welcome to the Spelling Game!")
    score = 0
    rounds = 5  # Number of rounds

    for i in range(rounds):
        word = random.choice(word_list)
        shuffled = shuffle_word(word)
        
        print(f"\nRound {i+1}")
        print("🔤 Unscramble this word:", shuffled)
        
        guess = input("Your guess: ").strip().lower()
        
        if guess == word:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Oops! The correct spelling is: {word}")
    
    print(f"\n🏁 Game Over! Your score: {score}/{rounds}")

if __name__ == "__main__":
    play_game()
