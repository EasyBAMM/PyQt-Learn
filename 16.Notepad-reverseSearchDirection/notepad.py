import sys
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore


class findWindow(QDialog):
    def __init__(self, parent):
        super(findWindow, self).__init__(parent)
        uic.loadUi(
            "C:\\project-all\\Python\\pyqt\\16.Notepad-reverseSearchDirection\\find.ui", self)
        self.show()

        self.lineEdit.setFocus()
        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancle.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
            # print("up")
        elif self.radioButton_down.isChecked():
            self.up_down = "down"
            # print("down")

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
            cs = QtCore.Qt.CaseSensitive    # 민감하다.
        else:
            cs = QtCore.Qt.CaseInsensitive    # 민감하지 않다.

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos)    # 검색 하기!
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)

        if index != -1 and (pos > -1):  # 검색된 결과가 있다면
            self.setCursor(index, len(pattern)+index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        # print(self.cursor.selectionStart(), self.cursor.selectionEnd()) # 현재 커서 위치
        self.cursor.setPosition(start)   # 앞에 커서를 찍고
        self.cursor.movePosition(
            QTextCursor.Right, QTextCursor.KeepAnchor, end-start)    # 뒤로 커서를 움직인다
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("메모장")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''{}을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton("확인", QMessageBox.YesRole)
        ret = msgBox.exec_()


form_class = uic.loadUiType(
    "C:\\project-all\\Python\\pyqt\\16.Notepad-reverseSearchDirection\\notepad.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveas.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)

        self.action_find.triggered.connect(self.findFunction)

        self.opened = False
        self.opened_file_path = "제목 없음"

    def isChanged(self):
        if not self.opened:  # 열린적은 없는데 에디터 내용이 있으면
            if self.plainTextEdit.toPlainText().strip():
                return True
            return False

        # 현재 데이터
        current_data = self.plainTextEdit.toPlainText()
        # 파일에 저장된 데이터
        with open(self.opened_file_path, encoding="UTF8") as f:
            file_data = f.read()

        if current_data == file_data:   # 열린적이 있고 변경사항이 없으면
            return False
        else:   # 열린적이 있고 변경사항이 있으면
            return True

    def save_changed_data(self):

        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton("저장", QMessageBox.YesRole)  # 0
        msgBox.addButton("저장 안 함", QMessageBox.NoRole)  # 1
        msgBox.addButton("취소", QMessageBox.RejectRole)  # 2
        ret = msgBox.exec_()

        if ret == 0:
            self.saveFunction()
        else:
            return ret

    def closeEvent(self, event):
        if self.isChanged():    # 열린적이 있고 변경사항이 있으면, 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()

    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()

        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)

        self.opened = True
        self.opened_file_path = fname

        print("save {}!!".format(fname))

    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()
        self.plainTextEdit.setPlainText(data)

        self.opened = True
        self.opened_file_path = fname

        print("open {}!!".format(fname))

    def openFunction(self):
        if self.isChanged():    # 열린적이 있고 변경사항이 있으면, 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()

        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plaintTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def findFunction(self):
        findWindow(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()
