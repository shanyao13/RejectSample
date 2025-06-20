import json
from testRunCode_request_v2 import code_box_util
import re
import os

def get_codes(file_path, fail_file_path, sucess_file_path):
    dir_path = os.path.dirname(fail_file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # fail_data = []
    with open(file_path, 'r', encoding='utf-8') as f, open(fail_file_path, 'w', encoding = 'utf-8') as fail_f, open(sucess_file_path, 'w', encoding = 'utf-8') as sucess_f:
        for idx, line in enumerate(f):
            print(f"----------idx: {idx}--------")
            try: 
                data = json.loads(line)
                id = data["custom_id"]
                print(f"----------custom_id: {id}--------")
                
                # 1. 代码提取
                code_text = data['response_code']
                code_exe = extract_codes(code_text)

                test_cases = data["test_cases"]
                if isinstance(test_cases, str):
                    try:
                        test_cases = json.loads(test_cases)
                    except json.JSONDecodeError:
                        print(f"❌ test_cases decode error at custom_id: {data.get('custom_id')}")
                        continue
                # 2. 测试用例提取
                inputs = test_cases['inputs']
                outputs = test_cases['outputs']

                for i, input_case in enumerate(inputs[:3]):   # 切片写法，只处理前三个用例
                    # # 只处理前三个用例
                    # if i >= 3:
                    #     break

                    # 3. 输入处理
                    if isinstance(input_case, list):
                        stdin = "\n".join(input_case)
                    else:
                        stdin = input_case.strip()

                    # 4. 期望输出处理
                    output = outputs[i]
                    if isinstance(output, list):
                        expected = "\n".join(output).strip()
                    else:
                        expected = output.strip()

                    # 5. 执行沙盒代码
                    resp = code_box_util(code_exe, stdin)
                    print(resp)

                    if resp is None:
                        print("❌ 运行失败（请求异常）")
                        break
                    elif resp['status'] == 'Failed':
                        print("❌ 运行失败（failed）")
                        # 保存失败的对象，转换成 JSON 字符串写入文件
                        fail_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                        break

                    actual = resp["run_result"]["stdout"]

                    # 6. 对比输出
                    if normalize_output(actual) == normalize_output(expected):
                        print("✅ 结果正确")
                        if i == 2:
                            # 保存成功的对象
                            sucess_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    else:
                        print("❌ 结果错误")
                        print(f"Expected:\n{expected}")
                        print(f"Actual:\n{actual}")
                        break
            except Exception as e:
                print(f"❌ Exception at line {idx}: {e}")


def extract_codes(response_text):
    # 提取 C++ 代码块：从 'Solution Code' 后的 ```cpp 到下一个 ```
    match = re.search(r'Solution Code\s*```cpp\n(.*?)```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def normalize_output(output_str):
    # 去掉多余空格、换行；按行 strip 后再 join
    lines = output_str.strip().splitlines()
    norm = '\n'.join([line.strip() for line in lines if line.strip() != ''])
    return norm

# get_codes('./data_classify/class_cpp.jsonl')
fail_file_path = './data/sanbox_output/fail.jsonl'
sucess_file_path = './data/sanbox_output/sucess.jsonl'
get_codes('/home/zsw/proDir/sandBoxDataProcess/data_classify/class_cpp_not_fn_name.jsonl', fail_file_path, sucess_file_path)
