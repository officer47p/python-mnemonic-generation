from bitstring import BitArray
from hashlib import sha256
from wordlist import wordlist


def binary_to_decimal(b_num):
    value = 0
    for i in range(len(b_num)):
        digit = b_num.pop()
        if digit == '1':
            value = value + pow(2, i)

    return value


def append_checksum(entropy_bits: BitArray):
    CHECKSUM_LENGTH = len(entropy_bits) // 32
    m = sha256()
    m.update(entropy_bits.bytes)
    checksum = BitArray(m.digest())
    entropy_bits.append(checksum[:CHECKSUM_LENGTH])

    return entropy_bits


# The actual entropy which can be from 128 to 256 bits
entropy_hex = "063679ca1b28b5cfda9c186b367e271e"
# Converting the entropy to bit array in order to work with it easier
entropy_bits = BitArray(hex=entropy_hex)
# Appending checksum to the end of entropy
check_entropy = append_checksum(entropy_bits)
# Spliting the entropy into groups of 11 bits
groups = list(zip(*(iter(entropy_bits),) * 11))
# Converting the datatype of groups from list[tuple[bool]] to list[BitArray]
groups = list(map(lambda x: BitArray(x), groups))
# Converting the bits to decimals
groups = list(map(lambda x: binary_to_decimal(list(x.bin)), groups))
# Converting the decimals to mnemonic words
groups = list(map(lambda x: wordlist[x], groups))
# Joinin the words
mnemonic = " ".join(groups)

print(mnemonic)
