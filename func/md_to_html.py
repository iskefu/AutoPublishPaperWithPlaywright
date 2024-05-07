import markdown

def md_to_html(md_file):
    # 读取 Markdown 文件内容
    with open(md_file, 'r') as f:
        md_text = f.read()
    # 将 Markdown 文本转换为 HTML
    html = markdown.markdown(md_text)
    return html

# 使用例子
if __name__ == "__main__":
    md_file = "Dataview JavaScript速查表.md"
    html_content = md_to_html(md_file)
    print(html_content)
