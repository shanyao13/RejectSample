# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
from config.constant import Constant

from mathruler.grader import extract_boxed_content, grade_answer
from utils.logger import logger


def format_reward(predict_str: str) -> float:
    pattern = re.compile(r"<think>.*</think>.*\\boxed\{.*\}.*", re.DOTALL)
    match_result = re.fullmatch(pattern, predict_str)
    return 1.0 if match_result else 0.0


def acc_reward(predict_str: str, ground_truth: str) -> float:
    answer = extract_boxed_content(predict_str)
    return 1.0 if grade_answer(answer, ground_truth) else 0.0


def compute_score(predict_str: str, ground_truth: str) -> float:
    return 0.9 * acc_reward(predict_str, ground_truth) + 0.1 * format_reward(predict_str)


# Q = "Which of the following statements is (are) correct? (x) The opportunity cost of the first 50 tables is 400 chairs and the opportunity cost of the first 800 chairs is 20 tables. (y) If the economy produces 80 tables and 800 chairs instead of 50 tables and 1,400 chairs, then the opportunity cost of the 30 additional tables is 600 chairs. (z) The opportunity cost of the 200th chair is equal to 1/40th of a table and the opportunity cost of the 30th table is more than 8 chairs but less than 10 chairs. a. (x), (y) and (z) b. (x) and (y), only c. (x) and (z), only d. (y) and (z), only e. (x) only Production Possibilities Tables Chairs 100 0 80 800 50 1,400 0 1,800"

# # predict_str = "To determine which statements are correct, we analyze the production possibilities table and calculate the opportunity costs: 1. **Statement (x):** - The opportunity cost of the first 50 tables: Starting from 0 tables and 1,800 chairs, producing 50 tables requires giving up 400 chairs (1,800 - 1,400). Thus, the opportunity cost is 400 chairs. - The opportunity cost of the first 800 chairs: Starting from 100 tables and 0 chairs, producing 800 chairs requires giving up 20 tables (100 - 80). Thus, the opportunity cost is 20 tables. - Both parts of statement (x) are correct. 2. **Statement (y):** - Moving from 50 tables and 1,400 chairs to 80 tables and 800 chairs: The economy produces 30 additional tables and gives up 600 chairs (1,400 - 800). The opportunity cost of 30 additional tables is 600 chairs. - This part of statement (y) is correct. 3. **Statement (z):** - Opportunity cost of the 200th chair: Moving from 100 tables to 80 tables, each chair costs \( \frac{1}{40} \) of a table (20 tables / 800 chairs). The 200th chair in this segment costs \( \frac{1}{40} \) of a table, which is correct. - Opportunity cost of the 30th table: Moving from 80 tables to 50 tables, each table costs 20 chairs. However, the statement claims it is more than 8 but less than 10 chairs, which is incorrect. - Since the second part of statement (z) is incorrect, the entire statement (z) is incorrect. Thus, the correct statements are (x) and (y). The answer is \(\boxed{b}\)."

# filePath = os.path.join(Constant.INPUT_DIR, "answers.jsonl")
# with open(filePath, 'r', encoding='utf-8') as f:
#     for line in f:
#         data = json.loads(line)
#         for i in range(0,6):
#             predict_str =  data.get("answers")[i]
#             ground_truth = "b"

#             score = compute_score(predict_str, ground_truth)
#             # print(f"Answer {i} , score: {score}")
#             logger.info(f"Answer {i} , score: {score}")
