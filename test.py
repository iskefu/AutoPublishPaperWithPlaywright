import sys
import markdown
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, 
                             QWidget, QFileDialog, QMessageBox)

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Markdown Editor')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)  # 文本编辑器，用于输入 Markdown
        self.htmlViewer = QTextEdit(self)  # 文本显示器，用于展示转换后的 HTML
        self.htmlViewer.setReadOnly(True)  # 设为只读，不允许编辑
        
        self.convertButton = QPushButton('Convert to HTML', self)  # 转换按钮
        self.convertButton.clicked.connect(self.convertMarkdownToHTML)
        
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.htmlViewer)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def convertMarkdownToHTML(self):
        mdText = self.textEdit.toPlainText()  # 从文本编辑器中获取 Markdown 文字
        html = markdown.markdown(mdText)  # 使用 markdown 库转换为 HTML
        self.htmlViewer.setHtml(html)  # 将转换后的 HTML 显示在 QTextEdit 中

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    editor = MarkdownEditor()
    editor.show()
    
    sys.exit(app.exec_())
