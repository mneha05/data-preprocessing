import sys
import numpy as np
import pandas as pd
from scipy import signal

def preprocess(df: pd.DataFrame) -> dict:
    data = df.select_dtypes(include=["number"]).to_numpy(dtype=float)
    mean = data.mean(axis=0)
    std = data.std(axis=0) + 1e-8
    norm = (data - mean) / std
    f, t, Zxx = signal.stft(norm[:, 0], nperseg=64)
    return {"normalized": norm, "stft_freqs": f, "stft_times": t, "stft": Zxx}

def main():
    if len(sys.argv) < 3:
        print("usage: preprocess.py input.csv output.npz")
        sys.exit(1)
    df = pd.read_csv(sys.argv[1])
    out = preprocess(df)
    np.savez_compressed(sys.argv[2], **out)
    print("Wrote:", sys.argv[2])

if __name__ == '__main__':
    main()
