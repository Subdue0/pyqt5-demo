# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from Page.page import Page


class Salary(Page):
	def __init__(self, parent=None):
		super(Page, self).__init__(parent)
		self.setupUi(self)
		
		self.setTitle('工资表')
		
		self.getDataFromDB()
		self.setRowHeader(self.row_sum)
		
		self.field = ['编号', '姓名', '部门', '职务', '基本工资', '提成', '奖金', '考勤扣除', '实发工资']
		self.setColumnHeader(self.field)
		
		self.col_sum = self.tableWidget.columnCount()
		
		self.setItemColorAlignment()
		
		self.setFormEditable()
		
		self.initFormDate()
		
		self.initSearchField()
			
		self.setFormStyleSheet()
		
	
		self.createContextMenu()


		self.history_record = {'add': [], 'del': [], 'update': {}}
		self.submit.setEnabled(False)
		# 初始化单元格改变信号标志
		self.cell_changed_flag = False
		# 初始化当前页面为1
		self.form_cur_page_num = 1
		# 统计下设置的行数可以分成多少页
		row_sum = self.tableWidget.rowCount()
		if row_sum%10:
			self.form_page_total = int(row_sum/10) + 1
		else:
			self.form_page_total = int(row_sum/10)
		# 初始化分页栏
		self.initFormPageBar()
		# 表格分页显示
		self.pageBlockDisplay()
		
		# 初始化信号连接
		self.signalConnection()
		
		# 断开上下文菜单信号
		self.tableWidget.customContextMenuRequested.disconnect(self.showContextMenu)
	

			
	'''获取数据'''
	def getDataFromDB(self):
		try:
			self.connectDB()
			self.cursor.execute('''
								select Employee.Eno as 员工编号,Ename as 姓名,Dname as 部门,Pname as 职位,BaseSalary as 基本工资,Com*BaseSalary as 提成,Allowance as 部门奖金,Unwork *100 as 考勤扣除,BaseSalary+Allowance+Com*BaseSalary-Unwork*100 as 实发工资
								from Employee,Post,Department,Salary,Attendance
								where Employee.Dno=Department.Dno
								and Employee.Pno=Post.Pno
								and Salary.Pno=Post.Pno
								and Salary.Dno=Department.Dno
								and Attendance.Eno=Employee.Eno
							''')
			
			self.row = self.cursor.fetchall()
			
			self.row_sum = len(self.row)
		
		except Exception as e:
			print('getDataFromDB():\n'+repr(e))
			sys.exit(-1)


	def setFormEditable(self):
		row_sum = self.tableWidget.rowCount()
		if self.editable.isChecked():
			for i in range(row_sum):
				for j in range(self.col_sum):
					if j != 5:
						self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
					else:
						self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
		else:
			for i in range(row_sum):
				for j in range(self.col_sum):
					self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
			

	'''初始化表格数据'''
	def initFormDate(self):
		for each_row in range(self.row_sum):
			for each_col in range(self.col_sum):
				if self.row[each_row][each_col]:
					item_text = str(self.row[each_row][each_col])
					self.tableWidget.item(each_row, each_col).setText(item_text)
	
		
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	salary = Salary()
	salary.show()
	sys.exit(app.exec_())