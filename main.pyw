import sys
from ctypes import windll
from threading import Thread

from PyQt5 import QtWidgets as qtws, QtGui as qtg, QtCore as qtc

import config
from stt import va_listen
from tts import va_speak
from process_cmds import va_respond


class DanyaTheVA(qtws.QWidget):
    def __init__(self):
        super().__init__()
        self.used = False
        self.w = 600
        self.h = 200
        qtg.QFontDatabase.addApplicationFont('gothic.ttf')
        self.font_ = 'Century Gothic'
        self.setGeometry((windll.user32.GetSystemMetrics(0) - self.w) // 2,
                         (windll.user32.GetSystemMetrics(1) - self.h) // 2, self.w, self.h)
        self.setWindowTitle(f'{config.VA_NAME} v{config.VA_VER}')
        self.setWindowIcon(qtg.QIcon('icon.png'))
        self.setFixedSize(self.size())
        self.listen_btn = qtws.QPushButton('Слушать', self)
        self.listen_btn.setFont(qtg.QFont(self.font_, 20, 50))
        self.listen_btn.resize(150, 50)
        self.listen_btn.move(10, 10)
        self.listen_btn.clicked.connect(self.clicked)
        self.explain_label = qtws.QLabel('Чтобы обратиться к ассистенту, начните со слова\n"Даня" или нажмите кнопку "Слушать" и говорите.', self)
        self.explain_label.setFont(qtg.QFont(self.font_, 12))
        self.explain_label.resize(self.explain_label.sizeHint())
        self.explain_label.move(170, 15)
        self.executed_command = qtws.QLabel(self)
        self.executed_command.setFont(qtg.QFont(self.font_, 14))
        self.executed_command.resize(self.w - 20, 130)
        self.executed_command.move(10, 70)
        self.executed_command.setAlignment(qtc.Qt.AlignHCenter)
        self.listen_indef()

    def listen_indef(self):
        def alisten():
            prev_phrase = ''
            for phrase in va_listen():
                if phrase and phrase != prev_phrase:
                    answer = va_respond(phrase, not self.used)
                    print(answer)
                    self.executed_command.setText(answer)
                    try:
                        va_speak(answer)
                    except ValueError:
                        pass
                    if answer == 'Пока! До скорой встречи...':
                        self.close()
                        sys.exit()
                prev_phrase = phrase
                self.used = False
        Thread(target=alisten).start()

    def clicked(self):
        def aclicked():
            self.listen_btn.setText('Говорите!')
            self.used = True
            while self.used:
                pass
            self.listen_btn.setText('Слушать')
        if self.used:
            return
        Thread(target=aclicked).start()


if __name__ == '__main__':
    app = qtws.QApplication(sys.argv)
    ex = DanyaTheVA()
    ex.show()
    sys.exit(app.exec())
