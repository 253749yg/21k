import os

def load_all_md_knowledge():
    # 存放md文档的文件夹！重点确认这里！
    # 你的md文件（01_新生入学.md等）位置：C:\Users\25374\xiaohang_helper
    folder_path = r"C:\Users\25374\xiaohang_helper"

    all_text = ""
    # 判断文件夹是否存在，防止直接崩溃
    if not os.path.isdir(folder_path):
        print(f"【警告】找不到文件夹：{folder_path}")
        return all_text

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            all_text += f"\n【文档：{filename}】\n{content}\n"
    return all_text