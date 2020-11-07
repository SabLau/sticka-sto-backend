import hashlib
import random
import string

from random import randint


# Random string is sufficient enough for email order confirmation
letter_digits = string.ascii_letters + string.digits
result = ''.join((random.choice(letter_digits) for i in range(12)))
print("Random String is:", result)

# md5 or encryption is necessary for password security
encode = hashlib.md5(result.encode())

print(encode)

print(encode.hexdigest())

print(encode.digest())