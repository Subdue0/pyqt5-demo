# -*- coding: utf-8 -*-

import sys
import pyodbc

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from Page.page import Page


class Employee(Page):
	def __init__(self, parent=None):
		super(Page, self).__init__(parent)
		self.setupUi(self)
		
		self.getDataFromDB()
		self.setRowHeader(self.row_sum)
		
		self.field = ['编号', '姓名', '性别', '年龄', '电话', '学历', '部门', '职务', '身份证', '入职时间', '毕业学校', '家庭住址', '个人简介']
		self.setColumnHeader(self.field)
		
		self.col_sum = self.tableWidget.columnCount()
		
		self.setItemColorAlignment()
		
		self.initFormDate()
		
		self.initSearchField()
		
		self.setNumNameUneditable()
		
		
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
		
		

	'''获取数据'''
	def getDataFromDB(self):
		try:
			self.connectDB()
			self.cursor.execute('''
								select Eno,Ename,Esex,Eage,Etel,Eedu,Dname,Pname,Eid,Intime,Gradu,Eaddr,Resume
								from Employee,Department,Post
								where Employee.Dno=Department.Dno
								and Employee.Pno=Post.Pno
							''')
			
			self.row = self.cursor.fetchall()
			
			self.row_sum = len(self.row)
		
		except pyodbc.Error as e:
			print('getDataFromDB():\n'+repr(e))


	'''初始化表格数据'''
	def initFormDate(self):
		for each_row in range(self.row_sum):
			for each_col in range(self.col_sum):
				if self.row[each_row][each_col]:
					item_text = str(self.row[each_row][each_col])
					self.tableWidget.item(each_row, each_col).setText(item_text)

	def refreshForm(self):
		self.getDataFromDB()
		self.initFormDate()
	
	def submitFormData(self):
		self.extractDelEmpNum()
		self.submit.setEnabled(False)
		print(self.history_record)
		if self.history_record['add']:
			print('+++++++++++')
			print('添加内容')
			print('+++++++++++')
			for each_row in self.history_record['add']:
				try:
					self.cursor.execute('select Dno from Department where Dname=?', each_row[6])
					each_row[6] = self.cursor.fetchone()[0]
				except pyodbc.Error as e:
					msg_box = QMessageBox()
					msg_box.setWindowTitle('错误')
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
					msg_box.setWindowIcon(icon)
					msg_box.setIcon(QMessageBox.Critical)
					msg_box.setText(e)
					msg_box.addButton('我知道了', QMessageBox.AcceptRole)
					msg_box.exec()
					return
				
				try:
					self.cursor.execute('select Pno from Post where Pname=?', each_row[7])
					each_row[7] = self.cursor.fetchone()[0]
				except pyodbc.Error as e:
					msg_box = QMessageBox()
					msg_box.setWindowTitle('错误')
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
					msg_box.setWindowIcon(icon)
					msg_box.setIcon(QMessageBox.Critical)
					msg_box.setText(e)
					msg_box.addButton('我知道了', QMessageBox.AcceptRole)
					msg_box.exec()
					return

				print(each_row[0], each_row[1], each_row[2], each_row[3], each_row[4], each_row[5], each_row[6], each_row[7], each_row[8], each_row[9], each_row[10], each_row[11], each_row[12])
				try:
					self.cursor.execute('insert into Employee values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', each_row[0], each_row[1], each_row[2], each_row[3], each_row[4], each_row[5], each_row[6], each_row[7], each_row[8], each_row[9], each_row[10], each_row[11], each_row[12])
					self.conn.commit()
				except pyodbc.Error as e:
					msg_box = QMessageBox()
					msg_box.setWindowTitle('错误')
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
					msg_box.setWindowIcon(icon)
					msg_box.setIcon(QMessageBox.Critical)
					msg_box.setText(e)
					msg_box.addButton('我知道了', QMessageBox.AcceptRole)
					msg_box.exec()
					return
			
			print('\n\n\n\n\n')
		if self.history_record['del']:
			print('+++++++++++')
			print('删除内容')
			print('+++++++++++')
			for each_row in self.history_record['del']:
				for each_key in list(each_row.keys()):
					try:
						self.cursor.execute('delete from Employee where Eno = ?', each_row[each_key][0])
						self.conn.commit()
					except pyodbc.Error as e:
						msg_box = QMessageBox()
						msg_box.setWindowTitle('错误')
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
						msg_box.setWindowIcon(icon)
						msg_box.setIcon(QMessageBox.Critical)
						msg_box.setText(e)
						msg_box.addButton('我知道了', QMessageBox.AcceptRole)
						msg_box.exec()
						return
					print('编号------->'+str(each_row[each_key][0]))
			print('\n\n\n\n\n')
		if self.history_record['update']:
			print('+++++++++++')
			print('更新内容')
			print('+++++++++++')
			for key in self.history_record['update'].keys():
				for each_col in self.history_record['update'][key]:
					col_name = list(each_col.keys())[0]
					col_value = list(each_col.values())[0]
					if col_name == '编号':
						col_name = 'Eno'
					elif col_name == '姓名':
						col_name = 'Ename'
					elif col_name == '性别':
						col_name = 'Esex'
						if col_value != '男' and col_value != '女':
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText('编号为' + key + '，性别不合法')
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							del self.history_record['update'][key]
							return						
					elif col_name == '年龄':
						col_name = 'Eage'
						try:
							col_value = int(col_value)
							if col_value < 16 or col_value > 100:
								msg_box = QMessageBox()
								msg_box.setWindowTitle('错误')
								icon = QtGui.QIcon()
								icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
								msg_box.setWindowIcon(icon)
								msg_box.setIcon(QMessageBox.Critical)
								msg_box.setText('编号为' + key + '，年龄应在16-100之间')
								msg_box.addButton('我知道了', QMessageBox.AcceptRole)
								msg_box.exec()
								del self.history_record['update'][key]
								return
						except:
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText('编号为' + key + '，年龄不合法')
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							del self.history_record['update'][key]
							return
					elif col_name == '电话':
						col_name = 'Etel'
					elif col_name == '学历':
						col_name = 'Eedu'
					elif col_name == '部门':
						col_name = 'Dno'
						try:
							self.cursor.execute('select Dno from Department where Dname = ?', col_value)
							col_value = self.cursor.fetchone()[0]
						except pyodbc.Error as e:
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText(e)
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							return
						except:
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText('编号为' + key + '，部门不合法')
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							del self.history_record['update'][key]
							return
					elif col_name == '职务':
						try:
							col_name = 'Pno'
							self.cursor.execute('select Pno from Post where Pname = ?', col_value)
							col_value = self.cursor.fetchone()[0]
						except pyodbc.Error as e:
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText(e)
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							return
						except:
							msg_box = QMessageBox()
							msg_box.setWindowTitle('错误')
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							msg_box.setWindowIcon(icon)
							msg_box.setIcon(QMessageBox.Critical)
							msg_box.setText('编号为' + key + '，职务不合法')
							msg_box.addButton('我知道了', QMessageBox.AcceptRole)
							msg_box.exec()
							del self.history_record['update'][key]
							return
					elif col_name == '身份证':
						col_name = 'Eid'
					elif col_name == '入职时间':
						col_name = 'Intime'
					elif col_name == '毕业学校':
						col_name = 'Gradu'
					elif col_name == '家庭住址':
						col_name = 'Eaddr'
					elif col_name == '个人简介':
						col_name = 'Resume'
					
					try:
						self.cursor.execute("update Employee set %s = \'%s\' where Eno = \'%s\'" %(col_name, col_value, key))
						self.conn.commit()
					except pyodbc.Error as e:
						msg_box = QMessageBox()
						msg_box.setWindowTitle('错误')
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
						msg_box.setWindowIcon(icon)
						msg_box.setIcon(QMessageBox.Critical)
						msg_box.setText(e)
						msg_box.addButton('我知道了', QMessageBox.AcceptRole)
						msg_box.exec()
						return

			
		self.history_record['add'] = []
		self.history_record['del'] = []
		self.history_record['update'] = {}
	
	
	
	
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	employee = Employee()
	employee.show()
	sys.exit(app.exec_())