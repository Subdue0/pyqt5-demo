# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\Eric6_Workspace\QTableWidget\form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from FormPageBar.form_page_bar import FormPageBar
from tablewidget import TableWidget

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(800, 600)
		self.verticalLayout = QtWidgets.QVBoxLayout(Form)
		self.verticalLayout.setObjectName("verticalLayout")
		self.groupBox = QtWidgets.QGroupBox(Form)
		self.groupBox.setObjectName("groupBox")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.title = QtWidgets.QLabel(self.groupBox)
		self.title.setStyleSheet("background-color: rgb(218, 218, 218);")
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.title.setObjectName("title")
		self.verticalLayout_2.addWidget(self.title)
		self.tableWidget = TableWidget(self.groupBox)
		self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
		self.tableWidget.setGridStyle(QtCore.Qt.DashDotLine)
		self.tableWidget.setCornerButtonEnabled(False)
		self.tableWidget.setRowCount(5)
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setObjectName("tableWidget")
		self.verticalLayout_2.addWidget(self.tableWidget)
		
		
		
		# cur_page_num, page_total = self.tableWidget.getPageNum()
		# self.tableWidget.pageBlockDisplay()
		# self.form_page_bar = FormPageBar(cur_page_num, page_total)
		# self.verticalLayout_2.addWidget(self.form_page_bar)
		
		self.verticalLayout.addWidget(self.groupBox)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.groupBox.setTitle(_translate("Form", "XXX公司"))
		self.title.setText(_translate("Form", "员工信息表"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())

