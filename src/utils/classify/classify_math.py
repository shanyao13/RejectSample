import json
import os

from gpt_o3_service import getMathclassFromO3


def classify_math_problems(input_file, output_dir):
    # 创建 output 目录（如果不存在的话）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 准备一个字典来存储每个类别的内容
    categories = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}

    # 读取 input.jsonl 文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            try:
                # 解析每一行的 JSON 数据
                data = json.loads(line.strip())
        
                # content = data.get("input", [{}])[0].get("content", "")
                content = data.get('question', '')
                if not content:
                    raise ValueError(f"format is wrong, you need to modify...")

                
                if content:
                    # 使用 getMathclassFromO3 获取分类结果
                    category = int(getMathclassFromO3(content))
                    
                    # 将该问题按类别存入字典
                    categories[category].append(data)
            except json.JSONDecodeError:
                print(f"跳过无效的 JSON 行: {line}")

    # 保存每个类别的数据到对应的 JSONL 文件
    for category, items in categories.items():
        if items:
            category_name = category_names[category]  # 获取类别名称
            output_file = os.path.join(output_dir, f'{category_name}.jsonl')
            with open(output_file, 'a', encoding='utf-8') as outfile:                    # 旧文件追加，‘a’；如果要清空并重新写入，改为'w'
                for item in items:
                    json.dump(item, outfile, ensure_ascii=False)
                    outfile.write('\n')
            print(f"保存 {len(items)} 条数据到 {output_file}.")

# 类别名称映射字典
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

# 使用示例
input_file = '/Users/shanyao/zjlWorkSpace/LLM/projectDir/RejectSample/data/input/train_test.jsonl'  # 输入的 JSONL 文件路径
output_dir = './output'       # 输出目录

classify_math_problems(input_file, output_dir)
