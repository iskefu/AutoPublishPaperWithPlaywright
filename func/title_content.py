import os
import re
def title(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename 
def content(filepath):
    with open(filepath, 'r',encoding='utf-8') as f:
        content = f.read()
        content=re.sub(r'---(.|\s)*?---', '', content)
    return content
 