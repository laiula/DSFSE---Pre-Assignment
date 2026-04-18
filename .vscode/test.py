
word = input("Enter a word: ")


consonant = 0
vowel = 0
for i in word:
    if i.lower() in 'aeiou':
        vowel = vowel + 1
    else:
        consonant = consonant + 1

print("Number of consonants: ", consonant)
print("Number of vowels: ", vowel)