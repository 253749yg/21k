import requests
import streamlit as st

# API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# =========在这里粘贴你自己的硅基流动密钥=========
API_KEY = "sk-zunwraoeelejmrvcrpejfuuxwrfguepfrvyjisoeurxmpuvq"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 任务要求：新生/在校生/教师三套独立system提示词
prompt_dict = {
    "新生": "你是小航，郑州航院校园信息助手，专门服务新生，耐心解答入学报到、宿舍、军训、校园导航等新生相关问题。",
    "在校生": "你是小航，郑州航院校园信息助手，服务在校学生，解答选课、自习室、社团、食堂、考试、奖学金等日常校园问题。",
    "教师": "你是小航，郑州航院校园信息助手，面向学校教师，侧重解答教务安排、教学相关事宜。"
}

# 页面UI（你已经调试成功的界面）
st.title("小航 · 郑州航院校园信息助手")
role = st.selectbox("你是？", ["新生", "在校生", "教师"])
question = st.text_input("有啥想问的？")

# 输入内容不为空，发起AI请求
if question:
    st.info(f"当前身份：{role}｜你的问题：{question}")
    system_prompt = prompt_dict[role]

    request_data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }

    # try-except 异常捕获（文档强制要求：超时、网络、未知错误）
    try:
        response = requests.post(API_URL, headers=HEADERS, json=request_data, timeout=15)
        response.raise_for_status()
        result = response.json()
        ai_answer = result["choices"][0]["message"]["content"]
        st.subheader("🤖小航回答：")
        st.write(ai_answer)

    except requests.exceptions.Timeout:
        st.error("AI响应超时，请稍后重试！")
    except requests.exceptions.ConnectionError:
        st.error("网络连接失败，请检查网络")
    except Exception as err:
        st.error(f"请求发生异常：{err}")