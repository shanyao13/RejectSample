import requests
import json

url = "http://10.200.92.162:8081/run_code"

def code_box_util(code_exe, stdin_data):
    payload = json.dumps({
        "compile_timeout": 10,
        "run_timeout": 10,
        "code": code_exe,
        "stdin": stdin_data,
        "language": "cpp",
        "files": {}
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        print(f"❌ 请求出错: {e}")
        return None
