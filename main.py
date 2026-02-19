# Algorithms Project 1 - RSA
# Author: CPSC Template/Shaun Moran
# 02.18.2026
# Objective: implement RSA Encryption and apply it to digital signature
import pandas as pd
import numpy as np
# this is the library you need
import hashlib                        # allows use of hash
print(hashlib.algorithms_guaranteed)
h = hashlib.sha256(b'computer science at UA is the best')
m = h.hexdigest()
print(m)
# Helper functions

def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(e, phi): # Uses Extended Euclidean algorithm
    """Modular multiplicative inverse of e mod phi."""
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_large_prime(bits=256): # Generates prime number comprised of 256 bits
    """Generate a random probable prime of given bit length."""
    import random
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # ensure top bit set and odd
        if FermatPrimalityTest(candidate):
            return candidate
# Check if p is prime (most likely a prime)
# to be completed
def FermatPrimalityTest(p):
    print(p)
    a = False
    # Hardcode two tests using 2,3
    if p < 2:
        return False
    if p == 2 or p == 3:
        return True
    if p % 2 == 0:
        return False
    # Fermat's little theorem: test with a=2 and a=3
    if pow(2, p - 1, p) != 1:
        return False   # composite
    if pow(3, p - 1, p) != 1:
        return False   # composite
    a = True           # passed both tests, likely prime
    return a
# you need to modify this function to generate the two pairs of keys!!!
# to be completed      
def RSA_key_generation():
    p = generate_large_prime(256) # generates p and q used to compute two keys for RSA
    q = generate_large_prime(256)
    while q == p:
        q = generate_large_prime(256)

    n   = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # hardcoded standard public exponent
    while extended_gcd(e, phi)[0] != 1:
        e += 2

    d = mod_inverse(e, phi) # converts e to d

    # Open a file in write mode ('w') and save ints p,q
    with open('p_q.txt', 'w') as file:
        file.write(f"{p}\n")
        file.write(f"{q}")

    # Open a file in write mode and save ints e,n
    with open('e_n.txt', 'w') as file: # public key
        file.write(f"{e}\n")
        file.write(f"{n}")

    # Open a file in write mode and save ints e,n
    with open('d_n.txt', 'w') as file: # private key
        file.write(f"{d}\n")
        file.write(f"{n}")

    print("done with key generation!")
    return
# to be completed
def Signing(doc, key):
    match = False
    # ...
    d, n = key

    # 1. Hash the document with SHA-256 and convert to integer
    digest   = hashlib.sha256(doc).hexdigest()
    hash_int = int(digest, 16)

    # 2. Sign: signature = hash^d mod n  (private-key operation)
    signature = pow(hash_int, d, n)

    # 3. Convert signature to 64 bytes (512 bits / 8)
    sig_bytes = signature.to_bytes(64, byteorder='big')

    match = True
    print("\nSigned ...")
    return sig_bytes
# to be completed
def verification(doc, key):
    match = False
    # ...
    e, n = key

    # Separate: last 64 bytes are the signature, everything before is the content
    original  = doc[:-64]
    sig_bytes = doc[-64:]

    # Convert signature bytes back to integer
    signature = int.from_bytes(sig_bytes, byteorder='big')

    # Hash the original content
    digest   = hashlib.sha256(original).hexdigest()
    hash_int = int(digest, 16)

    # Recover hash: recovered = signature^e mod n
    recovered = pow(signature, e, n)

    match = (recovered == hash_int)

    if match:
        print("\nAuthentic!")
    else:
        print("\nModified!")
    
    return
# to be completed
def CPSC_435_Project1(part, task="", fileName=""):
    # part I, command-line arguments will be: python yourProgram.py 1
    if part == 1:
        RSA_key_generation()
    # part II, command-line will be for example: python yourProgram.py 2 s file.txt
    #                                       or   python yourProgram.py 2 v file.txt.signed
    else:
        if "s" in task:  # do signing
            # you figure out
            with open(fileName, 'rb') as f:
                doc = f.read()
            with open('d_n.txt', 'r') as f:
                lines = f.read().strip().split('\n')
            key = (int(lines[0]), int(lines[1]))   # (d, n)

            sig_bytes = Signing(doc, key)

            # Append 64-byte signature directly to original content
            with open(fileName + '.signed', 'wb') as f:
                f.write(doc)
                f.write(sig_bytes)

            print(f"Saved: {fileName}.signed")

        else:
            # do verification
            # you figure out
            with open(fileName, 'rb') as f:
                doc = f.read()
            with open('e_n.txt', 'r') as f:
                lines = f.read().strip().split('\n')
            key = (int(lines[0]), int(lines[1]))   # (e, n)

            verification(doc, key)

    print("done!")
    
    return
# when we grade your part 1 - RSA_key_generation, we call this func
CPSC_435_Project1(1)
# when we grade your part 2a - signing,
docName = "contract.txt" # the fileName is just an example
CPSC_435_Project1(2, "s", docName)
# when we grade your part 2b - verification,
docName = "contract.txt.signed" # the fileName is just an example
CPSC_435_Project1(2, "v", docName)