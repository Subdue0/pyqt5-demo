# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\Eric6_Workspace\chg_passwd.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_childWindow(object):
    def setupUi(self, childWindow):
        childWindow.setObjectName("childWindow")
        childWindow.resize(391, 300)
        childWindow.setMaximumSize(QtCore.QSize(400, 300))
        childWindow.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(childWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(71, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(childWindow)
        self.okButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.okButton.setAutoDefault(False)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.btn_cancel = QtWidgets.QPushButton(childWindow)
        self.btn_cancel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_cancel.setAutoDefault(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.hboxlayout.addWidget(self.btn_cancel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.hboxlayout, 4, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(childWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(childWindow)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(childWindow)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(childWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 5, 0, 1, 2)

        self.retranslateUi(childWindow)
        QtCore.QMetaObject.connectSlotsByName(childWindow)

    def retranslateUi(self, childWindow):
        _translate = QtCore.QCoreApplication.translate
        childWindow.setWindowTitle(_translate("childWindow", "修改密码"))
        self.okButton.setText(_translate("childWindow", "确定"))
        self.btn_cancel.setText(_translate("childWindow", "取消"))
        self.label_3.setText(_translate("childWindow", "原密码："))
        self.label_4.setText(_translate("childWindow", "新密码："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    childWindow = QtWidgets.QDialog()
    ui = Ui_childWindow()
    ui.setupUi(childWindow)
    childWindow.show()
    sys.exit(app.exec_())

