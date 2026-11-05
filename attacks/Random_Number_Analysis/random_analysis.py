
import os
import sys
import ctypes
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import chisquare, binomtest, norm

SIZE = 1024 * 1024

os.makedirs("random_data", exist_ok=True)

files = {
    "Windows CNG": "random_data/windows_cng.bin",
    "OpenSSL rand": "random_data/openssl_rand.bin",
    "Linux urandom": "random_data/linux_urandom.bin"
}

# 1. Generate random data using Windows CNG

def generate_windows():

    buffer = (ctypes.c_ubyte * SIZE)()

    bcrypt = ctypes.WinDLL("bcrypt.dll")

    bcrypt.BCryptGenRandom.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_ulong,
        ctypes.c_ulong
    ]

    bcrypt.BCryptGenRandom.restype = ctypes.c_long

    status = bcrypt.BCryptGenRandom(
        None,
        buffer,
        SIZE,
        0x00000002
    )

    if status != 0:
        raise RuntimeError("Windows CNG generation failed")

    with open(files["Windows CNG"], "wb") as f:
        f.write(bytes(buffer))

    print("Windows CNG data generated successfully")


# 2. Generate random data using OpenSSL

def generate_openssl():

    try:
        subprocess.run(
            [
                "openssl",
                "rand",
                "-out",
                files["OpenSSL rand"],
                str(SIZE)
            ],
            check=True
        )

        print("OpenSSL data generated successfully")

    except FileNotFoundError:
        print("OpenSSL not found. Please install OpenSSL.")

    except subprocess.CalledProcessError:
        print("OpenSSL generation failed.")


# 3. Generate Linux random data using WSL

def generate_linux():

    try:
        subprocess.run(
            [
                "wsl",
                "sh",
                "-c",
                "head -c 1048576 /dev/urandom"
            ],
            stdout=open(files["Linux urandom"], "wb"),
            check=True
        )

        print("Linux /dev/urandom data generated successfully")

    except (FileNotFoundError, subprocess.CalledProcessError):
        print("WSL unavailable. Linux data must be copied manually.")


# 4. Generate all random data

generate_windows()
generate_openssl()
generate_linux()


# 5. Load random data

data = {}

for name, path in files.items():

    if os.path.exists(path):

        with open(path, "rb") as f:
            content = f.read()

        if len(content) == SIZE:
            data[name] = np.frombuffer(content, dtype=np.uint8)

            print(name, ":", len(content), "bytes loaded")

        else:
            print(name, "has incorrect file size")

    else:
        print(name, "file not found")


# 6. Byte frequency distribution

print("\n========== BYTE FREQUENCY ==========")

for name, arr in data.items():

    freq = np.bincount(arr, minlength=256)

    plt.figure(figsize=(10, 4))
    plt.bar(range(256), freq)

    plt.title(name + " - Byte Frequency")
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

    print("\n", name)
    print("Minimum:", freq.min())
    print("Maximum:", freq.max())
    print("Expected:", len(arr) / 256)


# 7. Chi-square test

print("\n========== CHI-SQUARE TEST ==========")

for name, arr in data.items():

    freq = np.bincount(arr, minlength=256)

    expected = np.full(256, len(arr) / 256)

    chi, p = chisquare(freq, expected)

    print("\n", name)
    print("Chi-square:", chi)
    print("P-value:", p)

    if p > 0.05:
        print("No significant deviation from uniformity")
    else:
        print("Significant deviation from uniformity")


# 8. Bit distribution test

print("\n========== BIT DISTRIBUTION ==========")

for name, arr in data.items():

    bits = np.unpackbits(arr)

    zeros = np.sum(bits == 0)
    ones = np.sum(bits == 1)

    p = binomtest(ones, len(bits), 0.5).pvalue

    print("\n", name)
    print("Total bits:", len(bits))
    print("Zeros:", zeros)
    print("Ones:", ones)
    print("Percentage of ones:", ones / len(bits) * 100)
    print("P-value:", p)


# 9. Repeated pattern detection

print("\n========== REPEATED PATTERN TEST ==========")

for name, arr in data.items():

    print("\n", name)

    for size in [2, 4, 8]:

        blocks = arr[:len(arr) - len(arr) % size]
        blocks = blocks.reshape(-1, size)

        unique = len(np.unique(blocks, axis=0))
        total = len(blocks)

        print("Block size:", size)
        print("Total blocks:", total)
        print("Unique blocks:", unique)
        print("Repeated blocks:", total - unique)


# 10. Serial correlation

print("\n========== SERIAL CORRELATION ==========")

for name, arr in data.items():

    correlation = np.corrcoef(
        arr[:-1].astype(float),
        arr[1:].astype(float)
    )[0, 1]

    print("\n", name)
    print("Serial correlation:", correlation)


# 11. Runs test

print("\n========== RUNS TEST ==========")

for name, arr in data.items():

    bits = np.unpackbits(arr).astype(int)

    n = len(bits)
    n1 = np.sum(bits)
    n0 = n - n1

    runs = 1 + np.sum(bits[1:] != bits[:-1])

    expected = 1 + (2 * n0 * n1) / n

    variance = (
        2 * n0 * n1 * (2 * n0 * n1 - n)
    ) / (n**2 * (n - 1))

    z = (runs - expected) / np.sqrt(variance)

    p = 2 * norm.sf(abs(z))

    print("\n", name)
    print("Observed runs:", runs)
    print("Expected runs:", expected)
    print("Z-score:", z)
    print("P-value:", p)

    if p > 0.05:
        print("No significant deviation")
    else:
        print("Significant deviation")


# 12. Final comparison

print("\n========== FINAL COMPARISON ==========")

results = []

for name, arr in data.items():

    freq = np.bincount(arr, minlength=256)

    chi, chi_p = chisquare(freq)

    bits = np.unpackbits(arr)

    ones = np.sum(bits)

    bit_p = binomtest(
        ones,
        len(bits),
        0.5
    ).pvalue

    corr = np.corrcoef(
        arr[:-1].astype(float),
        arr[1:].astype(float)
    )[0, 1]

    results.append({
        "Generator": name,
        "Chi-square P-value": chi_p,
        "Bit Test P-value": bit_p,
        "Serial Correlation": corr
    })

df = pd.DataFrame(results)

print(df.to_string(index=False))


# 13. Final conclusion

print("\n========== FINAL CONCLUSION ==========")

print("Random data generation and analysis completed.")

print("Statistical tests help identify:")
print("1. Non-uniform byte distribution")
print("2. Bit imbalance")
print("3. Repeated patterns")
print("4. Serial correlation")
print("5. Unusual bit runs")

print("\nPassing statistical tests does not guarantee")
print("cryptographic security or unpredictability.")
