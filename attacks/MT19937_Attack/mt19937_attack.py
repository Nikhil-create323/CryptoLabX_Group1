
import os
import time
import secrets
import string
import numpy as np

os.makedirs("outputs", exist_ok=True)

results = []

def show(text=""):
    print(text)
    results.append(str(text))


# Generate MT19937 keystream bytes

def generate_keystream(seed, length):
    rng = np.random.Generator(np.random.MT19937(seed))
    return rng.integers(0, 256, size=length, dtype=np.uint8)


# Encryption and decryption using XOR

def encrypt_decrypt(message, seed):
    data = np.frombuffer(message, dtype=np.uint8)
    keystream = generate_keystream(seed, len(data))
    return bytes(data ^ keystream)


# ==================================================
# PART A: MT19937 STREAM CIPHER
# ==================================================

show("========== PART A: MT19937 STREAM CIPHER ==========")

# 1. Test encryption and decryption

test_message = b"Hello MT19937 Stream Cipher"
test_seed = 12345

ciphertext = encrypt_decrypt(test_message, test_seed)
decrypted = encrypt_decrypt(ciphertext, test_seed)

show("\nOriginal message: " + test_message.decode())
show("Ciphertext (hex): " + ciphertext.hex())
show("Decrypted message: " + decrypted.decode())
show("Encryption and decryption successful: " + str(decrypted == test_message))


# 2. Generate plaintext with random prefix and 14 A characters

prefix_length = secrets.randbelow(16) + 5

characters = string.ascii_letters + string.digits + string.punctuation + " "

prefix = ''.join(
    secrets.choice(characters) for _ in range(prefix_length)
)

plaintext = (prefix + "A" * 14).encode()

# Random 16-bit seed

secret_seed = secrets.randbelow(65536)

ciphertext = encrypt_decrypt(plaintext, secret_seed)

show("\n========== SEED RECOVERY ==========")
show("Original plaintext: " + plaintext.decode())
show("Original seed: " + str(secret_seed))
show("Ciphertext (hex): " + ciphertext.hex())
show("Plaintext length: " + str(len(plaintext)))


# 3. Brute-force all 65536 seeds

known = b"A" * 14
known_length = len(known)

recovered_seed = None
recovered_plaintext = None
recovered_position = None

candidates_tested = 0

for seed in range(65536):

    candidates_tested += 1

    stream = generate_keystream(seed, len(ciphertext))

    # Search for the known 14-character sequence
    for i in range(len(ciphertext) - known_length + 1):

        possible_stream = (
            np.frombuffer(ciphertext[i:i + known_length], dtype=np.uint8)
            ^ np.frombuffer(known, dtype=np.uint8)
        )

        if np.array_equal(stream[i:i + known_length], possible_stream):

            possible_plaintext = encrypt_decrypt(ciphertext, seed)

            if known in possible_plaintext:

                recovered_seed = seed
                recovered_plaintext = possible_plaintext
                recovered_position = i
                break

    if recovered_seed is not None:
        break


# 4. Verify recovered seed

show("\nSeeds tested: " + str(candidates_tested))

if recovered_seed is not None:

    show("Recovered seed: " + str(recovered_seed))
    show("Known sequence position: " + str(recovered_position))
    show("Recovered plaintext: " + recovered_plaintext.decode())
    show("Recovered seed is correct: " + str(recovered_seed == secret_seed))
    show("Complete plaintext verified: " + str(recovered_plaintext == plaintext))
    show("14 consecutive A characters found: " + str(known in recovered_plaintext))

else:
    show("Seed recovery failed")


# ==================================================
# PART B: PREDICTABLE PASSWORD RESET TOKENS
# ==================================================

show("\n========== PART B: PASSWORD RESET TOKEN ==========")


# 5. Generate a simulated token using Unix timestamp

T = int(time.time())

observed_token = generate_keystream(T, 16).tobytes()

show("\nOriginal timestamp: " + str(T))
show("Original token (hex): " + observed_token.hex())


# 6. Attacker searches timestamps from T-300 to T+300

start_time = T - 300
end_time = T + 300

show("\n========== TIMESTAMP RECOVERY ==========")
show("Search start: " + str(start_time))
show("Search end: " + str(end_time))

recovered_timestamp = None
tested = 0

for candidate in range(start_time, end_time + 1):

    tested += 1

    candidate_token = generate_keystream(candidate, 16).tobytes()

    if candidate_token == observed_token:
        recovered_timestamp = candidate


# 7. Verify recovered timestamp

show("\nTotal timestamps tested: " + str(tested))

if recovered_timestamp is not None:

    verified_token = generate_keystream(recovered_timestamp, 16).tobytes()

    show("Recovered timestamp: " + str(recovered_timestamp))
    show("Recovered token (hex): " + verified_token.hex())
    show("Timestamp is correct: " + str(recovered_timestamp == T))
    show("Token verification: " + str(verified_token == observed_token))

else:
    show("No matching timestamp found")



show("\n========== FINAL RESULT ==========")
show("Part A: MT19937 weak seed recovery completed.")
show("Part B: Timestamp-based token prediction completed.")
show("The experiment demonstrates why MT19937 is not suitable for cryptographic use.")


# 8. Save all results

with open("outputs/results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

show("\nResults saved in outputs/results.txt")
