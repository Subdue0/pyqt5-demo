# -*- coding: utf-8 -*-


import sys

from PyQt5.QtWidgets import QApplication,QWidget

from .ui_form_page_bar import Ui_FormPageBar


class FormPageBar(QWidget, Ui_FormPageBar):
	form_cur_page_num = 1
	form_page_total = 1
	

	def __init__(self, parent=None):
		super(FormPageBar, self).__init__(parent)
		self.setupUi(self)
		self.tableWidget = parent
	
	@classmethod	
	def getPageNum(cls):
		return cls.form_cur_page_num, cls.form_page_total
		
		
	@classmethod
	def setPageNum(cls, form_cur_page_num, form_page_total):
		cls.form_cur_page_num = form_cur_page_num
		cls.form_page_total = form_page_total
		
		
	# 初始化信息表的分页栏
	def initFormPageBar(self):
		# 信息表分页栏信号连接
		self.form_first_page.clicked.connect(self.ctrlFormPageBar)
		self.form_previous_page.clicked.connect(self.ctrlFormPageBar)
		self.form_next_page.clicked.connect(self.ctrlFormPageBar)
		self.form_last_page.clicked.connect(self.ctrlFormPageBar)
		# 页码显示初始化
		self.form_page_num.setText('[%d/%d]页' %(self.form_cur_page_num, self.form_page_total))
		if self.form_cur_page_num == 1:
			if self.form_cur_page_num == 1 and self.form_page_total == 1:
				self.form_first_page.setEnabled(False)
				self.form_previous_page.setEnabled(False)
				self.form_next_page.setEnabled(False)
				self.form_last_page.setEnabled(False)
			else:
				self.form_first_page.setEnabled(False)
				self.form_previous_page.setEnabled(False)
				self.form_next_page.setEnabled(True)
				self.form_last_page.setEnabled(True)	
		elif self.form_cur_page_num == self.form_page_total:
			self.form_first_page.setEnabled(True)
			self.form_previous_page.setEnabled(True)
			self.form_next_page.setEnabled(False)
			self.form_last_page.setEnabled(False)
			

	
	# 槽函数（信息表分页栏）
	def ctrlFormPageBar(self):
		# 通过监测发送信号的对象名做相应处理
		obj_name = self.sender().objectName()
		if obj_name == 'form_first_page':
			self.form_cur_page_num = 1
			
			self.form_first_page.setEnabled(False)
			self.form_previous_page.setEnabled(False)
			self.form_next_page.setEnabled(True)
			self.form_last_page.setEnabled(True)
			
			self.form_page_num.setText('[1/%d]页' %self.form_page_total)
			
			self.tableWidget.pageBlockDisplay(self.form_cur_page_num)
			
		elif obj_name == 'form_previous_page':
			if self.form_cur_page_num > 1:
				self.form_cur_page_num -= 1
				
				if self.form_cur_page_num == 1:
					self.form_first_page.setEnabled(False)
					self.form_previous_page.setEnabled(False)
					
				self.form_page_num.setText('[%d/%d]页' %(self.form_cur_page_num, self.form_page_total))
			else:
				self.form_first_page.setEnabled(False)
				self.form_previous_page.setEnabled(False)
			
			if self.form_cur_page_num == self.form_page_total:
				self.form_next_page.setEnabled(False)
				self.form_last_page.setEnabled(False)
			else:
				self.form_next_page.setEnabled(True)
				self.form_last_page.setEnabled(True)
				
			self.tableWidget.pageBlockDisplay(self.form_cur_page_num)
				
		elif obj_name == 'form_next_page':
			if self.form_cur_page_num < self.form_page_total:
				self.form_cur_page_num += 1
				
				if self.form_cur_page_num == self.form_page_total:
					self.form_next_page.setEnabled(False)
					self.form_last_page.setEnabled(False)
					
				self.form_page_num.setText('[%d/%d]页' %(self.form_cur_page_num, self.form_page_total))
			else:
				self.form_next_page.setEnabled(False)
				self.form_last_page.setEnabled(False)
			
			if self.form_cur_page_num == 1:
				self.form_first_page.setEnabled(False)
				self.form_previous_page.setEnabled(False)
			else:
				self.form_first_page.setEnabled(True)
				self.form_previous_page.setEnabled(True)
			
			self.tableWidget.pageBlockDisplay(self.form_cur_page_num)

		elif obj_name == 'form_last_page':
			self.form_cur_page_num = self.form_page_total
			
			self.form_first_page.setEnabled(True)
			self.form_previous_page.setEnabled(True)
			self.form_next_page.setEnabled(False)
			self.form_last_page.setEnabled(False)
			
			self.form_page_num.setText('[%d/%d]页' %(self.form_page_total, self.form_page_total))
			
			self.tableWidget.pageBlockDisplay(self.form_cur_page_num)
			
			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui = FormPageBar(1, 3)
	ui.show()
	sys.exit(app.exec_())