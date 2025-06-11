# rejectSample


  
一个rejectSample的项目，将指令数据集(通过RL model输出多个回答)，进行一定规则的筛选和deepSeek打分得到最优回答。生成的新的指令数据集，用于SFT。

---

## 🚀 功能特性（Features）

- 具有回答正确性、语言混杂、长段落、代码块判定功能;
- 可调用deepseek等模型，进一步评分;
- 挑选最优RL answer数据作为SFT的训练数据;

---

## 📦 项目结构（Project Structure）

```text
RejectSample
├── README.md
├── config
│   ├── __pycache__
│   │   ├── constant.cpython-310.pyc
│   │   └── dsApiKey.cpython-310.pyc
│   ├── constant.py   #常量，如文件路径
│   └── dsApiKey.py  #模型apiKey
├── data     # 输入输出数据
│   ├── input
│   │   ├── answers.jsonl
│   │   ├── answers2.jsonl
│   │   ├── fastText.txt
│   │   └── train_test.jsonl
│   └── output
│       └── best_answer.jsonl
├── models  #模型文件，如fastText模型
│   └── lid.176.bin
├── src  #程序
│   ├── main.py   #程序入口
│   ├── services   # 调用deepseek服务
│   │   ├── __pycache__
│   │   ├── scoresFromDS.py
│   │   └── strToJson.py
│   └── utils    #数据筛选规则，如回答是否正确、是否混有多种语言、是否超出最大token长度等
│       ├── __pycache__
│       ├── filterLongAnswer.py
│       ├── mixedLanguageDetect.py
│       └── reward_score
└── tests
```

## 🧠 处理流程

<img src="https://shanyao13-bucket.oss-cn-beijing.aliyuncs.com/img/image-20250528170230176.png" alt="image-20250528170230176" style="zoom:50%;" />



输出文件格式：

```jsonl
{
    "question":"Which of the following statements is (are) correct? (x) The opportunity cost of the first 50 tables is 400 chairs and the opportunity cost of the first 800 chairs is 20 tables. (y) If the economy produces 80 tables and 800 chairs instead of 50 tables and 1,400 chairs, then the opportunity cost of the 30 additional tables is 600 chairs. (z) The opportunity cost of the 200th chair is equal to 1/40th of a table and the opportunity cost of the 30th table is more than 8 chairs but less than 10 chairs. a. (x), (y) and (z) b. (x) and (y), only c. (x) and (z), only d. (y) and (z), only e. (x) only Production Possibilities Tables Chairs 100 0 80 800 50 1,400 0 1,800",
    "answer":"<think> Okay, let's tackle this problem step by step. I need to figure out which of the statements (x), (y), and (z) are correct based on the given production possibilities data. The answer choices suggest that one or more of these. xxxx......xxxx.lysis of Statements:** - **Statement (x):** - Opportunity cost of 50 tables is 400 chairs (correct). - Opportunity cost of 800 chairs is 20 tables (correct). - **Correct** - **Statement (y):** - Moving from 50 tables and 1,400 chairs to 80 tables and 800 chairs. - Opportunity cost of 30 tables is 600 chairs (correct). - **Correct** - **Statement (z):** - Opportunity cost of the 200th chair is \( \frac{1}{40} \) of a table (correct). - Opportunity cost of the 30th table is 8 chairs (incorrect, as it is exactly 8 chairs). - **Incorrect** **Conclusion:** Statements (x) and (y) are correct. The correct answer is \(\boxed{b}\).",
    "best_sacore":10,
    "reason":"The student's answer is thorough, accurate, and demonstrates a clear understanding of the concepts. Each statement is analyzed carefully with correct calculations and logical reasoning. The student correctly identifies which statements are true and justifies their choice of the correct option (b). The explanation is complete and considers all relevant aspects of the question."
}
...
{
  ...
}
```



## ▶️ 运行项目

安装依赖：

```shell
pip install -r requirements.txt
```

执行脚本：

```shell
python ./src/main.py 
```

