import json

def clean_single_kwargs(kwargs):
    if not isinstance(kwargs, dict):
        return {}
    cleaned = {k: v for k, v in kwargs.items() if v is not None}
    return cleaned if cleaned else {}

def clean_kwargs_list(kwargs_list):
    if not isinstance(kwargs_list, list):
        return []
    cleaned_list = []
    for kwargs in kwargs_list:
        cleaned = clean_single_kwargs(kwargs)
        cleaned_list.append(cleaned)
    return cleaned_list


input_file = 'results-gen-ifeval-test-part0005.jsonl'
output_file1 = 'input.jsonl'
output_file2 = 'input_response_llama_nemo_processed.jsonl'


with open(input_file, 'r', encoding='utf-8') as fin, \
     open(output_file1, 'w', encoding='utf-8') as fout1, \
     open(output_file2, 'w', encoding='utf-8') as fout2:
    for line in fin:
        if line.strip():  # 非空行
            data = json.loads(line)
            # 提取字段内容
            custom_id = data.get('custom_id')
            prompt = data.get('prompt')
            instruction_id_list = data.get('args').get('instruction_id_list')
            # instruction_kwargs = data.get('args').get('instruction_kwargs')
            args = data.get('args', {})
            instruction_kwargs_list = args.get('instruction_kwargs', [])
            instruction_kwargs_cleaned = clean_kwargs_list(instruction_kwargs_list)

            response = data.get('solution')



            if prompt is not None:
                # 写入到新文件，保存为json对象格式，只有 prompt 字段
                out_obj = {
                    'key': custom_id,
                    'prompt': prompt,
                    'instruction_id_list': instruction_id_list,
                    'kwargs': instruction_kwargs_cleaned}
                fout1.write(json.dumps(out_obj, ensure_ascii=False) + '\n')

                out_obj_response = {
                    'prompt': prompt,
                    'response': response}
                fout2.write(json.dumps(out_obj_response, ensure_ascii=False) + '\n')


            
