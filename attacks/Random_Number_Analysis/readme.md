
# Random Number Generation and Statistical Analysis

## Objective

To evaluate operating-system random-number generation mechanisms and investigate their suitability for cryptographic applications.

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- OpenSSL
- Windows CNG API
- Linux /dev/urandom
- Windows Subsystem for Linux (WSL)

## Project Structure

```text
Random_Number_Analysis/
│
├── random_analysis.py
├── README.md
│
└── random_data/
    ├── windows_cng.bin
    ├── openssl_rand.bin
    └── linux_urandom.bin
```

## Random Number Generation Mechanisms

### 1. Linux /dev/urandom

- Uses the Linux kernel random-number generator.
- Generates cryptographically secure pseudorandom bytes.
- Random data is generated using the `/dev/urandom` interface.
- 1 MB of random data is generated.

### 2. OpenSSL RAND

- Uses OpenSSL's random-number generation facility.
- Uses a Deterministic Random Bit Generator (DRBG).
- Generates cryptographically secure random bytes.
- Data is generated using the `openssl rand` command.

### 3. Windows CNG

- Uses Windows Cryptography API: Next Generation.
- Uses the `BCryptGenRandom()` function.
- Uses the system-preferred cryptographic random provider.
- Generates 1 MB of random data.

## Statistical Tests Performed

### 1. Byte Frequency Distribution

Checks the frequency of all 256 possible byte values (0–255).

### 2. Chi-Square Test

Checks whether the observed byte-frequency distribution significantly differs from a uniform distribution.

### 3. Bit Distribution Test

Checks whether the number of zero and one bits is approximately equal.

### 4. Repeated Pattern Detection

Checks repeated consecutive blocks of 2, 4, and 8 bytes.

### 5. Serial Correlation Test

Measures the correlation between consecutive bytes.

### 6. Runs Test

Checks the distribution of consecutive sequences of identical bits.

## Requirements

Install the required Python libraries:

```bash
pip install numpy pandas matplotlib scipy
```

Additional requirements:

- Python 3 installed on Windows.
- OpenSSL installed and available in PATH.
- WSL with Ubuntu installed for generating Linux random data.

## How to Run

Open Command Prompt inside the project directory.

Execute:

```bash
python random_analysis.py
```

The program automatically:

1. Generates random data using Windows CNG.
2. Generates random data using OpenSSL.
3. Generates Linux random data using WSL.
4. Loads all generated binary files.
5. Performs statistical tests.
6. Displays byte-frequency graphs.
7. Displays the final comparison table.

## Expected Output

- Three binary files containing 1 MB of random data each.
- Byte-frequency distribution graphs.
- Chi-square test results.
- Bit distribution results.
- Repeated pattern detection results.
- Serial correlation values.
- Runs test results.
- Final comparison table.

## Comparison

| Feature | Linux | OpenSSL | Windows |
|---|---|---|---|
| Mechanism | /dev/urandom | RAND | CNG |
| Generator | Kernel CSPRNG | DRBG | System DRBG |
| Interface | Device file | Command line | API |
| Cryptographic use | Yes | Yes | Yes |

## Why Statistical Tests Cannot Guarantee Security

Statistical tests examine the distribution and patterns of random data.

However, a generator may pass statistical tests while still being predictable if its internal state or seed is compromised.

Cryptographic security also depends on:

- Entropy collection
- Secure initialization
- Internal state protection
- Resistance to prediction attacks

Therefore, passing statistical tests does not guarantee cryptographic security.

## Conclusion

Random data was generated using Linux /dev/urandom, OpenSSL RAND, and Windows CNG.

The generated data was evaluated using different statistical tests to analyze byte frequencies, bit distributions, repeated patterns, and serial correlations.

The experiment demonstrates that statistical randomness and cryptographic security are different concepts. Statistical tests help identify randomness-related weaknesses but cannot independently prove that a random-number generator is cryptographically secure.
