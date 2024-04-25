import psutil

def check_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        if proc.info['name'] == 'chrome':
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return True
    return False

# 检查端口9222是否被chrome打开
# print(check_port(9222))