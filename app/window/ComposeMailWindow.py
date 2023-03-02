import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QLineEdit, QTextEdit
)

from app.QtExt import util
from app.QtExt.QSeparationLine import QHSeparationLine

import mail


# ----------
# logging
# ----------


logger = logging.getLogger(__name__)


# ----------
# ComposeMailWindow
# ----------


class ComposeMailWindow(QScrollArea):
    def __init__(self, mail_transmitter: mail.Transmitter) -> None:
        super().__init__()

        # ----------
        # IServ
        # ----------

        self._mail_transmitter = mail_transmitter

        # ----------
        # window setting
        # ----------

        self.setWindowTitle('IScrA')

        # ----------
        # actions
        # ----------

        self.exit_action = QAction('Exit', self)
        self.exit_action.setStatusTip('Closes the application')
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(QApplication.instance().exit)

        # ----------
        # compose mail layout
        # ----------

        # to user
        self.to_user_info_label = QLabel('To user: ')
        self.to_user_info_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.to_user_info_label.setStyleSheet('QLabel { font-weight: bold; }')

        self.to_user_input = QLineEdit()
        self.to_user_input.setPlaceholderText('user.name')
        self.to_user_input.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)

        self.to_user_layout = QHBoxLayout()
        self.to_user_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.to_user_layout.addWidget(self.to_user_info_label)
        self.to_user_layout.addWidget(self.to_user_input)

        self.to_user_widget = QWidget()
        self.to_user_widget.setLayout(self.to_user_layout)

        # subject
        self.subject_info_label = QLabel('Subject: ')
        self.subject_info_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.subject_info_label.setStyleSheet('QLabel { font-weight: bold; }')

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText('Subject')
        self.subject_input.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)

        self.subject_layout = QHBoxLayout()
        self.subject_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.subject_layout.addWidget(self.subject_info_label)
        self.subject_layout.addWidget(self.subject_input)

        self.subject_widget = QWidget()
        self.subject_widget.setLayout(self.subject_layout)

        # body
        self.body_input = QTextEdit()
        self.body_input.setAcceptRichText(False)
        self.body_input.setPlaceholderText('Body')
        self.body_input.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        # send button
        self.send_mail_button = QPushButton('Send')
        self.send_mail_button.clicked.connect(self.send_mail)
        self.send_mail_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # ----------
        # main layout
        # ----------

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.to_user_widget)
        self.main_layout.addWidget(self.subject_widget)
        self.main_layout.addWidget(self.body_input)
        self.main_layout.addWidget(self.send_mail_button)

        self.main_widget = QWidget()
        self.main_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        self.main_widget.setLayout(self.main_layout)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)

        self.setWidget(self.main_widget)

    def empty_inputs(self) -> None:
        self.to_user_input.setText('')
        self.subject_input.setText('')
        self.body_input.setText('')

    def send_mail(self) -> None:
        try:
            self._mail_transmitter.send_mail(
                to_user=self.to_user_input.text(),
                subject=self.subject_input.text(),
                body=self.body_input.toPlainText(),
                formatted_body=False)

            self.empty_inputs()
            self.close()

        except Exception as exception:
            logger.exception(exception)

    def shutdown(self) -> None:
        # log out and close connections
        pass

    def close(self) -> None:
        super().close()

        # log out and close connections
        self.shutdown()