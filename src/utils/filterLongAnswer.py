import json
import os
from transformers import AutoTokenizer

from config.constant import Constant

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-math-7b-instruct")  #这里改为模型所在路径
def is_too_long(text, max_tokens=1024):
    tokens = tokenizer(text, return_tensors="pt").input_ids
    print(f"length: {tokens.shape[1]}")
    return tokens.shape[1] > max_tokens

filePath = os.path.join(Constant.INPUT_DIR, "answers.jsonl")
with open(filePath, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        for i in range(0,6):
            predict_str =  data.get("answers")[i]
            if is_too_long(predict_str):
                print("too long")
            else:
                print("not too long")
