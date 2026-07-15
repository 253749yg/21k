import requests
from src.config import API_URL, API_KEY, MODEL_NAME, TIMEOUT

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_ai_answer(system_msg, user_msg):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    }
    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=TIMEOUT)
        # 密钥失效
        if resp.status_code == 401:
            return "[ERROR]API Key失效，请联系老师重新获取"
        if resp.status_code != 200:
            return f"[ERROR]接口异常，状态码：{resp.status_code}"
        res_json = resp.json()
        answer = res_json["choices"][0]["message"]["content"]
        return answer
    except requests.exceptions.Timeout:
        return "[ERROR]AI响应超时，请稍后再试"
    except requests.exceptions.ConnectionError:
        return "[ERROR]网络连接失败，请检查网络"
    except (KeyError, IndexError):
        return "[ERROR]AI返回格式异常，请重试"
    except Exception as e:
        return f"[ERROR]未知错误：{str(e)}"