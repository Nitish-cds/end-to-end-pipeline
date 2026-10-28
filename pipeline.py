import os
import csv
from collections import Counter

# ==========================================
# PIPELINE PARAMETERS (Configurable)
# ==========================================
INPUT_FASTA = "input.fasta"
OUTPUT_DIR = "results"
MIN_SEQ_LENGTH = 25  # Minimum base pairs to keep a sequence

# Intermediate and final output filenames
INTERMEDIATE_FASTA = "01_filtered.fasta"
INTERMEDIATE_CSV = "02_frequencies.csv"
FINAL_REPORT = "03_summary_report.txt"
# ==========================================

def step1_filter_sequences(input_path, output_path, min_length):
    """Reads FASTA, filters by length, and writes an intermediate FASTA."""
    print(f"Step 1: Filtering sequences shorter than {min_length} bp...")
    kept_sequences = 0
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        header = ""
        seq = []
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                if header and len("".join(seq)) >= min_length:
                    outfile.write(f"{header}\n{''.join(seq)}\n")
                    kept_sequences += 1
                header = line
                seq = []
            else:
                seq.append(line)
        # Check last sequence
        if header and len("".join(seq)) >= min_length:
            outfile.write(f"{header}\n{''.join(seq)}\n")
            kept_sequences += 1
    print(f"  -> Saved {kept_sequences} sequences to {output_path}")

def step2_calculate_frequencies(input_path, output_path):
    """Reads filtered FASTA, calculates nucleotide frequencies, writes to CSV."""
    print("Step 2: Calculating nucleotide frequencies...")
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sequence_ID", "Length", "A", "T", "G", "C"])
        
        header = ""
        seq = []
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    full_seq = "".join(seq).upper()
                    counts = Counter(full_seq)
                    writer.writerow([header[1:], len(full_seq), counts.get('A',0), counts.get('T',0), counts.get('G',0), counts.get('C',0)])
                header = line
                seq = []
            else:
                seq.append(line)
        # Check last sequence
        if header:
            full_seq = "".join(seq).upper()
            counts = Counter(full_seq)
            writer.writerow([header[1:], len(full_seq), counts.get('A',0), counts.get('T',0), counts.get('G',0), counts.get('C',0)])
    print(f"  -> Saved frequencies to {output_path}")

def step3_generate_report(input_path, output_path):
    """Reads the CSV and generates a final summary report."""
    print("Step 3: Generating final summary report...")
    total_seqs = 0
    total_length = 0
    
    with open(input_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_seqs += 1
            total_length += int(row["Length"])
            
    avg_length = total_length / total_seqs if total_seqs > 0 else 0
    
    with open(output_path, 'w') as outfile:
        outfile.write("PIPELINE SUMMARY REPORT\n")
        outfile.write("=======================\n")
        outfile.write(f"Total sequences processed: {total_seqs}\n")
        outfile.write(f"Average sequence length:   {avg_length:.1f} bp\n")
        outfile.write(f"Total bases analyzed:      {total_length} bp\n")
        outfile.write("Pipeline completed successfully.\n")
    print(f"  -> Saved final report to {output_path}")

def main():
    print("Starting Analysis Pipeline...")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    path_filtered = os.path.join(OUTPUT_DIR, INTERMEDIATE_FASTA)
    path_csv = os.path.join(OUTPUT_DIR, INTERMEDIATE_CSV)
    path_report = os.path.join(OUTPUT_DIR, FINAL_REPORT)

    try:
        # Chain the steps together
        step1_filter_sequences(INPUT_FASTA, path_filtered, MIN_SEQ_LENGTH)
        step2_calculate_frequencies(path_filtered, path_csv)
        step3_generate_report(path_csv, path_report)
        print("\nPipeline finished successfully!")
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")

if __name__ == "__main__":
    main()