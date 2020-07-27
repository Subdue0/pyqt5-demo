# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\Eric6_Workspace\form_page.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormPageBar(object):
    def setupUi(self, FormPageBar):
        FormPageBar.setObjectName("FormPageBar")
        FormPageBar.resize(696, 492)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FormPageBar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.form_first_page = QtWidgets.QPushButton(FormPageBar)
        self.form_first_page.setFocusPolicy(QtCore.Qt.NoFocus)
        self.form_first_page.setObjectName("form_first_page")
        self.horizontalLayout.addWidget(self.form_first_page)
        self.form_previous_page = QtWidgets.QPushButton(FormPageBar)
        self.form_previous_page.setFocusPolicy(QtCore.Qt.NoFocus)
        self.form_previous_page.setObjectName("form_previous_page")
        self.horizontalLayout.addWidget(self.form_previous_page)
        self.form_page_num = QtWidgets.QLabel(FormPageBar)
        self.form_page_num.setAlignment(QtCore.Qt.AlignCenter)
        self.form_page_num.setObjectName("form_page_num")
        self.horizontalLayout.addWidget(self.form_page_num)
        self.form_next_page = QtWidgets.QPushButton(FormPageBar)
        self.form_next_page.setFocusPolicy(QtCore.Qt.NoFocus)
        self.form_next_page.setObjectName("form_next_page")
        self.horizontalLayout.addWidget(self.form_next_page)
        self.form_last_page = QtWidgets.QPushButton(FormPageBar)
        self.form_last_page.setFocusPolicy(QtCore.Qt.NoFocus)
        self.form_last_page.setObjectName("form_last_page")
        self.horizontalLayout.addWidget(self.form_last_page)

        self.retranslateUi(FormPageBar)
        QtCore.QMetaObject.connectSlotsByName(FormPageBar)

    def retranslateUi(self, FormPageBar):
        _translate = QtCore.QCoreApplication.translate
        FormPageBar.setWindowTitle(_translate("FormPageBar", "Form"))
        self.form_first_page.setText(_translate("FormPageBar", "首页"))
        self.form_previous_page.setText(_translate("FormPageBar", "上一页"))
        self.form_page_num.setText(_translate("FormPageBar", "[50/200]页"))
        self.form_next_page.setText(_translate("FormPageBar", "下一页"))
        self.form_last_page.setText(_translate("FormPageBar", "尾页"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormPageBar = QtWidgets.QWidget()
    ui = Ui_FormPageBar()
    ui.setupUi(FormPageBar)
    FormPageBar.show()
    sys.exit(app.exec_())

