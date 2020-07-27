# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from Ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		# 通过QSS样式的方式设置按钮文字
		self.setStyleSheet(TextStyle)
		self.setupUi(self)
		self.width = self.rolling_subtitles.width()
		self.scrollTimer = QTimer()
		self.scrollTimer.start(30)
		self.scrollTimer.timeout.connect(self.setScrollText)
	
	@pyqtSlot()
	def on_pushButton_25_clicked(self):
		"""
		Slot documentation goes here.
		"""
		# TODO: not implemented yet
		self.tableWidget_3.setCellWidget(1, 1, QCheckBox('111'))
	
	
	def setScrollText(self):
		if self.width != self.rolling_subtitles.width():
			self.width = self.rolling_subtitles.width()
			self.length = self.rolling_subtitles.fontMetrics().boundingRect(self.rolling_subtitles.text()).width()
			
			self._x = -(self.width/2 + self.length)
			self.x = -self._x
		
		self.rolling_subtitles.move(self._x, 0)
		self._x += 1
		if self._x == self.x:
			self._x = -(self.rolling_subtitles.width()/2 + self.length)
		
	
	@pyqtSlot(QTreeWidgetItem, int)
	def on_treeWidget_itemClicked(self, item, column):
		opt_obj = item.text(0)
		if opt_obj == '工资':
			print(self.rolling_subtitles.width())
			self.stackedWidget.setCurrentIndex(1)
		elif opt_obj == '员工':
			self.stackedWidget.setCurrentIndex(2)
		elif opt_obj == '考勤':
			self.stackedWidget.setCurrentIndex(3)
			
		elif opt_obj == 'Excel表':
			self.stackedWidget.setCurrentIndex(4)
			
		elif opt_obj == '新消息':
			self.stackedWidget.setCurrentIndex(5)
		elif opt_obj == '消息记录':
			self.stackedWidget.setCurrentIndex(6)
			
		elif opt_obj == '工资调整记录':
			self.stackedWidget.setCurrentIndex(7)
			
		elif opt_obj == '修改密码':
			self.stackedWidget.setCurrentIndex(8)
		elif opt_obj == '员工授权':
			self.stackedWidget.setCurrentIndex(9)
		elif opt_obj == '操作记录':
			self.stackedWidget.setCurrentIndex(10)
		elif opt_obj == '注销账号':
			reply = QMessageBox.question(self, '提示', '确认切换账户?', QMessageBox.Yes | QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.hide()
				self.parent().show()
		elif opt_obj == '退出系统':
			self.close()



	@pyqtSlot(QTableWidgetItem)	
	def on_tableWidget_3_itemClicked(self, item):
		"""
		Slot documentation goes here.
		
		@param item DESCRIPTION
		@type QTableWidgetItem
		"""
		# TODO: not implemented yet
		print(11)

	# def treeview_item_control(self, is_expanded):
		# if self.is_expanded == False:
			# self.treeWidget.expandAll()
			# self.is_expanded = True
		# else:
			# self.treeWidget.collapseAll()
			# self.is_expanded = False
	
	'''重载Qt事件'''
	def resizeEvent(self, event):
		if self.stackedWidget.currentIndex():
			self.salary.resize(self.page_1.size())
			self.emp.resize(self.page_2.size())
	def minimumSizeHintEvent(self, event):
		print(111)
	def closeEvent(self, event):
		reply = QMessageBox.question(self, '提示', '确认退出程序?', QMessageBox.Yes | QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			sys.exit()
		else:
			event.ignore()


TextStyle = """
	QMessageBox QPushButton[text="OK"] {
		qproperty-text: "好的";
	}
	QMessageBox QPushButton[text="Open"] {
		qproperty-text: "打开";
	}
	QMessageBox QPushButton[text="Save"] {
		qproperty-text: "保存";
	}
	QMessageBox QPushButton[text="Cancel"] {
		qproperty-text: "取消";
	}
	QMessageBox QPushButton[text="Close"] {
		qproperty-text: "关闭";
	}
	QMessageBox QPushButton[text="Discard"] {
		qproperty-text: "不保存";
	}
	QMessageBox QPushButton[text="Don't Save"] {
		qproperty-text: "不保存";
	}
	QMessageBox QPushButton[text="Apply"] {
		qproperty-text: "应用";
	}
	QMessageBox QPushButton[text="Reset"] {
		qproperty-text: "重置";
	}
	QMessageBox QPushButton[text="Restore Defaults"] {
		qproperty-text: "恢复默认";
	}
	QMessageBox QPushButton[text="Help"] {
		qproperty-text: "帮助";
	}
	QMessageBox QPushButton[text="Save All"] {
		qproperty-text: "保存全部";
	}
	QMessageBox QPushButton[text="&Yes"] {
		qproperty-text: "是";
	}
	QMessageBox QPushButton[text="Yes to &All"] {
		qproperty-text: "全部都是";
	}
	QMessageBox QPushButton[text="&No"] {
		qproperty-text: "不";
	}
	QMessageBox QPushButton[text="N&o to All"] {
		qproperty-text: "全部都不";
	}
	QMessageBox QPushButton[text="Abort"] {
		qproperty-text: "终止";
	}
	QMessageBox QPushButton[text="Retry"] {
		qproperty-text: "重试";
	}
	QMessageBox QPushButton[text="Ignore"] {
		qproperty-text: "忽略";
	}
	"""


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = MainWindow()
	ui.show()
	sys.exit(app.exec_())
