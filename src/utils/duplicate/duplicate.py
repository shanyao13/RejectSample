import hashlib
import zstandard as zstd
import json
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
import os
import io
import argparse

def get_ngrams(text, n=5):
    text = text.lower().replace('\n', ' ').replace('\r', ' ')
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    tokens = text.split()
    ngrams = set()
    for token in tokens:
        if len(token) < n:
            ngrams.add(token)
        else:
            for i in range(len(token) - n + 1):
                ngrams.add(token[i:i+n])
    return ngrams

def create_minhash(ngrams, num_perm=128):
    m = MinHash(num_perm=num_perm)
    for gram in ngrams:
        m.update(gram.encode('utf8'))
    return m

def hash_text_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def deDuplication(inputFilePath, outputFileDir, num_perm, threshold):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError(f"❌ 输入文件不存在: {inputFilePath}")
    # dctx = zstd.ZstdDecompressor()

    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

    seen_hashes = set()
    content_to_lines = {}  # md5 hash -> list of line numbers

    total_size = os.path.getsize(inputFilePath)
    count_all = 0
    count_unique = 0

    os.makedirs(outputFileDir, exist_ok=True)
    filename = os.path.basename(inputFilePath)
    # 去掉多个后缀（ .jsonl.zst）
    if filename.endswith('.jsonl.zst'):
        name = filename[:-len('.jsonl.zst')]
    elif filename.endswith('.jsonl'):
        name = os.path.splitext(filename)[0] #去掉文件后缀名
    else:
        raise ValueError(f"❌ 输入文件格式必须是.jsonl.zst或.jsonl")
    outPutFilePath = os.path.join(outputFileDir, name + ".dedup.jsonl")

    duplicatesFile = os.path.join(outputFileDir, name + ".dup.jsonl")   
    duplicatesInfo = os.path.join(outputFileDir, name + ".dupInfo.txt")   #记录重复信息，如第几行和第几行重复/相似

    duplicates_file = open(duplicatesFile, 'w', encoding='utf-8')
    duplicates_info = open(duplicatesInfo, 'w', encoding='utf-8')

    with open(inputFilePath, 'rb') as f, open(outPutFilePath, 'w', encoding='utf-8') as out_f:
        # stream = dctx.stream_reader(f)
        # text_stream = io.TextIOWrapper(stream, encoding='utf-8')
        if inputFilePath.endswith('.zst'):
            dctx = zstd.ZstdDecompressor()
            stream = dctx.stream_reader(f)
            text_stream = io.TextIOWrapper(stream, encoding='utf-8')
        else:
            text_stream = io.TextIOWrapper(f, encoding='utf-8')

        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Processing") as pbar:
            for line in text_stream:
                count_all += 1
                pbar.update(len(line.encode('utf-8')))

                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    content = data['input'][0]['content']    # 这里需要根据匹配内容字段修改！！！
                    # content = data['messages'][1]['content']     # 提取内容
                except Exception as e:
                    print(f"Error parsing line {count_all}: {e}")
                    continue

                md5 = hash_text_md5(content)
                if md5 in seen_hashes:
                    # 完全重复
                    content_to_lines.setdefault(md5, []).append(count_all)
                    duplicates_file.write(json.dumps(data, ensure_ascii=False) + '\n')
                    duplicates_info.write(f"Line {count_all} is exact duplicate of line(s) {content_to_lines[md5][0]}\n")
                    continue

                seen_hashes.add(md5)
                content_to_lines[md5] = [count_all]

                ngrams = get_ngrams(content, n=5)
                m = create_minhash(ngrams, num_perm=num_perm)

                result = lsh.query(m)
                if len(result) == 0:
                    lsh.insert(f"item{count_all}", m)
                    out_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    count_unique += 1
                else:
                    # 相似重复
                    duplicates_file.write(json.dumps(data, ensure_ascii=False) + '\n')
                    duplicates_info.write(f"Line {count_all} is similar to line(s): {[int(item[4:]) for item in result]}\n")

                if count_all % 10000 == 0:
                    pbar.set_postfix(processed=count_all, unique=count_unique)

    duplicates_file.close()
    duplicates_info.close()

    print(f"Total processed: {count_all}, Unique records: {count_unique}")

def main():
    parser = argparse.ArgumentParser(description="n_gram 去重/相似工具")

    parser.add_argument('--input_path', type=str, required=True, help='输入文件路径（.jsonl.zst或.jsonl）')
    parser.add_argument('--output_dir', type=str, required=True, help='去重后输出目录')
    parser.add_argument('--num_perm', type=int, default=64, help='num_perm 参数，默认64')
    parser.add_argument('--threshold', type=float, default=0.95, help='阈值，默认0.95')

    args = parser.parse_args()

    deDuplication(
        inputFilePath=args.input_path,
        outputFileDir=args.output_dir,
        num_perm=args.num_perm,
        threshold=args.threshold
    )

if __name__ == '__main__':
    main()

