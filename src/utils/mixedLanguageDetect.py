import fasttext
from config.constant import Constant

"""
用于检测文本是否混杂多种语言。
输入：txt path
输出：[],[] 分别是语言和probabilities
"""
# 加载语言识别模型
model = fasttext.load_model(Constant.MODEL_DIR)

def is_mixed_language(text)->bool:
    # prediction = model.predict(text)
    # labels, probs = model.predict(text.strip().replace("\n", " "), k=2)  # 去除换行符
    label, prob = model.predict(text.strip().replace("\n", " "))
    if prob < 0.7:
        return True   # 表示混有多种语言
    else:
        return False 

# # 每行检测语言
# with open(Constant.FastText_path, "r", encoding="utf-8") as f:
#     for i, line in enumerate(f):
#         if line.strip():  # 忽略空行
#             labels, probs = is_mixed_language(line)
#             print(f"[Line {i+1}] Language: {labels}, Confidence: {probs}")