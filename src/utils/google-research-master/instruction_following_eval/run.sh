#!/bin/bash
# Copyright 2025 The Google Research Authors.
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



# python3 -m instruction_following_eval.evaluation_main \
#   --input_data=./instruction_following_eval/data/input_data.jsonl \
#   --input_response_data=./instruction_following_eval/data/input_response_data_dsr10528_20250623.jsonl \
#   --output_dir=./instruction_following_eval/data/

# exit 0

# python3 -m instruction_following_eval.evaluation_main \
#   --input_data=./instruction_following_eval/data-test/input_data.jsonl \
#   --input_response_data=./instruction_following_eval/data-test/input_response_data_dsr10528_20250623.jsonl \
#   --output_dir=./instruction_following_eval/data-test/

# exit 0

# python3 -m instruction_following_eval.evaluation_main \
#   --input_data=./instruction_following_eval/data-llama-nemo/input.jsonl \
#   --input_response_data=./instruction_following_eval/data-llama-nemo/input_response_llama_nemo.jsonl \
#   --output_dir=./instruction_following_eval/data-llama-nemo/

# exit 0

python3 -m instruction_following_eval.evaluation_main \
  --input_data=./instruction_following_eval/data-qwen/input.jsonl \
  --input_response_data=./instruction_following_eval/data-qwen/input_response_qwen_processed.jsonl \
  --output_dir=./instruction_following_eval/data-qwen/

exit 0
