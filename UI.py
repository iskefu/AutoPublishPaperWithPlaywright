import sys
import asyncio
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QFileDialog, QLineEdit, QHBoxLayout, QMessageBox)
from publish.baijiahao import baijiahao
from blbl import bilibili
from publish.csdn import csdn
from publish.jianshu import jianshu
from publish.juejin import juejin
from publish.texcentcloud import tencentcloud
from publish.toutiao import toutiao
from publish.wxgzh import wxgzh
from publish.zhihu import zhihu

class PlatformSelectionWindow(QMainWindow):
    def __init__(self, cover_path, upload_path):
        super().__init__()
        self.cover_path = cover_path
        self.upload_path = upload_path
        self.setWindowTitle('Select Platform')
        self.setGeometry(400, 400, 300, 150)
        layout = QVBoxLayout()

        self.platforms = ["百家号", "哔哩哔哩", "csdn", "简书","掘金","微信公众号", "腾讯云", "头条", "知乎", "Others。。。"]
        for platform in self.platforms:
            btn = QPushButton(platform, self)
            btn.clicked.connect(lambda checked, p=platform: self.publish(p))
            layout.addWidget(btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def publish(self, platform):
        try:
            print(f"upload_path: {self.upload_path}, cover_path: {self.cover_path}")  # 添加打印语句
            if platform == "微信公众号":
            # 传递封面路径和上传文件路径至函数
                asyncio.run(wxgzh(self.upload_path, self.cover_path))
            elif platform=="百家号":
                asyncio.run(baijiahao(self.upload_path, self.cover_path))
            elif platform== "哔哩哔哩":
                asyncio.run(bilibili(self.upload_path, self.cover_path))
            elif platform=="csdn":
                asyncio.run(csdn(self.upload_path, self.cover_path))
            elif platform=="简书":
                asyncio.run(jianshu(self.upload_path, self.cover_path))
            elif platform=="掘金":
                asyncio.run(juejin(self.upload_path, self.cover_path))
            elif platform=="腾讯云":
                asyncio.run(tencentcloud(self.upload_path, self.cover_path))
            elif platform=="头条":
                asyncio.run(toutiao(self.upload_path, self.cover_path))
            elif platform=="知乎":
                asyncio.run(zhihu(self.upload_path, self.cover_path))
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'Failed to publish to {platform}. {e}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Uploader')
        self.setGeometry(100, 100, 800, 300)

        # 创建所有的控件
        self.coverLineEdit = QLineEdit(self)  
        self.selectCoverButton = QPushButton('Select Cover Image', self)
        self.selectCoverButton.clicked.connect(self.selectCover)  
        self.uploadFileLineEdit = QLineEdit(self)
        self.selectUploadFileButton = QPushButton('Select Upload File', self)
        self.selectUploadFileButton.clicked.connect(self.selectUploadFile)  
        self.confirmButton = QPushButton("Confirm", self)
        self.confirmButton.clicked.connect(self.confirmSelection)
        self.cancelButton = QPushButton("Cancel", self)

        # 创建水平布局用于控件
        coverLayout = QHBoxLayout()
        coverLayout.addWidget(self.coverLineEdit)
        coverLayout.addWidget(self.selectCoverButton)
        
        uploadFileLayout = QHBoxLayout()
        uploadFileLayout.addWidget(self.uploadFileLineEdit)
        uploadFileLayout.addWidget(self.selectUploadFileButton)
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.confirmButton)
        buttonsLayout.addWidget(self.cancelButton)

        # 创建一个垂直布局来包含所有的水平布局
        layout = QVBoxLayout()
        layout.addLayout(coverLayout)
        layout.addLayout(uploadFileLayout)
        layout.addLayout(buttonsLayout)
        
        # 创建一个中心控件，并设置布局和控件到窗口
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def selectCover(self):
        # 选择封面图片目录
        directory = QFileDialog.getExistingDirectory(self, "Select Cover Directory")
        if directory:
            self.coverLineEdit.setText(directory)

    def selectUploadFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Upload File", "", "All Files (*)")
        if path:
            self.uploadFileLineEdit.setText(path)

    def confirmSelection(self):
        coverPath = self.coverLineEdit.text()
        uploadFilePath = self.uploadFileLineEdit.text()
        if coverPath and uploadFilePath:
            self.platformWindow = PlatformSelectionWindow(coverPath, uploadFilePath)
            self.platformWindow.show()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select both a cover image and an upload file.')

# 应用程序主入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())   