import time
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QTimer


class Example(QWidget):
	
	def __init__(self):
		super().__init__()
		self.initUI()
		self.scrollTimer = QTimer()
		self.scrollTimer.start(30)
		self.scrollTimer.timeout.connect(self.setScrollText)
		
		
		
	def initUI(self):	  
		self.setGeometry(300, 300, 280, 270)
		self.setWindowTitle('Pen styles')
		self.ql = QLabel(self)
		self.ql.setText('你有一条新消息！')
		self.length = self.ql.fontMetrics().boundingRect(self.ql.text()).width()
		print(self.length)
		self.index = self.width()
		
		self.show()
		
	def setScrollText(self):
		self.ql.move(self.index, 0)
		self.index -= 1
		if self.index == -self.length:
			self.index = self.width()
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())