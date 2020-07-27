# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


from ui_form import Ui_Form
from FormPageBar.form_page_bar import FormPageBar


class Form(QWidget, Ui_Form):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)
		self.setupUi(self)
	
	# 设定公司名字，参数类型str
	def setCompanyName(self, name):
		self.groupBox.setTitle(name)
		
	# 设定表格上方的标题，参数类型str
	def setTitle(self, title):
		self.title.setText(title)
	
	# 表头水平垂直拉伸，参数类型bool，bool
	def setStretch(self, row, col):
		if row:
			self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
		if col:
			self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
			
	# 设定表头样式表
	def setHeaderStyleSheet(self):
		self.tableWidget.setStyleSheet("QHeaderView::section, QTableCornerButton::section {"
			"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(158, 225, 255, 255), stop:0.583333 rgba(0, 128, 255, 255), stop:1 rgba(0, 128, 255, 255));"
			"	color: white;"
			"	border: 1px solid #d8d8d8;"
			"}")
			
	# 设定列表头，居中对齐，文本，参数类型list
	def setColumnHeader(self, name):
		sum_col = (len(name))
		self.tableWidget.setColumnCount(sum_col)
		for each_col in range(sum_col):
			column = QTableWidgetItem()
			column.setTextAlignment(QtCore.Qt.AlignCenter)
			self.tableWidget.setHorizontalHeaderItem(each_col, column)
			self.tableWidget.horizontalHeaderItem(each_col).setText(name[each_col])
			
	# 设定行表头，居中对齐，文本，参数类型int
	def setRowHeader(self, row_sum):
		self.tableWidget.setRowCount(row_sum)
		for each_row in range(row_sum):
			row = QTableWidgetItem()
			row.setTextAlignment(QtCore.Qt.AlignCenter)
			self.tableWidget.setVerticalHeaderItem(each_row, row)
			self.tableWidget.verticalHeaderItem(each_row).setText('%s' %(each_row + 1))
	
	# 设定表格不可以编辑
	def setUneditable(self):
		self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
	
	# 设置表格所有单元格的样式
	def setItemStyle(self):
		self.tableWidget.setItemColorAlignment()
		
		
	def test(self):
		self.tableWidget.pageBlockDisplay(1)
		page_total = self.tableWidget.getPageTotal()
		self.form_page_bar = FormPageBar(self.tableWidget)
		self.form_page_bar.setPageNum(1, page_total)
		self.form_page_bar.initFormPageBar()
		
		self.verticalLayout_2.addWidget(self.form_page_bar)

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	ui = Form()
	name = ['测试1', '测试2', '测试3', '测试3', '测试3', '测试3', '测试3', '测试3']
	ui.setColumnHeader(name)
	ui.setRowHeader(45)
	ui.setItemStyle()
	ui.test()
	# ui.setStretch(True, False)
	# ui.setUneditable()
	ui.setHeaderStyleSheet()
	ui.show()
	sys.exit(app.exec_())
