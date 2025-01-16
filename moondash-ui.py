from flask import Flask, request, jsonify, render_template_string
from zhipuai import ZhipuAI
import json

# 初始化Flask应用
app = Flask(__name__)

# 质谱AI客户端
client = ZhipuAI(api_key="63c3c130511b4cb2ad37651de8993789.CdsztJBo5kmCqU85")

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoonDash</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            color: #4CAF50;
        }
        input[type="text"] {
            width: calc(100% - 20px);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            border-radius: 4px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            text-align: left;
            background: #f1f1f1;
            padding: 15px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>MoonDash</h1>
        <p>请输入月饼设计的描述：</p>
        <form method="POST">
            <input type="text" name="description" placeholder="描述您的月饼设计..." required>
            <br>
            <button type="submit">分析</button>
        </form>
        {% if result %}
        <div class="result">
            <h3>规格：</h3>
            <pre>{{ result }}</pre>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# 主页面路由
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        description = request.form['description']

        # 构造质谱AI的消息内容
        messages = [
            {
                "role": "user",
                "content": '''你是一个专家级的AI，能够分析月饼设计的描述并提取详细的规格信息。
                                根据输入的月饼描述，识别并提取以下属性（若无法确定，选择最合适的，禁止输出Null）：
                                1. **花纹样式**：根据描述选择以下之一：
                                    - 吉祥如意纹
                                    - 寿桃纹
                                    - 福禄寿纹
                                    - 龙凤呈祥纹
                                    - 花卉纹
                                    - 古钱币纹
                                    - 八卦纹
                                    - 云雷纹
                                    - 仿木雕纹
                                2. **月饼侧边瓣数**：提取描述中提到的瓣数（例如：12，16，20）。
                                3. **月饼颜色**：根据描述识别颜色（例如：金黄、淡黄、深棕等）。
                                4. **月饼厚度**：确定厚度为以下之一：
                                    - 薄
                                    - 中
                                    - 厚
                                用且仅用以下JSON格式返回结果：
                                {"pattern_style": "<提取的花纹样式>","petal_count": "<提取的瓣数>","color": "<提取的颜色>","thickness": "<提取的厚度>"}
                                你的回答中应该包含上述所有字段，同时不应出现其他的文字。。

                                月饼描述为：
                                '''+description
            }
        ]

        # 调用质谱AI模型
        try:
            response = client.chat.completions.create(
                model="glm-4v-plus", 
                messages=messages
            )
            # 提取结果并格式化为JSON
            response_message = response.choices[0].message.content
            response_message = response_message.replace('```json\n', '').replace('```', '')

            print(response_message)
            result = json.dumps(json.loads(response_message), indent=2, ensure_ascii=False)
        except Exception as e:
            result = f"发生错误：{str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)
