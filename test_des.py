from des import encrypt, decrypt

key = "ashamaam"
message = "Hello Network Security!"

cipher = encrypt(message, key)
plain = decrypt(cipher, key)

print("Original :", message)
print("Cipher   :", cipher)
print("Decrypted:", plain)

assert plain == message
print("TEST PASSED")
