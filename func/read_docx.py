from docx import Document
def read_docx(file_path):
    # 使用python-docx读取 .docx 文件
    try:
        doc = Document(file_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception as e:
        print(e)
        return None
    


if __name__ == '__main__':
    file_path = f'Dataview JavaScript速查表.docx'
    text = read_docx(file_path)
    if text:
        print('成功读取文件：', file_path)
        print(text)
    else:
        print('读取文件失败：', file_path)