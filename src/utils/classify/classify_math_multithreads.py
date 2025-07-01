import json
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from gpt_4o_service import getMathclassFrom4o

category_names = {
    0: 'others',
    1: 'linear_algebra',
    2: 'calculus',
    3: 'probability',
    4: 'statistics',
    5: 'differential_equations',
    6: 'discrete_mathematics',
    7: 'differential_geometry'
}

# 如果 API 有 QPS 限制，可限制同时活跃线程数
semaphore = threading.Semaphore(10)  # 限制同时最多10个请求

def classify_and_write(data, file_handles, locks, line_num):
    content = data.get('question', '')
    if not content:
        print(f"[Line {line_num}] ❌ 缺少 'question' 字段")
        return

    try:
        with semaphore:
            category = int(getMathclassFrom4o(content))

        if category not in category_names:
            print(f"[Line {line_num}] ❌ 无效分类编号: {category}")
            return

        with locks[category]:  # 写入加锁
            json.dump(data, file_handles[category], ensure_ascii=False)
            file_handles[category].write('\n')

    except Exception as e:
        print(f"[Line {line_num}] ❌ 分类失败: {e}")

def classify_math_problems_threaded(input_file, output_dir, max_workers=32):
    os.makedirs(output_dir, exist_ok=True)

    # 打开输出文件 & 加锁
    file_handles = {}
    locks = {}
    for cat, name in category_names.items():
        output_path = os.path.join(output_dir, f"{name}.jsonl")
        file_handles[cat] = open(output_path, 'a', encoding='utf-8')
        locks[cat] = threading.Lock()

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             ThreadPoolExecutor(max_workers=max_workers) as executor:

            futures = []
            for line_num, line in enumerate(infile, 1):
                try:
                    data = json.loads(line.strip())
                    futures.append(
                        executor.submit(classify_and_write, data, file_handles, locks, line_num)
                    )
                except json.JSONDecodeError:
                    print(f"[Line {line_num}] ❌ JSON 格式错误: {line.strip()}")

            # 等待所有任务完成
            for future in as_completed(futures):
                _ = future.result()

    finally:
        for f in file_handles.values():
            f.close()



input_file = '/Users/shanyao/zjlWorkSpace/LLM/projectDir/RejectSample/data/input/train_test.jsonl'
output_dir = './output_multi_thread'
classify_math_problems_threaded(input_file, output_dir)