
# MT19937 Stream Cipher and Predictable Password Reset Tokens

## Objective

To understand why a statistical pseudorandom number generator is unsuitable for cryptographic applications by implementing a toy stream cipher, recovering a weak seed, and analyzing predictable reset tokens.

## Technologies Used

- Python
- NumPy
- MT19937 (Mersenne Twister)
- XOR Encryption
- Brute-force Attack
- Unix Timestamp

## Project Structure

```text
MT19937_Attack/
│
├── mt19937_attack.py
├── README.md
│
└── outputs/
    └── results.txt
```

## Part A: MT19937 Stream Cipher

### 1. Stream Cipher Implementation

- Uses NumPy's inbuilt MT19937 implementation.
- Generates one 8-bit keystream value per plaintext byte.
- Encrypts plaintext using XOR.
- Uses the same function for encryption and decryption.

### 2. Encryption and Decryption

Encryption:

Ciphertext = Plaintext XOR Keystream

Decryption:

Plaintext = Ciphertext XOR Keystream

XOR is reversible when the same keystream is used.

### 3. Known Plaintext Attack

- Generates a random printable prefix of 5–20 characters.
- Appends 14 consecutive A characters.
- Encrypts the plaintext using a randomly selected 16-bit seed.
- The position of the known sequence is unknown.

### 4. Brute-force Seed Recovery

The program tests all possible 16-bit seeds.

Search space:

2^16 = 65,536 possible seeds.

For each seed:

1. Generate the candidate keystream.
2. Search for the known 14-byte sequence.
3. Compare the expected and generated keystream bytes.
4. Decrypt the complete ciphertext if a match is found.
5. Verify the recovered plaintext and seed.

## Part B: Predictable Password Reset Tokens

### 1. Token Generation

- Records the current Unix timestamp.
- Uses the timestamp as the MT19937 seed.
- Generates 16 consecutive 8-bit outputs.
- Combines the outputs into a 16-byte token.
- Displays the timestamp and token in hexadecimal.

### 2. Timestamp Recovery

The simulated attacker knows that the token was generated within 300 seconds before or after the observed time.

Search interval:

T - 300 to T + 300

Total candidates:

601 timestamps.

For every candidate timestamp:

1. Seed MT19937 with the candidate.
2. Generate a 16-byte token.
3. Compare it with the observed token.
4. Record matching timestamps.
5. Regenerate the token to verify the match.

## MT19937 Algorithm

MT19937 stands for Mersenne Twister 19937.

It is a pseudorandom number generator that:

- Maintains an internal state of 624 32-bit words.
- Uses a recurrence operation called twisting.
- Uses tempering operations to improve the output distribution.
- Has a period of 2^19937 - 1.

## Why MT19937 Is Not Cryptographically Secure

1. It is deterministic.
2. Its output is predictable when the seed is known.
3. Its internal state can be reconstructed from sufficient output.
4. It is not designed to resist cryptographic attacks.
5. Weak seeds, such as timestamps, can be brute-forced.

## Known Plaintext Attack Explanation

If the attacker knows the plaintext and ciphertext:

Keystream = Plaintext XOR Ciphertext

Knowing 14 consecutive A characters reveals 14 consecutive keystream bytes.

The attacker can test candidate seeds until the generated keystream matches the known bytes.

## Why Timestamp-Based Seeding Is Vulnerable

Unix timestamps represent the number of seconds since January 1, 1970.

If a generator is seeded with the current timestamp, an attacker can estimate the generation time and test nearby timestamps.

This drastically reduces the seed search space.

## Pseudocode

### Seed Recovery

```text
FOR seed = 0 TO 65535:

    Generate keystream using seed

    Search for known 14-byte sequence

    IF matching sequence is found:

        Decrypt complete ciphertext

        Verify plaintext

        Return recovered seed

END FOR
```

### Timestamp Prediction

```text
FOR timestamp = T-300 TO T+300:

    Generate 16-byte token using timestamp

    Compare candidate token with observed token

    IF tokens match:

        Save matching timestamp

END FOR

Regenerate token using recovered timestamp

Verify token
```

## How to Run

Install NumPy:

```bash
pip install numpy
```

Execute:

```bash
python mt19937_attack.py
```

## Expected Output

- Encryption and decryption results.
- Original plaintext and ciphertext.
- Original 16-bit seed.
- Recovered seed.
- Complete decrypted plaintext.
- Verification of the known 14-character sequence.
- Generated 16-byte reset token.
- Original Unix timestamp.
- Timestamp search interval.
- Number of timestamps tested.
- Token verification.

## Conclusion

The experiment demonstrates that MT19937 is unsuitable for cryptographic applications.

In Part A, a weak 16-bit seed can be recovered using a known plaintext sequence and brute-force search.

In Part B, timestamp-based seeding makes simulated reset tokens predictable because an attacker can search a limited timestamp interval.

Cryptographic applications should use dedicated cryptographically secure random-number generators instead of statistical PRNGs such as MT19937.
