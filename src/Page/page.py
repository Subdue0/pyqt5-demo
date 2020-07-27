# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from .Ui_page import Ui_Page, Ui_AddEmpInfoDialog
# from Ui_page import Ui_Page, Ui_AddEmpInfoDialog


class Page(QWidget, Ui_Page):
	def __init__(self, parent=None):
		super(Page, self).__init__(parent)
		self.setupUi(self)
		
		# 初始化总行数
		self.row_sum = 5
		
		self.setRowHeader(self.row_sum)
		
		self.field = ['编号', '姓名', '性别', '年龄', '电话', '学历', '部门', '职务', '身份证', '入职时间', '毕业学校', '家庭住址', '个人简介']
		self.setColumnHeader(self.field)
	
		# 初始化表格列数，一直不变
		self.col_sum = self.tableWidget.columnCount()
		
		# 设置的总列数只有5，不足以占满表格空间，故拉伸水平表头
		self.setStretch(True, False)
		
		self.setItemColorAlignment()
		
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


	'''连接SQL数据库'''
	def connectDB(self):
		try:
			import pyodbc
		
			self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=PMS;UID=sa;PWD=123456')
			self.cursor = self.conn.cursor()
		
		except Exception as e:
			print('connectDB():\n'+repr(e))
			sys.exit(-1)
	
	def signalConnection(self):
		'''表格内信号'''
		# 表格上下文菜单信号
		self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
		# 上下文菜单选项信号
		self.add.triggered.connect(self.addRow)
		self.delete.triggered.connect(self.delRow)
		self.refresh.triggered.connect(self.refreshForm)
		self.undo.triggered.connect(self.undoDelOpt)
		# 表格的单元格双击信号
		self.tableWidget.cellDoubleClicked.connect(self.recordUpdateData)
		
		'''表格外部信号'''
		# 分页栏信号
		self.form_first_page.clicked.connect(self.ctrlFormPageBar)
		self.form_previous_page.clicked.connect(self.ctrlFormPageBar)
		self.form_next_page.clicked.connect(self.ctrlFormPageBar)
		self.form_last_page.clicked.connect(self.ctrlFormPageBar)
		
		# 全局搜索信号
		self.global_search.textEdited.connect(self.globalSearchStrings)
		# 部分搜索信号
		self.search_field.currentIndexChanged.connect(self.partialSearchStrings)
		self.partial_search.textEdited.connect(self.partialSearchStrings)
		
		# 编辑状态信号
		self.editable.toggled.connect(self.setFormEditable)
		
		# 提交按钮信号
		self.submit.clicked.connect(self.submitFormData)

	
	# 创建上下文菜单
	def createContextMenu(self):
		self.tableWidget.contextMenu = QMenu(self)
		# 第一个参数加图标addAction(const QIcon &icon, const QString &text)
		add_icon = QtGui.QIcon()
		add_icon.addPixmap(QtGui.QPixmap(":form/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.add = self.tableWidget.contextMenu.addAction(add_icon, '添加')
		
		delete_icon = QtGui.QIcon()
		delete_icon.addPixmap(QtGui.QPixmap(":form/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.delete = self.tableWidget.contextMenu.addAction(delete_icon, '删除')

		undo_icon = QtGui.QIcon()
		undo_icon.addPixmap(QtGui.QPixmap(":form/images/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)		
		self.undo = self.tableWidget.contextMenu.addAction(undo_icon, '撤销')

		refresh_icon = QtGui.QIcon()
		refresh_icon.addPixmap(QtGui.QPixmap(":form/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)		
		self.refresh = self.tableWidget.contextMenu.addAction(refresh_icon, '刷新')

 
	# 菜单显示前，初始化菜单，并且将它移动到鼠标点击的位置
	def showContextMenu(self):
		# 查看历史记录，没有记录则禁用，否则可以使用
		opt_times = len(self.history_record['del'])
		if opt_times:
			self.undo.setEnabled(True)
		else:
			self.undo.setEnabled(False)
			
		if len(self.tableWidget.selectedRanges()):
			self.delete.setEnabled(True)
		else:
			self.delete.setEnabled(False)
		self.tableWidget.contextMenu.move(QtGui.QCursor.pos())
		self.tableWidget.contextMenu.show()
		
	def submitFormData(self):
		self.extractDelEmpNum()
		self.submit.setEnabled(False)
		self.history_record['add'] = []
		self.history_record['del'] = []
		self.history_record['update'] = {}
	
	def extractDelEmpNum(self):
		# 取出所有需要更新的员工号
		list_update_emp_num = list(self.history_record['update'].keys())
		'''更新下历史记录，确保要提交到数据库的历史记录准确无误'''
		for each_dict_record in self.history_record['del']:
			for each_key in list(each_dict_record.keys()):
				each_del_emp_num = each_dict_record[each_key][0]
				# 如果要被删除的员工和要更新的员工是同一个，那么去掉该员工的更新记录。
				if each_del_emp_num in list_update_emp_num:
					self.history_record['update'].pop(each_del_emp_num)
				# 如果要被删除的员工和刚添加的员工是同一个，那么去掉该员工的添加记录并且去掉该条删除记录。
				for each_add_emp_num in self.history_record['add']:
					if each_del_emp_num == each_add_emp_num[0]:
						self.history_record['add'].remove(each_add_emp_num)
						each_dict_record.pop(each_key)
	
	# 刷新表格
	def refreshForm(self):
		pass
	
	# 选择单元格数据改变后，记录选择的员工编号和字段
	def recordSubmitData(self):
		list_property = {}
		emp_num = self.tableWidget.item(self.editing_cell.row(), 0).text()
		property = self.tableWidget.horizontalHeaderItem(self.editing_cell.column()).text()
		update_text = self.editing_cell.text()
		list_property[property] = update_text
		

		if emp_num not in list(self.history_record['update'].keys()):
			self.history_record['update'][emp_num] = []		


		self.history_record['update'][emp_num].append(list_property)
		
		# 提交按钮恢复交互状态
		if self.submit.isEnabled() == False:
			self.submit.setEnabled(True)


		
	# 记录，并且只连接一次单元格的改变信号
	def recordUpdateData(self):
		self.editing_cell = self.tableWidget.currentItem()
		if not self.cell_changed_flag:
			self.tableWidget.cellChanged.connect(self.recordSubmitData)
			self.cell_changed_flag = True
	
	# 记录删除的数据
	def recordDelData(self, row_num, selected_row_opt_data):
		row_num = str(row_num)
		# 存储单行数据
		single_row_opt_data = []
		for j in range(self.col_sum):
			item_data = self.tableWidget.item(int(row_num), j).text()
			single_row_opt_data.append(item_data)
		selected_row_opt_data[row_num] = single_row_opt_data
	
	
	# 撤销删除操作，也就是插入操作，和删除操作相反，插入顺序必须按从小到大插入，否则非常难处理，因为索引之间相互影响。
	def undoDelOpt(self):
		# 单元格改变信号关闭
		if self.cell_changed_flag:
			self.tableWidget.cellChanged.disconnect()
			self.cell_changed_flag = False
	
		recent_opt_data = self.history_record['del'].pop()
		del_row_num = list(recent_opt_data.keys())
		for i in range(len(del_row_num)):
			min_row_num = int(min(del_row_num))
			# 插入最小行
			self.tableWidget.insertRow(min_row_num)
			# 指定行头的item
			header_item = QTableWidgetItem()
			self.tableWidget.setVerticalHeaderItem(min_row_num, header_item)
			# 还原最小行的表格数据
			for col_num in range(len(recent_opt_data[str(min_row_num)])):
				each_item_data = recent_opt_data[str(min_row_num)][col_num]
				# 指定最小行号的item，并设置文本
				item = QTableWidgetItem()
				item.setText(each_item_data)
				self.tableWidget.setItem(min_row_num, col_num, item)
			# 删除列表中的最小行
			del_row_num.remove(str(min_row_num))
		
		# 没有任何记录则禁用提交按钮
		if not len(self.history_record['add']) and not len(self.history_record['del']) and not len(self.history_record['update']):
			self.submit.setEnabled(False)
		
		'''分页栏和表格分页显示'''
		row_sum = self.tableWidget.rowCount()
		# 如果总行数可以被10整除且不为0，总页面数/10直接取整，否则/10直接取整+1。总行数为0，总页面数为1
		if not row_sum%10:
			# 非首页
			if self.form_cur_page_num != 1:
				# 如果当前页面在尾页，那么当前页面-1
				if self.form_cur_page_num == self.form_page_total:
					self.form_cur_page_num -= 1
			if row_sum:
				self.form_page_total = int(row_sum/10)
			else:
				self.form_page_total = 1
		else:
			self.form_page_total = int(row_sum/10) + 1
		# 初始化分页栏
		self.initFormPageBar()
		# 每次撤销都会刷新页面的分页
		self.pageBlockDisplay()

		
		# 每一次撤销操作都会影响到所有表格的排版，故更新表格
		self.updateRowHeader()
		self.updateItemColorAlignment()
		
		# 操作完后把单元格改变信号连接回去
		if not self.cell_changed_flag:
			self.tableWidget.cellChanged.connect(self.recordSubmitData)
			self.cell_changed_flag = True
	
	
	# 删除选中行，所有选中行的删除顺序，必须按行号从大到小删除，否则处理会非常麻烦，因为索引之间相互影响。
	def delRow(self):
		# 单元格改变信号关闭
		if self.cell_changed_flag:
			self.tableWidget.cellChanged.disconnect()
			self.cell_changed_flag = False
		
		# 存储选中的行号
		del_row_num = []
		# 存储选中行的行号以及数据
		selected_row_opt_data = {}
		# clicks表示Ctrl非连续多选的单击次数
		clicks = len(self.tableWidget.selectedRanges())	
		for i in range(clicks):
			top = self.tableWidget.selectedRanges()[i].topRow()
			bottom = self.tableWidget.selectedRanges()[i].bottomRow()
			
			# 记录将要被删除的一个单行的元素对象的数据
			if top == bottom:
				del_row_num.append(top)
			else:	
				# cycles表示使用Shift或单击鼠标拖拉连续选择的总数量
				cycles = bottom - top + 1
				# 记录将要被删除的一个多行的元素对象的数据
				for j in range(cycles):
					del_row_num.append(top+j)
		
		selected_row_opt_data = {}
		for i in range(len(del_row_num)):
			max_row_num = max(del_row_num)
			self.recordDelData(max_row_num, selected_row_opt_data)
			self.tableWidget.removeRow(max_row_num)
			del_row_num.remove(max_row_num)
		self.history_record['del'].append(selected_row_opt_data)
		
		row_sum = self.tableWidget.rowCount()
		# 如果总行数可以被10整除且不为0，总页面数/10直接取整，否则/10直接取整+1，总行数为0，总页面数为1
		if not row_sum%10:
			# 非首页
			if self.form_cur_page_num != 1:
				# 如果当前页面在尾页，那么当前页面-1
				if self.form_cur_page_num == self.form_page_total:
					self.form_cur_page_num -= 1
			if row_sum:
				self.form_page_total = int(row_sum/10)
			else:
				self.form_page_total = 1
		else:
			self.form_page_total = int(row_sum/10) + 1
		self.initFormPageBar()

		# 每次删除都会刷新页面的分页
		self.pageBlockDisplay()

		# 每一次删除操作都会影响到所有表格的排版，故更新表格
		self.updateRowHeader()
		self.updateItemColorAlignment()
		
		# 提交按钮恢复交互状态
		if self.submit.isEnabled() == False:
			self.submit.setEnabled(True)
		
		# 添加完后把单元格改变信号连接回去
		if not self.cell_changed_flag:
			self.tableWidget.cellChanged.connect(self.recordSubmitData)
			self.cell_changed_flag = True

		
	# 在当前行后添加新行
	def addRow(self):
		row_sum = self.tableWidget.rowCount()
		
		# 将表格中所有的员工编号传入添加员工信息对话框，以便比对添加的员工是否重复
		emp_num = []
		for each_row in range(row_sum):
			emp_num.append(self.tableWidget.item(each_row, 0).text())
		
		# 创建一个添加员工信息的模态对话框
		add_dialog = AddEmpInfoRecord(emp_num)
		add_dialog.exec_()
		# 只有读取到数据的时候才会添加新行
		if add_dialog.emp_info:
			# 单元格改变信号关闭
			if self.cell_changed_flag:
				self.tableWidget.cellChanged.disconnect()
				self.cell_changed_flag = False
			
			# 将模态对话框所获得的数据存入历史记录
			self.history_record['add'].append(add_dialog.emp_info)
			
			# 插入一个新行
			self.tableWidget.insertRow(row_sum)
			
			'''表格新添加行创建item'''
			# 指定行头的item
			header_item = QTableWidgetItem()
			self.tableWidget.setVerticalHeaderItem(row_sum, header_item)
			# 给新添的行加item
			for col_num in range(self.col_sum):
				# 指定插入的新行的item
				item = QTableWidgetItem()
				if col_num == 0 or col_num == 1:
					item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
				item.setText(add_dialog.emp_info[col_num])
				self.tableWidget.setItem(row_sum, col_num, item)
			
			
			'''分页栏改变'''
			# 如果总行数可以被10整除，那么页面总数量+1
			if not row_sum%10:
				self.form_page_total = int(row_sum/10) + 1
			# 添加新行，自动跳转到最后一页		
			self.form_cur_page_num = self.form_page_total
			self.initFormPageBar()
			# 每次添加一行都会刷新页面的分页
			self.pageBlockDisplay()
			
			# 每一次添加操作都会影响到所有表格的排版，故更新表格
			self.updateRowHeader()
			self.updateItemColorAlignment()	

			# 提交按钮恢复交互状态
			if self.submit.isEnabled() == False:
				self.submit.setEnabled(True)
				
			# 添加完后把单元格改变信号连接回去
			if not self.cell_changed_flag:
				self.tableWidget.cellChanged.connect(self.recordSubmitData)
				self.cell_changed_flag = True
			
			
	# 刷新页面的分页
	def pageBlockDisplay(self):
		row_sum = self.tableWidget.rowCount()
		# 清空之前的选择
		self.tableWidget.clearSelection()
		# 每次换页必须把之前的编辑状态给关闭了，否则导致乱七八糟的选择
		self.tableWidget.closePersistentEditor(self.tableWidget.currentItem())
		# 全部隐藏
		for i in range(row_sum):
			self.tableWidget.setRowHidden(i, True)
		
		# 部分显示
		start = 10*self.form_cur_page_num - 10
		# 最后一页的end就是总行数
		if self.form_cur_page_num == self.form_page_total:
			end = row_sum
		else:
			end = 10*self.form_cur_page_num
		for i in range(start, end):
			self.tableWidget.setRowHidden(i, False)
			
		
	# 更新行头显示
	def updateRowHeader(self):
		row_sum = self.tableWidget.rowCount()
		for each_row in range(row_sum):
			self.tableWidget.verticalHeaderItem(each_row).setTextAlignment(QtCore.Qt.AlignCenter)
			self.tableWidget.verticalHeaderItem(each_row).setText('%s' %(each_row + 1))
	
	
	# 更新所有单元格的背景颜色
	def updateItemColorAlignment(self):
		row_sum = self.tableWidget.rowCount()
		for i in range(row_sum):
			if not i%2:
				for j in range(self.col_sum):
					item = self.tableWidget.item(i, j)
					item.setBackground(QtGui.QColor(240, 240, 240))
					item.setTextAlignment(QtCore.Qt.AlignCenter)
			else:
				for j in range(self.col_sum):
					item = self.tableWidget.item(i, j)
					item.setBackground(QtGui.QColor(255, 255, 255))
					item.setTextAlignment(QtCore.Qt.AlignCenter)			
	
	# 设置所有单元格的背景颜色和文本对齐，务必在设置好行列以后调用
	def setItemColorAlignment(self):
		row_sum = self.tableWidget.rowCount()
		for i in range(row_sum):
			if not i%2:
				for j in range(self.col_sum):
					item = QTableWidgetItem()
					item.setBackground(QtGui.QColor(240, 240, 240))  
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget.setItem(i, j, item)
			else:
				for j in range(self.col_sum):
					item = QTableWidgetItem()
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget.setItem(i, j, item)	
	
	
	'''分页栏'''
	# 初始化信息表的分页栏
	def initFormPageBar(self):
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
		else:
			self.form_first_page.setEnabled(True)
			self.form_previous_page.setEnabled(True)
			self.form_next_page.setEnabled(True)
			self.form_last_page.setEnabled(True)
				

	
	# 控制表格分页栏
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
			
			self.pageBlockDisplay()
			
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
			
			self.pageBlockDisplay()
				
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
			
			self.pageBlockDisplay()

		elif obj_name == 'form_last_page':
			self.form_cur_page_num = self.form_page_total
			
			self.form_first_page.setEnabled(True)
			self.form_previous_page.setEnabled(True)
			self.form_next_page.setEnabled(False)
			self.form_last_page.setEnabled(False)
			
			self.form_page_num.setText('[%d/%d]页' %(self.form_page_total, self.form_page_total))
			
			self.pageBlockDisplay()



	'''页面'''

	# 设定公司名字，参数类型str
	def setCompanyName(self, name):
		self.groupBox.setTitle(name)
		
	# 设定表格上方的标题，参数类型str
	def setTitle(self, title):
		self.title.setText(title)
	
	# 表头拉伸，参数类型bool，bool
	def setStretch(self, horizontal, vertical):
		if horizontal:
			self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		if vertical:
			self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
			
	# 设定表头样式表
	def setFormStyleSheet(self):
		self.tableWidget.setStyleSheet("QHeaderView::section, QTableCornerButton::section {\n"
			"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(158, 225, 255, 255), stop:0.583333 rgba(0, 128, 255, 255), stop:1 rgba(0, 128, 255, 255));\n"
			"	color: white;\n"
			"	border: 1px solid #d8d8d8;\n"
			"}\n"
			"QTableWidget {\n"
			"selection-background-color: lightGreen;\n"
			"selection-color: red;\n"
			"}\n"
			"")
		
	# 设定列表头，居中对齐，文本，参数类型list
	def setColumnHeader(self, name):
		sum_col = len(name)
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
	
	# 设定表格编辑状态
	def setFormEditable(self):
		if self.editable.isChecked():
			self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
			self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed)
		else:
			self.tableWidget.customContextMenuRequested.disconnect()
			self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

	# 全局搜索框
	def globalSearchStrings(self):
		# 清空部分搜索框的内容
		self.partial_search.setText('')
	
		row_sum = self.tableWidget.rowCount()
		match_text = self.global_search.text().split()

		# 部分搜索框内容为空，表格和分页栏时为初始状态，不为空时就开始搜索
		# 单个关键词搜索模式
		if len(match_text) == 1:
			match_row_num = []
			match_item = self.tableWidget.findItems(match_text[0], QtCore.Qt.MatchContains)
			for each_item in match_item:
				match_row_num.append(each_item.row())
			# 重新赋值，去除重复行
			match_row_num = sorted(set(match_row_num), key = match_row_num.index)
			# 全部行隐藏
			for i in range(row_sum):
				self.tableWidget.setRowHidden(i, True)
			# 显示成功匹配的行
			if len(match_row_num):
				for i in match_row_num:
					self.tableWidget.setRowHidden(i, False)
			# 分页栏变成[1/1]页
			self.form_cur_page_num = 1
			self.form_page_total = 1
			self.initFormPageBar()
		# 多个关键词搜索模式
		elif len(match_text) > 1:
			match_row_num = []
			match_item = self.tableWidget.findItems(match_text[0], QtCore.Qt.MatchContains)
			for each_item in match_item:
				match_row_num.append(each_item.row())
			# 重新赋值，去除重复行
			match_row_num = sorted(set(match_row_num), key = match_row_num.index)
			# 全部行隐藏
			for i in range(row_sum):
				self.tableWidget.setRowHidden(i, True)
			
			# 筛选出match_row_num匹配到的最终匹配行
			for each_match_text in match_text:
				# 略过第一个，因为上面已经通过全局搜索得到了最开始的匹配行
				if each_match_text == match_text[0]:
					continue
				else:
					'''
					重难点：
						一定不能在循环找匹配行的时候，直接删除match_row_num中匹配的某行，
					如果那样做，结果可能会不对，因为循环已经失控，部分匹配行还没搜索就被跳过了。
					比如，a = [1, 2, 3]，在遍历打印a元素的时候，如果删掉了元素1，那么会略过2，直接打印3。
					
					解决方法：
						采用，记录需要移除的行的值，等match_row_num中全部循环完成，再对该列表进行删除操作。
					这样删除操作就不会影响到循环本身，所以也就能完美的搜索匹配所有行，而不会出现略过某些行的情况。
					'''
					# 用于记录不受匹配的行的行号
					match_row_num_del = []
					for each_match_row_num in match_row_num:
						match_text_flag = False
						for each_col in range(self.col_sum):
							if each_match_text in self.tableWidget.item(each_match_row_num, each_col).text():
								match_text_flag = True
						# 记录不受匹配的行号，也是需要删除的行号。
						if not match_text_flag:
							match_row_num_del.append(each_match_row_num)
					# 删除不受匹配的行
					for each_match_row_num_del in match_row_num_del:
						match_row_num.remove(each_match_row_num_del)
			# 显示最终成功匹配的行
			if len(match_row_num):
				for i in match_row_num:
					self.tableWidget.setRowHidden(i, False)
			# 分页栏变成[1/1]页
			self.form_cur_page_num = 1
			self.form_page_total = 1
			self.initFormPageBar()
		else:
			# 表格和分页栏恢复首页状态
			self.form_cur_page_num = 1
			if row_sum%10:
				self.form_page_total = int(row_sum/10) + 1
			else:
				self.form_page_total = int(row_sum/10)
			self.pageBlockDisplay()
			self.initFormPageBar()

	'''部分搜索'''
	# 初始化搜索字段
	def initSearchField(self):
		for each_field in self.field:
			self.search_field.addItem(each_field)
	
	# 部分搜索框
	def partialSearchStrings(self):
		# 清空全局搜索框的内容
		self.global_search.setText('')
		
		row_sum = self.tableWidget.rowCount()
		match_text = self.partial_search.text()
		# 部分搜索框内容为空，表格和分页栏时为初始状态，不为空时就开始搜索
		if match_text:
			match_row_num = []
			field_index = self.field.index(self.search_field.currentText())
			for each_row in range(row_sum):
				if match_text in self.tableWidget.item(each_row, field_index).text():
					match_row_num.append(each_row)
			# 全部行隐藏
			for i in range(row_sum):
				self.tableWidget.setRowHidden(i, True)	
			# 显示成功匹配的行
			if len(match_row_num):
				for i in match_row_num:
					self.tableWidget.setRowHidden(i, False)
			# 分页栏变成[1/1]页
			self.form_cur_page_num = 1
			self.form_page_total = 1
			self.initFormPageBar()
		else:
			self.form_cur_page_num = 1
			if row_sum%10:
				self.form_page_total = int(row_sum/10) + 1
			else:
				self.form_page_total = int(row_sum/10)
			self.pageBlockDisplay()
			self.initFormPageBar()
	
	# 设置表格第一二列不可编辑
	def setNumNameUneditable(self):
		row_sum = self.tableWidget.rowCount()
		for i in range(row_sum):
			for j in range(2):
				self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
		
	
class AddEmpInfoRecord(QDialog, Ui_AddEmpInfoDialog):
	def __init__(self, emp_num, parent=None):
		super(AddEmpInfoRecord, self).__init__(parent)
		self.setupUi(self)
		self.emp_num = emp_num
		self.emp_info = []
	
	@pyqtSlot()
	def on_add_clicked(self):
		if self.name.text() and self.number.text():
			number_text = self.number.text()
			for each_number in self.emp_num:
				if number_text == each_number:
					self.number.clearFocus()
					self.number.setText('')
					self.number.setPlaceholderText('员工编号重复')
					self.number.setAlignment(QtCore.Qt.AlignCenter)
					self.number.setStyleSheet('background-color: red')
					return
			self.emp_info.append(self.number.text())
			self.emp_info.append(self.name.text())
			if self.male.isChecked():
				self.emp_info.append('男')
			else:
				self.emp_info.append('女')
			self.emp_info.append(self.age.text())
			self.emp_info.append(self.phone.text())
			self.emp_info.append(self.educational_background.currentText())
			self.emp_info.append(self.department.currentText())
			self.emp_info.append(self.position.currentText())
			self.emp_info.append(self.ID_card.text())
			entry_time = self.year.text() + '-' + self.month.text() + '-' + self.day.text()
			self.emp_info.append(entry_time)
			self.emp_info.append(self.graduated_school.text())
			self.emp_info.append(self.home_address.text())
			self.emp_info.append(self.personal_profile.toPlainText())
			
			self.close()
		else:
			if not self.name.text():
				self.name.clearFocus()
				self.name.setPlaceholderText('必填')
				self.name.setAlignment(QtCore.Qt.AlignCenter)
				self.name.setStyleSheet('background-color: red')
			if not self.number.text():
				self.number.clearFocus()
				self.number.setPlaceholderText('必填')
				self.number.setAlignment(QtCore.Qt.AlignCenter)
				self.number.setStyleSheet('background-color: red')

				
	@pyqtSlot()
	def on_cancel_clicked(self):
		self.emp_info = []
		self.close()



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	page = Page()
	page.show()
	sys.exit(app.exec_())