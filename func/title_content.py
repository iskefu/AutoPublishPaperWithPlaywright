import os
import re

import mistune
def title(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename 
def content(filepath):
   
    with open(filepath, 'r',encoding='utf-8') as f:
        content = f.read()
    content=re.sub(r'---(.|\s)*?---', '', content)
    return content

def md_content(filepath):
    markdown = mistune.create_markdown()
    with open(filepath, 'r',encoding='utf-8') as f:
        content = f.read()
    html = markdown(content) 
    print(html)

    return content





if __name__ == '__main__':
    
    filepath = '/run/media/kf/data/obsidian/Capture/ollma3部署记录.md'

    # content(filepath)
    md_content(filepath)