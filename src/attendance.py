# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication

from Page.page import Page



class Attendance(Page):
	def __init__(self, parent=None):
		super(Page, self).__init__(parent)
		self.setupUi(self)
		
		self.getDataFromDB()
		self.setRowHeader(self.row_sum)
		
		self.field = ['编号', '姓名', '迟到', '早退', '病假', '事假', '旷工']
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
		
		except Exception as e:
			print('getDataFromDB():\n'+repr(e))
			sys.exit(-1)

	'''初始化表格数据'''
	def initFormDate(self):
		for each_row in range(self.row_sum):
			for each_col in range(self.col_sum):
				if self.row[each_row][each_col]:
					item_text = str(self.row[each_row][each_col])
					self.tableWidget.item(each_row, each_col).setText(item_text)
		
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
	attendance = Attendance()
	attendance.show()
	sys.exit(app.exec_())