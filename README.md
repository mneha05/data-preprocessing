# Data Preprocessing — Clean, Fast, Reproducible Pipelines

![status](https://img.shields.io/badge/status-ready-brightgreen) ![python](https://img.shields.io/badge/python-3.8%2B-blue)

Compact, production-ready data preprocessing utilities demonstrating robust feature engineering, normalization, and signal transforms using NumPy, SciPy and pandas. Designed to be reproducible, well-documented, and ready to integrate into GPU-accelerated training pipelines.

Key features
- Reproducible feature normalization and scaling pipelines
- Signal transforms (STFT) examples for time-series data
- Save/load compressed NumPy artifacts for efficient downstream training
- Easy to containerize for consistent preprocessing at scale

Tech
- Python, NumPy, SciPy, pandas

Quickstart

```powershell
python -m pip install -r requirements.txt
python preprocess.py sample.csv artifacts/preprocessed.npz
```

Demo GIF (replace with captured workflow):

![preprocess-demo](./assets/preprocess_demo.gif)

Processing pipeline diagram

```mermaid
flowchart TD
	A[Raw CSV] --> B[Load with pandas]
	B --> C[Numeric selection]
	C --> D[Normalize (mean/std)]
	D --> E[STFT]
	E --> F[Save .npz artifacts]
```

Why this impresses recruiters
- Clear, reproducible steps showing data hygiene and signal processing knowledge
- Ready-to-integrate artifacts for GPU training workflows

License: MIT

