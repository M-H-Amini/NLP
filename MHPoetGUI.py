import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from MHPoet import *
import multiprocessing

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("PoetGUI.ui", self)
        self.startButton.clicked.connect(self.start)
        self.Slider.valueChanged.connect(self.setPoem)

    def start(self):
        text = self.textEdit.text()
        N = int(self.NEdit.text())
        no = int(self.NoEdit.text())
        step = int(self.stepEdit.text())
        hafez_stat = self.hafezBox.isChecked()
        saadi_stat = self.saadiBox.isChecked()
        poems = []
        if hafez_stat:
            poems.extend(readFromFile('Saadi.txt'))
        if saadi_stat:
            poems.extend(readFromFile('Hafez.txt'))
        unique_words = set([word for poem in poems for word in poem.split()])
        unique_words = preprocessWords(unique_words)
        no_of_words = len(unique_words)
        self.statLabel.setText("در حال پردازش...")
        self.completed = completeIt([text], N, no, step, unique_words, poems)
        self.statLabel.setText("تمام!")
        self.Slider.setMinimum(1)
        self.Slider.setMaximum(len(self.completed))
        self.completedLabel.setText(str(self.completed[0]))

    def setPoem(self):
        index = self.Slider.value()
        self.completedLabel.setText(self.completed[index-1])
        print(self.completed[index-1])        
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()