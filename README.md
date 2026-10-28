# End-to-End Sequence Analysis Pipeline

This repository contains an automated, multi-step pipeline for analyzing FASTA sequence data. It is fully reproducible with a single command from a clean checkout.

## Pipeline Steps
1. **Filtering:** Reads raw sequence data and removes sequences below a minimum length threshold. Generates an intermediate filtered FASTA file.
2. **Analysis:** Calculates the base pair length and exact nucleotide frequencies (A, T, G, C) for the filtered sequences. Saves this data as an intermediate CSV.
3. **Reporting:** Reads the CSV output and generates a human-readable final summary report of the processed data.

## How to Run
This pipeline has **zero external dependencies** and uses only the Python Standard Library. 

Simply execute the main script from your terminal:
```bash
python pipeline.py