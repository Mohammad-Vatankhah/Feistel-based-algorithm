S_BOX = [
    0x3, 0xf, 0xe, 0x1, 0x5, 0xd, 0xa, 0x7,
    0x9, 0x0, 0x6, 0xb, 0x2, 0x8, 0xc, 0x4
]

def s_box_substitute(x):
    output = 0
    for i in range(8):  # 8 * 4 bits = 32 bits
        n = (x >> (i * 4)) & 0xF  # extract 4-bit chunk
        substituted = S_BOX[n]  # substitute using S-box
        output |= substituted << (i * 4)  # combine substituted value into output
    return output

def F(R, K):
    temp = R ^ K # XOR with the subkey
    return s_box_substitute(temp) # apply S-box substitution to the result

def generate_subkeys(K):
    # split the main key into two 32-bit halves
    K1, K2 = K >> 32, K & 0xFFFFFFFF
    subkeys = []

    for i in range(1, 17):
        if i % 2 == 0:
            subkey = (K1 ^ i) ^ K2
        else:
            subkey = (K2 ^ i) ^ K1
        subkeys.append(subkey & 0xFFFFFFFF)
    return subkeys

def encrypt(plaintext, key):
    L = plaintext >> 32 # L0
    R = plaintext & 0xFFFFFFFF # R0

    subkeys = generate_subkeys(key)

    # 16 rounds of the Feistel network
    for i in range(16):
        temp = R
        R = L ^ F(R, subkeys[i])
        L = temp

    ciphertext = (L << 32) | R # combine R and L
    return ciphertext

plaintext = 0x09135139800ABCDE
key = 0x4440136850ABCDEF

ciphertext = encrypt(plaintext, key)
print(f"Plaintext: {plaintext:016X}")
print(f"Ciphertext: {ciphertext:016X}")