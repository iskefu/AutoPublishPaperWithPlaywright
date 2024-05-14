import asyncio
import tkinter as tk
from functools import partial
from publish_fun import baijiahao, bilibili, csdn, jianshu, juejin, tencentcloud, toutiao, wxgzh, zhihu

# 创建主窗口
root = tk.Tk()
root.geometry("400x300")

# 创建按钮并绑定对应的函数
button1 = tk.Button(root, text="WZGZH", command=lambda: asyncio.create_task(wxgzh()))
button1.pack()

button2 = tk.Button(root, text="BaiJiaHao", command=lambda: asyncio.create_task(baijiahao()))
button2.pack()

button3 = tk.Button(root, text="blbl", command=lambda: asyncio.create_task(bilibili()))
button3.pack()

button4 = tk.Button(root, text="csdn", command=lambda: asyncio.create_task(csdn()))
button4.pack()

button5 = tk.Button(root, text="jianshu", command=lambda: asyncio.create_task(jianshu()))
button5.pack()

button6 = tk.Button(root, text="juejin", command=lambda: asyncio.create_task(juejin()))
button6.pack()

button7 = tk.Button(root, text="tencentcloud", command=lambda: asyncio.create_task(tencentcloud()))
button7.pack()

button8 = tk.Button(root, text="toutiao", command=lambda: asyncio.create_task(toutiao()))
button8.pack()

button9 = tk.Button(root, text="zhihu", command=lambda: asyncio.create_task(zhihu()))
button9.pack()

# 运行应用程序
root.mainloop()
