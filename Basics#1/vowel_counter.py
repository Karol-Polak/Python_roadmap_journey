#basic vowel counting tool in given by user text
text = input("Enter text: ").lower()
vowels = ['a', 'ą', 'e', 'ę', 'i', 'o', 'u', 'ó', 'y']
counter = 0

for letter in text:
    if letter in vowels:
        counter += 1

print("Number of vowels:", counter)
