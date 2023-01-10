import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import json
import jsonpickle

def encrypt_first_shuffle_array(key, iv, shuffled_array):
    encrypted_shuffle_array = []

    for num in shuffled_array:
        num_in_bytes = num.to_bytes(32, "big")
        algorithm =algorithms.AES(key)
        cipher = Cipher(algorithm, modes.CBC(iv))
        encryptor = cipher.encryptor()
        enc_num = encryptor.update(num_in_bytes) + encryptor.finalize()
        encrypted_shuffle_array.append(enc_num)

    return encrypted_shuffle_array

def encrypt_shuffle_array(key, iv, shuffled_array):
    encrypted_shuffle_array = []

    for num in shuffled_array:
        algorithm =algorithms.AES(key)
        cipher = Cipher(algorithm, modes.CBC(iv))
        encryptor = cipher.encryptor()
        enc_num = encryptor.update(num) + encryptor.finalize()
        encrypted_shuffle_array.append(enc_num)

    return encrypted_shuffle_array

def decrypt_shuffle_array(key, iv, encrypted_shuffle_array):
    decrypted_shuffle_array = []

    for enc_num in encrypted_shuffle_array:
        algorithm =algorithms.AES(key)
        cipher = Cipher(algorithm, modes.CBC(iv))
        decryptor = cipher.decryptor()
        dec_num = decryptor.update(enc_num) + decryptor.finalize()
        decrypted_shuffle_array.append(dec_num)

    return decrypted_shuffle_array

def decrypt_last_shuffle_array(key, iv, encrypted_shuffle_array):
    decrypted_shuffle_array = []

    for enc_num in encrypted_shuffle_array:
        algorithm =algorithms.AES(key)
        cipher = Cipher(algorithm, modes.CBC(iv))
        decryptor = cipher.decryptor()
        dec_num = decryptor.update(enc_num) + decryptor.finalize()
        decrypted_shuffle_array.append(int.from_bytes(dec_num, "big"))

    return decrypted_shuffle_array

def main():
    key = os.urandom(32)
    iv = os.urandom(16)
    key2 = os.urandom(32)
    iv2 = os.urandom(16)
    key3 = os.urandom(32)   
    iv3 = os.urandom(16)
   
    
    num_array = [1,2,3,4,5,6,7,8,9]
    print("Init array: ", num_array)
    aux = encrypt_first_shuffle_array(key, iv, num_array)
    c = encrypt_shuffle_array(key2, iv2, jsonpickle.decode(jsonpickle.encode(aux)))
    d = encrypt_shuffle_array(key3, iv3, jsonpickle.decode(jsonpickle.encode(c)))
    dec_array_aux = decrypt_shuffle_array(key3,iv3, jsonpickle.decode(jsonpickle.encode(d)))
    dec_array_aux2 = decrypt_shuffle_array(key2,iv2, jsonpickle.decode(jsonpickle.encode(dec_array_aux)))
    dec_array = decrypt_last_shuffle_array(key, iv, jsonpickle.decode(jsonpickle.encode(dec_array_aux2)))
    print(dec_array)

if __name__ == "__main__":
    main()