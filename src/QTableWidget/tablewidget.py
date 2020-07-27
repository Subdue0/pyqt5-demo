import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from FormPageBar.form_page_bar import FormPageBar
from FormPageBar.ui_form_page_bar import Ui_FormPageBar


class TableWidget(QTableWidget):
	def __init__(self, parent=None):
		super(TableWidget, self).__init__(parent)
		self.createContextMenu()
		# 必须将ContextMenuPolicy设置为Qt.CustomContextMenu，否则无法使用customContextMenuRequested信号
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.showContextMenu)
		# 设置选择行为，以行为单位
		self.setSelectionBehavior(QAbstractItemView.SelectRows)

		self.history_record = {'add': [], 'del': []}
		
		
	
	# 创建上下文菜单
	def createContextMenu(self):
		self.contextMenu = QMenu(self)
		# 第一个参数加图标addAction(const QIcon &icon, const QString &text)
		self.add = self.contextMenu.addAction('添加') 
		self.delete = self.contextMenu.addAction('删除')
		self.undo = self.contextMenu.addAction('撤销')
		self.redo = self.contextMenu.addAction('重做')
		self.refresh = self.contextMenu.addAction('刷新')
	
		self.add.triggered.connect(self.addRow)
		self.delete.triggered.connect(self.delRow)
		self.refresh.triggered.connect(self.updateRowHeader)
		self.redo.triggered.connect(self.clearForm)
		self.undo.triggered.connect(self.undoDelOpt)
		

 
	# 菜单显示前，初始化菜单，并且将它移动到鼠标点击的位置
	def showContextMenu(self):
		# 查看历史记录，没有记录则禁用，否则可以使用
		opt_times = len(self.history_record['del'])
		if opt_times:
			self.undo.setEnabled(True)
		else:
			self.undo.setEnabled(False)
			
		if len(self.selectedRanges()):
			self.add.setEnabled(True)
			self.delete.setEnabled(True)
		else:
			self.add.setEnabled(False)
			self.delete.setEnabled(False)
		self.contextMenu.move(QtGui.QCursor.pos())
		self.contextMenu.show()
	
	def recordData(self, opt, data=None):
		if opt == 'add':
			print('添加')
		elif opt == 'del':
			print('test')
		else:
			print('tablewidget.TableWidget.recordDate(self, opt)，参数opt为"add"/"del"')
			sys.exit(-1)
		
	def recordLineData(self, row_num, selected_row_opt_data):
		row_num = str(row_num)
		
		sum_col = self.getRowColumm()[1]
		# 存储行数据
		single_row_opt_data = []
		for j in range(sum_col):
			item_data = self.item(int(row_num), j).text()
			single_row_opt_data.append(item_data)
		selected_row_opt_data[row_num] = single_row_opt_data
	
	# 撤销删除操作，也就是插入操作，和删除操作相反，插入顺序必须按从小到大插入，否则非常难处理，因为索引之间相互影响。
	def undoDelOpt(self):
		recent_opt_data = self.history_record['del'].pop()
		del_row_num = list(recent_opt_data.keys())
		for i in range(len(del_row_num)):
			min_row_num = int(min(del_row_num))
			# 插入最小行
			self.insertRow(min_row_num)
			# 指定行头的item
			header_item = QTableWidgetItem()
			self.setVerticalHeaderItem(min_row_num, header_item)
			# 还原最小行的表格数据
			for col_num in range(len(recent_opt_data[str(min_row_num)])):
				each_item_data = recent_opt_data[str(min_row_num)][col_num]
				# 指定最小行号的item，并设置文本
				item = QTableWidgetItem()
				item.setText(each_item_data)
				self.setItem(min_row_num, col_num, item)
			# 删除列表中的最小行
			del_row_num.remove(str(min_row_num))
			
		# 每一次撤销操作都会影响到所有表格的排版，故更新表格
		self.updateRowHeader()
		self.updateItemColorAlignment()
	
	# 删除选中行，所有选中行的删除顺序，必须按行号从大到小删除，否则处理会非常麻烦，因为索引之间相互影响。
	def delRow(self):
		# 存储选中的行号
		del_row_num = []
		# 存储选中行的行号以及数据
		selected_row_opt_data = {}
		# clicks表示Ctrl非连续多选的单击次数
		clicks = len(self.selectedRanges())	
		for i in range(clicks):
			top = self.selectedRanges()[i].topRow()
			bottom = self.selectedRanges()[i].bottomRow()
			
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
			self.recordLineData(max_row_num, selected_row_opt_data)
			self.removeRow(max_row_num)
			del_row_num.remove(max_row_num)
		self.history_record['del'].append(selected_row_opt_data)

		# 每一次删除操作都会影响到所有表格的排版，故更新表格
		self.updateRowHeader()
		self.updateItemColorAlignment()

		
	# 在当前行后添加新行
	def addRow(self):
		sum_row = self.getRowColumm()[0]
		sum_col = self.getRowColumm()[1]
		self.insertRow(sum_row)
		# 指定行头的item
		header_item = QTableWidgetItem()
		self.setVerticalHeaderItem(sum_row, header_item)
		# 还原最小行的表格数据
		for col_num in range(sum_col):
			# 指定插入的新行的item
			item = QTableWidgetItem()
			self.setItem(sum_row, col_num, item)
		
		# 每一次添加操作都会影响到所有表格的排版，故更新表格
		self.updateRowHeader()
		self.updateItemColorAlignment()
		
		self.editItem(self.item(sum_row, 0))
		# 每次添加必须把之前的选择状态给清除了，否则无法编辑下一个
		self.setCurrentItem(self.item(sum_row, 0), QtCore.QItemSelectionModel.Clear)
		
		
		FormPageBar.setPageNum(2, 5)
		print(FormPageBar.getPageNum())
		self.form_page_num.setText('[1/4]页')
		
		# self.pageBlockDisplay(5)
		

	def getPageTotal(self):
		sum_row = self.getRowColumm()[0]
		form_page_total = int(sum_row/10) + 1
		
		return form_page_total



	def pageBlockDisplay(self, form_cur_page_num):
		# 每次换页必须把之前的编辑状态给关闭了，否则导致乱七八糟的选择
		self.closePersistentEditor(self.currentItem())
		
		sum_row = self.getRowColumm()[0]
		form_page_total = int(sum_row/10) + 1
		
		# 全部隐藏
		for i in range(sum_row):
			self.setRowHidden(i, True)
		
		# 部分显示
		start = 10*form_cur_page_num - 10
		# 最后一页的end就是总行数
		if form_cur_page_num == form_page_total:
			end = sum_row
		else:
			end = 10*form_cur_page_num
		for i in range(start, end):
			self.setRowHidden(i, False)

		
	# 更新行头显示
	def updateRowHeader(self):
		sum_row = self.getRowColumm()[0]
		for each_row in range(sum_row):
			self.verticalHeaderItem(each_row).setTextAlignment(QtCore.Qt.AlignCenter)
			self.verticalHeaderItem(each_row).setText('%s' %(each_row + 1))
	
	# 清空表格文本
	def clearForm(self):
		row_sum, col_sum = self.getRowColumm()
		for i in range(row_sum):
			for j in range(col_sum):
				item = self.item(i, j)
				item.setText('')
	
	# 获得行列数量
	def getRowColumm(self):
		return self.rowCount(), self.columnCount()
	
	# 更新所有单元格的背景颜色
	def updateItemColorAlignment(self):
		row_sum, col_sum = self.getRowColumm()
		for i in range(row_sum):
			if not i%2:
				for j in range(col_sum):
					item = self.item(i, j)
					item.setBackground(QtGui.QColor(250, 250, 250))
					item.setTextAlignment(QtCore.Qt.AlignCenter)
			else:
				for j in range(col_sum):
					item = self.item(i, j)
					item.setBackground(QtGui.QColor(255, 255, 255))
					item.setTextAlignment(QtCore.Qt.AlignCenter)			
	
	# 设置所有单元格的背景颜色和文本对齐，务必在设置好行列以后调用
	def setItemColorAlignment(self):
		row_sum = self.getRowColumm()[0]
		col_sum = self.getRowColumm()[1]
		for i in range(row_sum):
			if not i%2:
				for j in range(col_sum):
					item = QTableWidgetItem()
					item.setBackground(QtGui.QColor(250, 250, 250))  
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.setItem(i, j, item)
			else:
				for j in range(col_sum):
					item = QTableWidgetItem()
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.setItem(i, j, item)	