from PyQt5.QtWidgets import QLabel


class QtClickLabel(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        
    def clicked(self):
        
