from openai import OpenAI

from config.ApiKey import API_KEY_4o

# 放在全局，初始化一次
client = OpenAI(
    base_url="https://openai.sohoyo.io/v1",
    api_key= API_KEY_4o
)

def getMathclassFrom4o(question):
    prompt = f"""You are a math classifier. Given a math problem, classify it strictly into one of the following categories by returning the corresponding number only. Do NOT output anything else — just the number.

            Category codes: 
            1: linear algebra  
            2: calculus  
            3: probability  
            4: statistics  
            5: differential equations  
            6: discrete mathematics  
            7: differential geometry
            0: others 

            Input: {question}

            Output (only a single digit from 0 to 7, no explanation):"""
    
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    # print("response: " + response.choices[0].message.content)

    return response.choices[0].message.content


