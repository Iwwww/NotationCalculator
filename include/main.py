import sys

import pyperclip
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QPushButton, QComboBox, QHBoxLayout, QLineEdit, \
    QSizePolicy, QGridLayout, QSpinBox, QLabel, QPlainTextEdit, \
    QShortcut
import resources

import BaseToBase as BTB


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notation calculator")
        self.setMinimumSize(400, 180)
        self.setMaximumHeight(250)
        self.resize(450, 180)

        '''
        mainLayout {
            calculateLayout {
                enterLayout {
                    first-secondNums
                    singBox
                }
                resultBox
                enterLayout {
                    btnEnter
                    btnCopy
                }
            }
        }
        '''

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(8)
        self.setLayout(self.mainLayout)

        self.calculateLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.calculateLayout)

        self.inputLayout = QGridLayout()
        self.calculateLayout.addLayout(self.inputLayout)

        self.firstNum = QLineEdit()
        self.firstNum.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.firstNum.setClearButtonEnabled(True)
        self.firstNum.setPlaceholderText("First number")
        self.inputLayout.addWidget(self.firstNum, 0, 0)

        self.signBox = QComboBox()
        self.signBox.addItems(["+", "-", "*"])
        self.signBox.setGeometry(200, 200, 200, 200)
        self.signBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.inputLayout.addWidget(self.signBox, 0, 1)

        self.secondNum = QLineEdit()
        self.secondNum.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.secondNum.setClearButtonEnabled(True)
        self.secondNum.setPlaceholderText("Second number (empty)")
        self.inputLayout.addWidget(self.secondNum, 0, 2)

        self.inputBaseLayout = QHBoxLayout()
        self.inputLayout.addLayout(self.inputBaseLayout, 1, 0)

        self.inputBaseLayout.addWidget(QLabel("Input base:"))

        self.inputBase = QSpinBox()
        self.inputBase.setMinimum(2)
        self.inputBase.setMaximum(36)
        self.inputBase.setValue(10)
        self.inputBase.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.inputBaseLayout.addWidget(self.inputBase)

        self.outputBaseLayout = QHBoxLayout()
        self.inputLayout.addLayout(self.outputBaseLayout, 1, 2)

        self.outputBaseLayout.addWidget(QLabel("Output base:"))

        self.outputBase = QSpinBox()
        self.outputBase.setMinimum(2)
        self.outputBase.setMaximum(36)
        self.outputBase.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.outputBaseLayout.addWidget(self.outputBase)

        self.resultBox = QPlainTextEdit()
        self.resultBox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.resultBox.setReadOnly(True)
        self.calculateLayout.addWidget(self.resultBox)

        self.enterLayout = QHBoxLayout()
        self.calculateLayout.addLayout(self.enterLayout)

        self.btnEnter = QPushButton("Enter")
        self.btnEnter.setMinimumSize(0, 35)
        self.btnEnter.setEnabled(False)
        self.enterLayout.addWidget(self.btnEnter)

        self.btnCopy = QPushButton("Copy")
        self.btnCopy.setMinimumSize(0, 35)
        self.btnCopy.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btnCopy.setEnabled(False)
        self.enterLayout.addWidget(self.btnCopy)

        # Connect
        self.btnEnter.clicked.connect(self.runClicked)
        self.btnCopy.clicked.connect(self.copyClicked)

        self.firstNum.textChanged.connect(self.inputCheckFirst_num)
        self.firstNum.textChanged.connect(self.inputChanged)
        self.secondNum.textChanged.connect(self.inputCheckSecond_num)
        self.secondNum.textChanged.connect(self.inputChanged)

        self.inputBase.valueChanged.connect(self.inputCheckFirst_num)
        self.inputBase.valueChanged.connect(self.inputCheckSecond_num)
        self.inputBase.valueChanged.connect(self.inputBaseChanged)
        self.outputBase.valueChanged.connect(self.inputBaseChanged)

        self.signBox.currentIndexChanged.connect(self.inputChanged)

        self.shortcut_runReturn = QShortcut(QKeySequence('Return'), self)
        self.shortcut_runReturn.activated.connect(self.shortcutRun)
        self.shortcut_runEnter = QShortcut(QKeySequence('Enter'), self)
        self.shortcut_runEnter.activated.connect(self.shortcutRun)
        self.shortcut_copy = QShortcut(QKeySequence('Ctrl+C'), self)
        self.shortcut_copy.activated.connect(self.shortcutCopy)

    def runClicked(self):
        first_num = self.firstNum.text()
        second_num = self.secondNum.text()
        sign = self.signBox.currentText()
        input_base: int = self.inputBase.value()
        output_base: int = self.outputBase.value()
        result = None

        # Check for waste numbers
        # flag = True
        # alphabet = BTB.getAlphabet(type="string")
        # for i in first_num:
        #     if i in alphabet[int(input_base)::]:
        #         flag = False
        #         result = "Error"
        #         break

        if first_num != '':  # and flag == True:
            if second_num == '':
                result = BTB.baseToBase(first_num, input_base, output_base)
            else:
                try:
                    a = BTB.baseToDec(first_num, input_base)
                    b = BTB.baseToDec(second_num, input_base)
                    if sign == "+":
                        result = BTB.decToBase(a + b, output_base)
                    elif sign == "-":
                        result = BTB.decToBase(a - b, output_base)
                    elif sign == "*":
                        result = BTB.decToBase(a * b, output_base)
                    # elif sign == "/":
                    #     result = BTB.decToBase(a / b, output_base)

                except Exception as e:
                    result = "Error,", e
                    print(e, type(e))

        self.resultBox.setPlainText(result)

        self.resultBox.setStyleSheet("color: black;")
        self.btnCopy.setEnabled(True)

    def copyClicked(self):
        text = self.resultBox.toPlainText()
        if text != '' and text[::5] != "Error":
            pyperclip.copy(text)

    def shortcutRun(self):
        if self.btnEnter.isEnabled() == True:
            self.runClicked()

    def shortcutCopy(self):
        if self.btnCopy.isEnabled() == True:
            self.copyClicked()

    def inputCheckFirst_num(self):
        first_num = self.firstNum.text()

        if first_num.isupper() == False:
            first_num = first_num.upper()


        # Replace '-' from center in string
        if '-' in first_num[1::]:
            first_num = first_num[0] + first_num[1::].replace('-', '')

        # tmp = first_num

        for sign in first_num:
            if sign not in "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                first_num = first_num.replace(sign, '')
            elif "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(sign) - 1 >= self.inputBase.value():
                first_num = first_num.replace(sign, '')

        # self.inputChanged()
        self.firstNum.setText(first_num)


    def inputCheckSecond_num(self):
        second_num = self.secondNum.text()

        if second_num.isupper() == False:
            second_num = second_num.upper()

        # tmp = second_num

        # Replace '-' from center in string
        if '-' in second_num[1::]:
            second_num = second_num[0] + second_num[1::].replace('-', '')

        for sign in second_num:
            if sign not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-":
                second_num = second_num.replace(sign, '')
            elif "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(sign) - 1 >= self.inputBase.value():
                second_num = second_num.replace(sign, '')

        self.secondNum.setText(second_num)
        # if tmp == second_num:
        #     self.inputChanged()

    def inputChanged(self):
        if self.firstNum.text() == '' or self.firstNum.text() == '-':
            self.resultBox.setPlainText('')
            self.btnEnter.setEnabled(False)
            self.btnCopy.setEnabled(False)
        else:
            self.resultBox.setStyleSheet("color: gray;")
            self.btnCopy.setEnabled(False)
            self.btnEnter.setEnabled(True)

    def inputBaseChanged(self):
        self.resultBox.setStyleSheet("color: gray;")
        self.btnCopy.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/icons/calculator-icon.ico'))
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
