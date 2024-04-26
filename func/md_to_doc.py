
import subprocess
import pypandoc
import os

def md_to_docx(filepath):
    output_path = os.path.splitext(filepath)[0] + '.docx'
    try:   
        subprocess.run(['pandoc', '-s', filepath, '-o', output_path], check=True)
        print("文件转换成功！")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"文件转换失败。命令`{e.cmd}`返回错误代码 {e.returncode}")
        return 
filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'

if __name__ == '__main__':
    md_to_docx(filepath)