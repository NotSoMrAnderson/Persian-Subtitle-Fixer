from os import getenv

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from subtitle_processor import main


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(r"assets\comics-mask_97446.ico"))

        layout = QVBoxLayout()
        layout.addWidget(MyBar(self))
        layout.addWidget(NewLabel(self))
        self.setWindowOpacity(1 - 15 / 100)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(-1)
        self.setMinimumSize(400, 110)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False


class MyBar(QWidget):
    __version__ = getenv("APP_VERSION", "0.0.0")

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.MBlayout = QHBoxLayout()
        self.MBlayout.setContentsMargins(0, 0, 5, 5)
        self.title = QLabel("Sub Fixer " + self.__version__)

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(26, 16)
        self.btn_close.setStyleSheet(
            " QPushButton::hover{background-color : red}; color:white ; font: bold; border-radius: 3px;padding-bottom:3px;")

        self.btn_min = QPushButton("_")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(26, 16)
        self.btn_min.setStyleSheet(
            " QPushButton::hover{background-color : #808080}; color:white; font: bold; border-radius: 3px;padding-bottom:3px;")

        self.btn_help = QPushButton("?")
        self.btn_help.setFixedSize(14, 14)
        self.btn_help.setStyleSheet(
            " QToolTip{font-size:11px ; font: bold; color:black; font-family: Segoe print; border:1px solid black; border-radius: 0px}; color:red ; border-radius: 7px; padding-left:1px; padding-bottom:1px; border: 1px solid red")
        self.btn_help.setToolTip('Supported Formats: srt, SRT, ass\n PS: Use Files with utf8 or ansi Encoding')

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignLeft)
        self.MBlayout.addWidget(self.title)
        self.MBlayout.addWidget(self.btn_help)
        self.MBlayout.addWidget(self.btn_min)
        self.MBlayout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            padding-top: 8px;
            padding-left: 4px;
            background-color: black;
            color: white;
            font: bold;
            font-family: Segoe print;
        """)
        self.setLayout(self.MBlayout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(self.mapToGlobal(movement).x(),
                                    self.mapToGlobal(movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()


class NewLabel(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.stat = False
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag & Drop your Subtitle here.\nEnjoy ;)")
        self.setFixedSize(400, 55)
        self.setStyleSheet("""
                     border: 3px dashed red;
                     margin-left:5px;
                     margin-right:5px;
                     padding:5px;
                     color: Black;
                     font: bold;
                     font-family: Segoe print;

                 """)

    def reset(self):
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag & Drop your Subtitle here.\nEnjoy ;)")
        self.stat = False

    def mousePressEvent(self, event):
        if self.stat:
            start = self.mapToGlobal(event.pos())
            pressing = True
            self.reset()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                # else:       # for next version catch sub from url
                #     links.append(str(url.toString()))
            num = main(links)
            self.change_label(num)

        else:
            event.ignore()

    def change_label(self, count='0'):
        self.stat = True
        self.setText("Done! {} Files were not supported Files\nClick for Fixing more. ".format(count))
        self.setAcceptDrops(False)
