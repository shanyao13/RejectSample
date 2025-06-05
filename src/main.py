import json
import os
from config.constant import Constant
# from utils.filterLongAnswer import is_too_long
from services.scoresFromDS import getScoresFromDS
from utils.mixedLanguageDetect import is_mixed_language
from utils.reward_score.geo3k import compute_score
from utils.logger import logger


def is_low_quality(rlAnswersPath, trainPath, outputPath):

    output_dir = os.path.dirname(outputPath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = []
    with open(rlAnswersPath, 'r', encoding='utf-8') as f1, open(trainPath, 'r', encoding='utf-8') as f2:
        round = 1
        for line1, line2 in zip(f1, f2):
            # print(f"this is the {round} th round")
            logger.info(f"This is the {round} th question.")
            data1 = json.loads(line1)
            data2 = json.loads(line2)

            question = data1.get("question")
            answers = data1.get("answers", [])
            ground_truth = data2.get("answer")

            scored_candidates = []
            for i, answer in enumerate(answers[:6]):
                # 1、判断每个answer是否正确
                score = compute_score(answer, ground_truth)
                logger.info(f"The {i} th answer's score is: {score}.")
                if score < 1:
                    scored_candidates.append((answer, 0, "the answer is wrong"))
                    continue
                # # 2、判断answer是否太长，默认1024
                # if is_too_long(answer):
                #     scored_candidates.append((answer, 0, "the answer is too long"))
                #     continue
                # 3、判断是否混有其他语言
                if is_mixed_language(answer):
                    scored_candidates.append((answer, 0, "the answer is mixed many languages"))
                    logger.info(f"The {i} th answer is mixed many languages.")
                    continue
                # 3、判断code block  --

                # 4、DeepSeek 打分（这是主要的排序指标）
                try:
                    score = getScoresFromDS(question, answer)   #调用deepseek接口
                    scored_candidates.append((answer, score[0].get("score"), score[0].get("reason")))
                    logger.info(f"The {i} th answer getScoresFromDS, score: {score[0].get('score')}, reason: {score[0].get('reason')}.")                  
                except Exception as e:
                    # print(f"Error scoring answer {i}: {e}")
                    logger.error(f"Error scoring answer {i}: {e}")
                    continue

            # 按分数降序排序，选择最佳（必须6选1）
            if scored_candidates:
                best_answer, best_score, reason = sorted(scored_candidates, key=lambda x: x[1], reverse=True)[0]
                results.append({"question": question, "answer": best_answer, "best_sacore": best_score, "reason": reason})
            else:
                # print(f"No valid answers for question: {question}")
                logger.error(f"No valid answers for question: {question}")
            round += 1

    # 写入最终文件
    with open(outputPath, 'w', encoding='utf-8') as fout:
        for item in results:
            fout.write(json.dumps(item, ensure_ascii=False) + '\n')



    # return (
    #     is_mixed_language(think) or
    #     is_too_long(think, max_tokens=256) or
    #     contains_code_block(think)
    # )

# trainPath = "/mnt/cpfs/users/lfu/llm/datasets/reasoning/WebInstruct-verified/data/train.jsonl"
trainPath = os.path.join(Constant.INPUT_DIR, "train_test.jsonl")    # train_test-phd.jsonl
rlAnswersPath = os.path.join(Constant.INPUT_DIR, "answers.jsonl")  # answers_test-phd.jsonl
outputPath = os.path.join(Constant.OUTPUT_DIR, "best_answer.jsonl")  # best_answer_test-phd.jsonl
is_low_quality(rlAnswersPath, trainPath, outputPath)



