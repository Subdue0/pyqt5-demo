# -*- coding: utf-8 -*-


from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Ui_login import Ui_LoginDialog
from Ui_login import ClickedLabel

from mainwindow import MainWindow

import os
import sys
import json
import hashlib


class LoginDialog(QDialog, Ui_LoginDialog):
	def __init__(self, parent=None):
		super(LoginDialog, self).__init__(parent)
		self.setupUi(self)
		self.setStyleSheet(TextStyle)
		self.login_success = False
		self.initLoginInfo()
		self.focusPosition()
	
	def focusPosition(self):
		if not self.account_number.text():
			self.account_number.setFocus(True)
		elif not self.password.text():
			self.password.setFocus(True)
		else:
			self.verification_code.setFocus(True)
	
	def loadConfig(self):
		json_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\login.json'
		if os.path.exists(json_path):
			with open(json_path, 'r') as f:
				self.login_info = json.load(f)
				return True
		else:
			self.login_info = {}
			return False
		
	def initLoginInfo(self):
		if self.loadConfig():
			if 'account_number' in self.login_info.keys():
				self.remember_account_number.setChecked(True)
				self.account_number.setText(self.login_info['account_number'])
			else:
				self.remember_account_number.setChecked(False)
			
			if 'password' in self.login_info.keys():
				self.remember_password.setChecked(True)
				self.password.setText(self.login_info['password'])
			else:
				self.remember_password.setChecked(False)

			
			if 'server_name' in self.login_info.keys():
				self.server_name.setText(self.login_info['server_name'])
			if 'database_name' in self.login_info.keys():
				self.database_name.setText(self.login_info['database_name'])
			if 'username' in self.login_info.keys():
				self.username.setText(self.login_info['username'])
			if 'database_password' in self.login_info.keys():
				self.database_password.setText(self.login_info['database_password'])
		
		
		
	@pyqtSlot()
	def on_confirm_clicked(self):
		# 清除焦点
		self.server_name.clearFocus()
		self.username.clearFocus()
		self.database_password.clearFocus()
		# 换页
		self.stackedWidget.setCurrentIndex(0)
	
	@pyqtSlot()
	def on_go_back_1_clicked(self):
		# 清除焦点
		self.server_name.clearFocus()
		self.username.clearFocus()
		self.database_password.clearFocus()
		# 换页
		self.stackedWidget.setCurrentIndex(0)

	'''连接SQL数据库'''
	def connectDB(self, server, database, uid, pwd):
		try:
			import pyodbc
			
			conn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' %(server, database, uid, pwd))
			self.cursor = conn.cursor()
		
		except Exception as e:
			print('connectDB():\n'+repr(e))
			sys.exit(-1)		

	def verifyPassword(self):
		self.cursor.execute('select * from User')
			
		self.row = self.cursor.fetchall()
		print(self.row)
		# self.row_sum = len(self.row)
		# if right:
			# return True
		# else:
			# return False
		
	
	@pyqtSlot()
	def on_login_clicked(self):
		# 用户登录
		account_number = self.account_number.text()
		if self.password.text():
			if len(self.password.text()) != 32:
				password = hashlib.md5(self.password.text().encode('utf-8')).hexdigest()
			else:
				password = self.password.text()
		else:
			password = ''
		# 数据库登录
		server_name = self.server_name.text()
		database_name = self.database_name.text()
		username = self.username.text()
		database_password = self.database_password.text()
		
		if self.login_info:
			if self.remember_account_number.isChecked():
				if account_number != self.login_info['account_number']:
					self.login_info['account_number'] = account_number
			else:
				if 'account_number' in self.login_info.keys():
					self.login_info['account_number'] = ''
			if self.remember_password.isChecked():
				if password != self.login_info['password']:
					self.login_info['password'] = password
			else:
				if 'password' in self.login_info.keys():
					self.login_info['password'] = ''
			if server_name != self.login_info['server_name']:
				self.login_info['server_name'] = server_name
			if database_name != self.login_info['database_name']:
				self.login_info['database_name'] = database_name
			if username != self.login_info['username']:
				self.login_info['username'] = username
			if database_password != self.login_info['database_password']:
				self.login_info['database_password'] = database_password
		else:
			self.login_info['account_number'] = account_number
			self.login_info['password'] = password
			self.login_info['server_name'] = server_name
			self.login_info['database_name'] = database_name
			self.login_info['username'] = username
			self.login_info['database_password'] = database_password

		
		print(self.login_info)
		json_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\login.json'
		with open(json_path, 'w') as f:
			f.write(json.dumps(self.login_info))

		
		
		self.connectDB(server_name, database_name, username, database_password)
		# self.verifyPassword()
		
		
		print(self.str_verification_code)
		verification_code = self.verification_code.text()
		if not verification_code:
			msg_box = QMessageBox()
			msg_box.setWindowTitle('提示')
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			msg_box.setWindowIcon(icon)
			msg_box.setIcon(QMessageBox.Information)
			msg_box.setText('验证码不能为空!')
			msg_box.addButton('我知道了', QMessageBox.AcceptRole)
			msg_box.exec()
		else:
			if verification_code != self.str_verification_code:
				msg_box = QMessageBox()
				msg_box.setWindowTitle('错误')
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(":/mainwindow/images/mainwindow/money-bag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				msg_box.setWindowIcon(icon)
				msg_box.setIcon(QMessageBox.Critical)
				msg_box.setText('验证码错误!')
				msg_box.addButton('我知道了', QMessageBox.AcceptRole)
				msg_box.exec()
		
		
		self.login_success = True
		self.hide()
		# self.parent().show()
		self.mainwindow = MainWindow(self)
		self.mainwindow.show()
		
		
		
		# 记住账号和密码
		# if self.remember_password.isChecked():
			# self.login_info['account_number'] = account_number
			# self.login_info['password'] = password
			
			# print('账号：%s' %account_number)
			# print('密码：%s' %password)			
			
		# 记住账号
		# else:
			# if self.remember_account_number.isChecked():
				# self.login_info['account_number'] = account_number
				# print('账号：%s' %account_number)
				# if self.load_password:
					# json_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\login.json'
					# if os.path.exists(json_path):
						# with open(json_path, 'r') as f:
							# login_info = json.load(f)
						# print(login_info)
						
						
				# if self.login_info['remember_password'] == 'True':
					# self.load_account_number = self.login_info['account_number']
					# self.load_password = self.login_info['password']
					# self.remember_account_number.setChecked(True)
					# self.remember_password.setChecked(True)
					# self.account_number.setText(self.load_account_number)
					# self.password.setText(self.load_password)
				# else:
		
		
		# if self.emp.isChecked():
			# print('员工登录')
		# else:
			# print('管理员登录')
		
		# if 

		

		
		# login_info = {}
		
		# if self.remember_password.isChecked():
			# if self.load_account_number == self
			# m = hashlib.md5(password.encode('utf-8'))
			# self.login_info['remember_account_number'] = 'True'
			# self.login_info['remember_password'] = 'True'
			# self.login_info['account_number'] = account_number
			# self.login_info['password'] = m.hexdigest()
		# else:
			# self.login_info['remember_password'] = 'False'
			# if self.remember_account_number.isChecked():
				# self.login_info['remember_account_number'] = 'True'
				# self.login_info['account_number'] = account_number

				


					
					
					
				
		# if self.emp.isChecked():
			# print('员工登录')
			# self.login_info['user_type'] = 'emp'
		# else:
			# self.login_info['user_type'] = 'admin'
			# print('管理员登录')
		
		
		
		# with open(json_path, 'w') as f:
			# f.write(json.dumps(login_info))

		
		# print(os.path.dirname(os.path.realpath(sys.argv[0])))


		# if self.account_number
		
		
	@pyqtSlot()
	def on_go_back_2_clicked(self):
		self.stackedWidget.setCurrentIndex(0)

	@pyqtSlot()
	def on_remember_password_clicked(self):
		if not self.remember_account_number.isChecked():
			self.remember_account_number.setChecked(True)

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
	login = LoginDialog()
	login.show()
	sys.exit(app.exec_())


