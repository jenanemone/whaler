from collections import Counter

INPUT_FILE = 'pools_target_cities_feb26/maricopa_master_residential.txt'

def count_pipe_variances():
    print("📊 Scanning file for pipe delimiter consistency...")
    pipe_counts = Counter()
    total_lines = 0
    
    with open(INPUT_FILE, 'r', encoding='latin1') as f:
        for line in f:
            total_lines += 1
            # Count occurrences of the pipe character
            count = line.count('|')
            pipe_counts[count] += 1
            
            if total_lines % 500000 == 0:
                print(f"Scanned {total_lines} lines...")

    print("\n--- PIPE COUNT RESULTS ---")
    print(f"Total Lines Scanned: {total_lines}")
    print(f"{'Pipes':<10} | {'Frequency':<15}")
    print("-" * 30)
    
    # Sort by frequency (most common counts first)
    for count, freq in pipe_counts.most_common():
        percentage = (freq / total_lines) * 100
        print(f"{count:<10} | {freq:<15} ({percentage:.2f}%)")

if __name__ == "__main__":
    count_pipe_variances()