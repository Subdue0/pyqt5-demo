# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from login import LoginDialog
from mainwindow import MainWindow


def main():
	app = QApplication(sys.argv)
	login = LoginDialog()
	# test = 1
	# while True:
	login.exec_()
		if login.login_success:
			mainwindow = MainWindow(login)
			mainwindow.show()
			login = LoginDialog(mainwindow)
			login.exec_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()