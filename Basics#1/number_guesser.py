#basic game using random module, user need to guess random number
import random

random_number = random.randint(1, 20)
count = 0
guess = False

while not guess:
    number = int(input("Guess a number between 1 and 20: "))
    count += 1
    if number == random_number:
        print("Correct! Number of guesses is: ", count)
        guess = True
    elif number > random_number:
        print("Too high!")
    else:
        print("Too low!")