# -*- coding: utf-8 -*-

"""
Module implementing FormPageBar.
"""


from PyQt5 import QtWidgets

from Ui_form_page import Ui_FormPageBar


class FormPageBar(QtWidgets.QWidget, Ui_FormPageBar):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        print(parent)
        super(FormPageBar, self).__init__(parent)
        self.setupUi(self)
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = FormPageBar()
    ui.show()

    sys.exit(app.exec_())
