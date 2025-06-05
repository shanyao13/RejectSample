import json
from utils.logger import logger


def strToJson(scores: str):
    # 移除前7个字符和后3个字符
    # modified_scores = scores[7:-3]
    modified_scores = scores
    # print(f"modified_scores: {modified_scores}")

    # 将剩余的字符串转换为JSON
    try:
        scores_json = json.loads(modified_scores)
        # print(f"转换后的JSON: {scores_json}")
        return scores_json
    except json.JSONDecodeError as e:
        # print(f"JSON解析错误: {e}")
        logger.error(f"JSON解析错误: {e}")

# # 示例：原始的scores字符串
# scores = '''json[{"id":123, "scores":[1,2,3]}, {"id":124, "scores":[4,5,6]}]'''  # 这是一个示例字符串
# strToJson(scores)
