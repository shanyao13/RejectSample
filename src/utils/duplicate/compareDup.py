import hashlib
import json
import os
import io
import argparse
import zstandard as zstd
from tqdm import tqdm

def hash_text_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def load_contents(path):
    contents = []
    is_zst = path.endswith(".zst")
    open_func = lambda p: io.TextIOWrapper(zstd.ZstdDecompressor().stream_reader(open(p, 'rb')), encoding='utf-8') if is_zst else open(p, 'r', encoding='utf-8')
    with open_func(path) as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())
                content = data['messages'][1]['content']
                contents.append((line_num, content))
            except Exception as e:
                print(f"[{path}] Error at line {line_num}: {e}")
    return contents

def compare_exact_duplicates(file1, file2):
    contents1 = load_contents(file1)
    contents2 = load_contents(file2)

    print(f"✅  File 1 contains {len(contents1)} entries")
    print(f"✅  File 2 contains {len(contents2)} entries")

    hash_to_line1 = {}
    for line_num, content in contents1:
        md5 = hash_text_md5(content)
        hash_to_line1[md5] = line_num

    exact_duplicates = []
    for line_num2, content2 in contents2:
        md5 = hash_text_md5(content2)
        if md5 in hash_to_line1:
            exact_duplicates.append((hash_to_line1[md5], line_num2))

    print(f"\n🔁  Exact duplicates found: {len(exact_duplicates)}")
    for d in exact_duplicates:
        print(f"Line {d[1]} in file2 is exact duplicate of line {d[0]} in file1")

def main():
    parser = argparse.ArgumentParser(description="Compare two JSONL files for exact duplicate content")
    parser.add_argument('--file1', type=str, required=True, help='First input JSONL(.zst) file')
    parser.add_argument('--file2', type=str, required=True, help='Second input JSONL(.zst) file')
    args = parser.parse_args()

    compare_exact_duplicates(args.file1, args.file2)

if __name__ == '__main__':
    main()