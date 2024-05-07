# 替换'mdfile'为你的Markdown文件的实际路径
import os
import subprocess

def md_to_doc(input_file):
    input_file = os.path.abspath(input_file)
    print(f"输入文件: {input_file}")

    file_name = os.path.splitext(input_file)[0]
    # print(f"文件名: {file_name}")
    
    output_file = f"{file_name}.docx"
    print(f"输出文件名: {output_file}")
    
    # 设置你的 Docx 模板路径
    template_docx = 'pandoc_word_template-main/templates_标题不编号.docx'  # 替换成你的 Docx 模板文件路径
    # print(f"模板文件: {template_docx}")

    command = [
        'pandoc', input_file,
        '--reference-doc', template_docx,
        '-o', output_file
    ]

    # 使用 subprocess.run 来执行命令
    try:
        if not os.path.exists(output_file):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"文件成功生成在: {output_file}")

    except subprocess.CalledProcessError as error:
        print("命令执行失败")
        print(f"标准输出: {error.stdout}")
        print(f"标准错误: {error.stderr}")

    # 返回输出的文件地址
    return output_file

if __name__ == '__main__':
    input_file = 'Dataview JavaScript速查表.md' # 替换成你的 Markdown 文件路径
    md_to_doc(input_file)