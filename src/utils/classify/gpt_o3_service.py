import time
from openai import OpenAI

from config.ApiKey import API_KEY_O3

def getMathclassFromO3(question):
    client = OpenAI(
        base_url="https://openai.sohoyo.io/v1",
        api_key=API_KEY_O3,
    )
    categories = [
         "linear algebra", "calculus", "probability",
        "statistics", "differential equations",
        "discrete mathematics", "differential geometry",
        "others"
        ]
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
    
    response = client.chat.completions.create(model="o3", messages=[{"role": "user", "content": prompt}])
    # print(response.choices[0].message.content)

    # return response
    return response.choices[0].message.content

# question = "Solve the following math problem. Make sure to put the answer (and only answer) inside \\boxed{}.\n\nSketch the graph of the function $g(x) = \\ln(x^5 + 5) - x^3$."
# question = "Solve the equation on $\\mathbb{R}$\n\\[ (1+x^2)(2+x)\\sqrt{1+2\\sqrt{x+2}}=(1+\\frac{3}{x})\\sqrt[4]{x+2}\\"

# question = "1 + 8 = ?"
# start = time.time()
# getMathclassFromO3(question)
# end = time.time()
# cost = end - start
# print(f"cost time for one prompt: {cost}")