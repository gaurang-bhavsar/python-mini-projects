# An encryptor in python
import random 
import string

chars=" " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()
random.shuffle(key)

#print(chars)
#print(key)

#  ENCRYPTION
plain_text=input("Enter a message you wanna encrypt ")
cipher_text =""

for letter in plain_text:
    index=chars.index(letter)
    cipher_text+=key[index]

print(f"Original message: {plain_text}")
print(f"encrypt message: {cipher_text}")

###########################################

#DECRYPT
cipher_text=input("Enter an encrypt text: ")
plain_text=""

for letter in cipher_text:
    index=cipher_text.index(letter)
    plain_text+=chars[index]

print(f"encrypted message: {cipher_text}")
print(f"original message: {plain_text}")