import requests
import streamlit as st
import os
import time

# 导入全局读取全部md知识库函数
from utils.knowledge_loader import load_all_md_knowledge

# API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# ========在这里粘贴你自己的硅基流动密钥========
API_KEY = "sk-mdfencyuidwlrljklhxifddqizbcltbftdeoixmsjnvvxyta"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# =========【新增1】初始化会话历史存储 =========
if "history" not in st.session_state:
    st.session_state["history"] = []

# 一次性加载所有md知识库（新生入学、办事流程、电话黄页、交通出行全部读取）
all_knowledge = load_all_md_knowledge()

# 任务要求：新生/在校生/教师三套独立system提示词
prompt_dict = {
    "新生": f"你是小航，郑州航院校园信息助手，专门服务新生，耐心解答入学报到、校园导航、宿舍、食堂相关问题，回答简洁易懂。\n【校园参考资料】\n{all_knowledge}",
    "在校生": f"你是小航，郑州航院校园信息助手，服务在校学生，解答选课、自习室、图书馆、考试、社团相关问题。\n【校园参考资料】\n{all_knowledge}",
    "教师": f"你是小航，郑州航院校园信息助手，面向学校教师，侧重解答教务安排、教室使用、科研相关问题。\n【校园参考资料】\n{all_knowledge}"
}

# 页面UI
st.title("小航 · 郑州航院校园信息助手")
role = st.selectbox("你是？", ["新生", "在校生", "教师"])
question = st.text_input("有啥想问的？")

# 输入内容不为空，发起AI请求
if question:
    st.info(f"当前身份：{role} | 你的问题：{question}")
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

        # 密钥失效判断
        if response.status_code == 401:
            st.error("API Key 失效，请检查密钥！")
        elif response.status_code >= 400:
            st.warning(f"API请求异常，状态码：{response.status_code}")
        else:
            response.raise_for_status()
            result = response.json()
            ai_answer = result["choices"][0]["message"]["content"]
            st.subheader("🤖小航回答：")
            st.write(ai_answer)

            # =========【新增2】保存本次问答记录 =========
            st.session_state["history"].append({
                "time": time.strftime("%H:%M:%S"),
                "role": role,
                "question": question,
                "answer": ai_answer,
            })

    except requests.exceptions.Timeout:
        st.error("AI响应超时，请稍后重试！")
    except requests.exceptions.ConnectionError:
        st.error("网络连接失败，请检查网络")
    except Exception as err:
        st.error(f"请求发生异常：{err}")
else:
    # 新增：用户空输入提示
    if st.button("提交提问"):
        st.warning("请输入你的问题，不允许空白提问！")

# 数据文件缺失检测
target_file = "./data/readme.txt"
try:
    if os.path.exists(target_file):
        with open(target_file,"r",encoding="utf-8") as f:
            pass
    else:
        st.warning(f"检测到文件缺失：{target_file}")
except Exception as e:
    st.error(f"读取文件发生错误：{e}")

# ==========新增页面底部静态黄页表格==========
st.divider()
st.header("📞 郑航校内电话黄页")
st.caption("常用校内部门联系电话")
yellow_table = """
| 部门 | 联系电话 |
| ---- | ---- |
| 校园保卫处24小时 | 0371-61916110 |
| 学校总值班室 | 0371-61911000 |
| 校医院急诊 | 0371-61912730 |
| 后勤报修热线 | 0371-61913110 |
| 信息管理中心（校园网/一卡通） | 0371-61912718 |
| 招生办公室 | 0371-61916161 |
| 研究生招生办 | 0371-61912520 |
"""
st.markdown(yellow_table)
st.warning("⚠️涉及转账、缴费的来电，请先和辅导员确认，防范电信诈骗！")

# =========【新增3】问答历史展示区域 =========
st.divider()
st.header("📝问答历史")
# reversed() 实现最新对话在最上方
for item in reversed(st.session_state["history"]):
    st.write(f"[{item['time']}] {item['role']} 提问：{item['question']}")
    st.write(f"回答：{item['answer']}")
    st.caption("————————————")