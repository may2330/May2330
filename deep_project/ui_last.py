# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui',
# licensing of 'main.ui' applies.
#
# Created: Fri Oct  4 17:54:56 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

import os
import time

import numpy as np
import cv2
from datetime import datetime, date
from heatmappy import Heatmapper
import numpy as np
from PIL import Image
import shutil

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib

from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize

from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import threading

#############################
#############################
## real ##
# Root directory of the project

ROOT_DIR = os.getcwd()
weight_name = "/home/js/Mask_RCNN/mask_rcnn_coco_0402.h5"
# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, weight_name)
# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

batch_size = 1

class InferenceConfig(Config):
    NAME = "man_woman"
    GPU_COUNT = 1
    IMAGES_PER_GPU = batch_size
    NUM_CLASSES = 3


config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

class_names = ['BG', 'woman', 'man']


class Ui_Form(object):





    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.setWindowState(Qt.WindowFullScreen)
        # Form.resize(1692, 800)
        Form.setStyleSheet('background-color: white')
        
        self.width = Form.width()
        self.height = Form.height()
        print("window_size: ", self.width, self.height)

        #####################################
        #####################################
        ## 전체 사이즈 설정 (full size - width: 1800 height: 1080)
        self.menu_height = 1080
        self.menu_width = 1800
        self.menu_bar = 160



        #############################
        #############################
        ## menu
        self.menu_widget = QtWidgets.QWidget(Form)
        self.menu_widget.setGeometry(QtCore.QRect(0, 0, self.menu_bar, 1080))
        self.menu_widget.setObjectName("menu_widget")
        self.menu_widget.setStyleSheet("background-color: #45775e")

        self.menu1_widget = QtWidgets.QWidget(self.menu_widget)
        self.menu1_widget.setGeometry(QtCore.QRect(0, 20, self.menu_bar, 80))
        self.menu1_widget.setObjectName("menu1_widget")

        self.menu_btn = QtWidgets.QPushButton(self.menu1_widget)
        self.menu_btn.setGeometry(QtCore.QRect(40, 20, 75, 80))
        self.menu_btn.setStyleSheet('QPushButton {border-style: double; color: white; font-size: 35px; font-weight:bold}')
        self.menu_btn.setObjectName("menu_btn")
        self.menu_btn.setCheckable(True)
        self.menu_btn.toggle()
        self.menu_btn.clicked.connect(self.menu_btn_clicked)

        self.menu2_widget = QtWidgets.QWidget(self.menu_widget)
        self.menu2_widget.setGeometry(QtCore.QRect(0, 110, self.menu_bar, 611))
        self.menu2_widget.setObjectName("menu2_widget")
        self.menu2_widget.setVisible(False)

        self.menu_list_VLayout = QtWidgets.QWidget(self.menu2_widget)
        self.menu_list_VLayout.setGeometry(QtCore.QRect(0, 10, self.menu_bar, 181))
        self.menu_list_VLayout.setObjectName("menu_list_VLayout")
        self.menu_list = QtWidgets.QVBoxLayout(self.menu_list_VLayout)
        self.menu_list.setContentsMargins(0, 0, 0, 0)
        self.menu_list.setObjectName("menu_list")

        self.menu_Btn_1 = QtWidgets.QPushButton(self.menu_list_VLayout)
        self.menu_Btn_1.setObjectName("menu_Btn_1")
        self.menu_list.addWidget(self.menu_Btn_1)
        self.menu_Btn_1.clicked.connect(self.menu_Btn_1_clicked)
        self.menu_Btn_1.setStyleSheet('QPushButton {border-style: double; color: white; font-size: 27px; font-weight:bold}')

        self.menu_Btn_2 = QtWidgets.QPushButton(self.menu_list_VLayout)
        self.menu_Btn_2.setObjectName("menu_Btn_2")
        self.menu_list.addWidget(self.menu_Btn_2)
        self.menu_Btn_2.clicked.connect(self.menu_Btn_2_clicked)
        self.menu_Btn_2.setStyleSheet('QPushButton {border-style: double; color: white; font-size: 27px; font-weight:bold}')

        self.menu_Btn_3 = QtWidgets.QPushButton(self.menu_list_VLayout)
        self.menu_Btn_3.setObjectName("menu_Btn_3")
        self.menu_list.addWidget(self.menu_Btn_3)
        self.menu_Btn_3.clicked.connect(self.menu_Btn_3_clicked)
        self.menu_Btn_3.setStyleSheet('QPushButton {border-style: double; color: white; font-size: 27px; font-weight:bold}')

        self.line = QtWidgets.QFrame(self.menu_widget)
        self.line.setGeometry(QtCore.QRect(self.menu_bar, 0, 11, 700))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")







        #####################################
        #####################################
        ## 오른쪽 화면
        ## main_menu
        self.main_widget = QtWidgets.QWidget(Form)
        self.main_widget.setGeometry(QtCore.QRect(self.menu_bar, 10, self.menu_width, 1080))
        self.main_widget.setObjectName("main_widget")

        self.main_lay = QtWidgets.QGridLayout(self.main_widget)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.setObjectName("main_lay")

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setObjectName("main_layout")

        self.main_main_widget = QtWidgets.QWidget(self.main_widget)
        self.main_main_widget.setObjectName("main_main_widget")
        self.main_main_widget.setGeometry(QtCore.QRect(1250, 100, 500, 600))

        self.image_widget_left = QtWidgets.QWidget(self.main_main_widget)
        self.image_widget_left.setGeometry(QtCore.QRect(50, 80, 900, 400))
        self.image_widget_left.setObjectName("image_widget_left")

        self.mainLeft_img_label = QtWidgets.QLabel(self.image_widget_left)
        self.mainLeft_img_label.setGeometry(QtCore.QRect(0, 0, 900, 400))
        self.mainLeft_img_label.setObjectName("mainLeft_img_label")
        self.mainLeft_img_label.setScaledContents(True)

        self.mainlabel = QtWidgets.QLabel(self.main_main_widget)
        self.mainlabel.setGeometry(QtCore.QRect(90, 500, 900, 50))
        self.mainlabel.setObjectName("mainlabel")
        self.mainlabel.setStyleSheet('QLabel {font-size:45px; font-weight:bold; font-color: rgb(69,119,94) }')
        
        # self.image_widget_right = QtWidgets.QWidget(self.main_main_widget)
        # self.image_widget_right.setGeometry(QtCore.QRect(700, 100, 851, 691))
        # self.image_widget_right.setObjectName("image_widget_right")
        # self.image_widget_right.setStyleSheet("background-color: #cfdcd3")

        self.mainRight_img_label = QtWidgets.QLabel(self.main_main_widget)
        self.mainRight_img_label.setGeometry(QtCore.QRect(965, 200, 800, 800))
        self.mainRight_img_label.setObjectName("mainRight_img_label")
        self.mainRight_img_label.setScaledContents(True)

        self.main_layout.addWidget(self.main_main_widget, 0, 1, 1, 1)
        self.main_lay.addLayout(self.main_layout, 0, 0, 1, 1)

        #
        image = QtGui.QImage('./img/mainLeft_img.jpg')
        image = image.scaled(self.mainLeft_img_label.size())
        self.mainLeft_img_label.setPixmap(QtGui.QPixmap.fromImage(image))

        image = QtGui.QImage('./img/mainRight_img.jpg')
        image = image.scaled(self.mainRight_img_label.size())
        self.mainRight_img_label.setPixmap(QtGui.QPixmap.fromImage(image))


        ###########################
        ###########################
        ## menu_1
        self.main_menu1_widget = QtWidgets.QWidget(Form)
        self.main_menu1_widget.setGeometry(QtCore.QRect(self.menu_bar, 10, self.menu_width, 1000))
        self.main_menu1_widget.setObjectName("main_menu1_widget")
        # self.main_menu1_widget.setStyleSheet("background-color: #e0e3e1")

        self.main_lay_1 = QtWidgets.QGridLayout(self.main_menu1_widget)
        self.main_lay_1.setContentsMargins(0, 0, 0, 0)
        self.main_lay_1.setObjectName("main_lay_1")

        self.real_lay = QtWidgets.QGridLayout()
        self.real_lay.setObjectName("real_lay")

        self.real_widget = QtWidgets.QWidget(self.main_menu1_widget)
        self.real_widget.setObjectName("real_widget")

        self.subject_label_1 = QtWidgets.QLabel(self.real_widget)
        self.subject_label_1.setGeometry(QtCore.QRect(20, 20, 701, 50))
        self.subject_label_1.setObjectName("subject_label_1")
        self.subject_label_1.setStyleSheet("font-size: 45px; font-weight:bold")

        self.realBtn_total_widget = QtWidgets.QWidget(self.real_widget)
        self.realBtn_total_widget.setGeometry(QtCore.QRect(30, 120, 450, 120))
        self.realBtn_total_widget.setObjectName("horizontalLayoutWidget")

        self.realBtn_HLayout = QtWidgets.QHBoxLayout(self.realBtn_total_widget)
        self.realBtn_HLayout.setContentsMargins(0, 0, 0, 0)
        self.realBtn_HLayout.setObjectName("realBtn_HLayout")

        self.dirBtn_label = QtWidgets. QLabel("No File", self.realBtn_total_widget)
        self.dirBtn_label.setGeometry(QtCore.QRect(2, 90, 450, 30))
        self.dirBtn_label.setObjectName("dirBtn_label")
        self.dirBtn_label.setStyleSheet("color: red; font-size: 30px")

        self.dirBtn = QtWidgets.QPushButton(self.realBtn_total_widget)
        self.dirBtn.setObjectName("dirBtn")
        self.dirBtn.clicked.connect(self.dirBtn_clicked)
        self.realBtn_HLayout.addWidget(self.dirBtn)
        self.dirBtn.setIcon(QtGui.QIcon('./img/folder_img.jpg'))
        self.dirBtn.setIconSize(QtCore.QSize(70,70))
        self.dirBtn.setStyleSheet('QPushButton {border-style: double; font-size: 30px; font-weight:bold}')

        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.realBtn_HLayout.addItem(spacerItem)

        self.real_playBtn = QtWidgets.QPushButton(self.realBtn_total_widget)
        self.real_playBtn.setObjectName("real_playBtn")
        self.real_playBtn.clicked.connect(self.real_play_btn_clicked)
        self.realBtn_HLayout.addWidget(self.real_playBtn)
        self.real_playBtn.setIcon(QtGui.QIcon('./img/play_img.jpg'))
        self.real_playBtn.setIconSize(QtCore.QSize(70,70))
        self.real_playBtn.setStyleSheet('QPushButton {border-style: double; font-size: 30px; font-weight:bold}')

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.realBtn_HLayout.addItem(spacerItem)

        self.real_stopBtn = QtWidgets.QPushButton(self.realBtn_total_widget)
        self.real_stopBtn.setObjectName("real_stopBtn")
        self.real_stopBtn.clicked.connect(self.real_stop_btn_clicked)
        self.realBtn_HLayout.addWidget(self.real_stopBtn)
        self.real_stopBtn.setIcon(QtGui.QIcon('./img/stop_img.jpg'))
        self.real_stopBtn.setIconSize(QtCore.QSize(70,70))
        self.real_stopBtn.setStyleSheet('QPushButton {border-style: double; font-size: 30px; font-weight:bold}')

        self.realShow_total_widget = QtWidgets.QWidget(self.real_widget)
        self.realShow_total_widget.setGeometry(QtCore.QRect(10, 300, self.menu_width - 55, 700))
        self.realShow_total_widget.setObjectName("realShow_total_widget")

        self.realShow_HLayout = QtWidgets.QHBoxLayout(self.realShow_total_widget)
        self.realShow_HLayout.setContentsMargins(0, 0, 0, 0)
        self.realShow_HLayout.setObjectName("realShow_HLayout")

        self.realShow1_widget = QtWidgets.QLabel(self.realShow_total_widget)
        self.realShow1_widget.setObjectName("realShow1_widget")
        self.realShow1_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.realShow1_widget.setScaledContents(True)
        # self.realShow1_widget.setStyleSheet("border: 1px solid gray")
        self.realShow1_widget.setStyleSheet("background-color: #cfdcd3")
        self.realShow_HLayout.addWidget(self.realShow1_widget,2)

        self.realShow2_widget = QtWidgets.QScrollArea(self.realShow_total_widget)
        self.realShow2_widget.setObjectName("realShow2_widget")
        self.content_1_widget = QtWidgets.QLabel(self.realShow_total_widget)
        self.realShow2_widget.setWidget(self.content_1_widget)
        self.realShow2_widget.setWidgetResizable(True)
        self.realShow2_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.realShow2_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.realShow_HLayout.addWidget(self.realShow2_widget,1)

        self.realShow3_widget = QtWidgets.QScrollArea(self.realShow_total_widget)
        self.realShow3_widget.setObjectName("realShow3_widget")
        self.content_2_widget = QtWidgets.QLabel(self.realShow_total_widget)
        self.realShow3_widget.setWidget(self.content_2_widget)
        self.realShow3_widget.setWidgetResizable(True)
        self.realShow3_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.realShow3_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.realShow_HLayout.addWidget(self.realShow3_widget,1)

        self.info_label_1 = QtWidgets.QLabel(self.real_widget)
        self.info_label_1.setGeometry(QtCore.QRect(1050, 240, 341, 40))
        self.info_label_1.setObjectName("info_label_1")
        self.info_label_1.setStyleSheet("font-size: 30px; font-weight: bold")
        

        self.info_label_2 = QtWidgets.QLabel(self.real_widget)
        self.info_label_2.setGeometry(QtCore.QRect(1470, 240, 341, 40))
        self.info_label_2.setObjectName("info_label_2")
        self.info_label_2.setStyleSheet("font-size: 30px; font-weight: bold")
        
        self.real_lay.addWidget(self.real_widget, 0, 1, 1, 1)
        self.main_lay_1.addLayout(self.real_lay, 0, 0, 1, 1)

        ###############
        ## menu1 변수
        self.file_name = None
        self.frame_num = 0
        self.dir_cnt = 0
        self.scroll_w = 0
        self.scroll_m = 0
        self.realBtn_bool = True


        ######################
        ######################
        ## menu_2
        self.main_menu2_widget = QtWidgets.QWidget(Form)
        self.main_menu2_widget.setGeometry(QtCore.QRect(self.menu_bar, 10, self.menu_width - 20, 1000))
        self.main_menu2_widget.setObjectName("main_menu2_widget")

        self.main_lay_2 = QtWidgets.QGridLayout(self.main_menu2_widget)
        self.main_lay_2.setContentsMargins(0, 0, 0, 0)
        self.main_lay_2.setObjectName("main_lay_2")

        self.vid_lay = QtWidgets.QGridLayout()
        self.vid_lay.setObjectName("vid_lay")

        self.vid_widget = QtWidgets.QWidget(self.main_menu2_widget)
        self.vid_widget.setObjectName("vid_widget")

        self.videoWidget_widget = QtWidgets.QWidget(self.vid_widget)
        self.videoWidget_widget.setGeometry(QtCore.QRect(0, 300, self.menu_width, 700))
        self.videoWidget_widget.setObjectName("videoWidget_widget")

        self.videoWidget_total_widget = QtWidgets.QWidget(self.videoWidget_widget)
        self.videoWidget_total_widget.setGeometry(QtCore.QRect(10, 0, self.menu_width, 550))
        self.videoWidget_total_widget.setObjectName("videoWidget_total_widget")

        self.videoWidget_HLayout = QtWidgets.QHBoxLayout(self.videoWidget_total_widget)
        self.videoWidget_HLayout.setContentsMargins(0, 0, 0, 0)
        self.videoWidget_HLayout.setObjectName("videoWidget_HLayout")

        self.vWidget_1 = QtMultimediaWidgets.QVideoWidget(self.videoWidget_total_widget)
        self.vWidget_1.setObjectName("vWidget_1")
        self.vWidget_1.setStyleSheet("background-color: #cfdcd3")
        self.videoWidget_HLayout.addWidget(self.vWidget_1,1)

        self.vWidget_2 = QtMultimediaWidgets.QVideoWidget(self.videoWidget_total_widget)
        self.vWidget_2.setObjectName("vWidget_2")
        self.vWidget_2.setStyleSheet("background-color: #cfdcd3")
        self.videoWidget_HLayout.addWidget(self.vWidget_2,1)

        self.img_label = QtWidgets.QLabel(self.videoWidget_total_widget)
        self.img_label.setObjectName("img_label")
        self.img_label.setScaledContents(True)
        self.img_label.setStyleSheet("background-color: #cfdcd3")
        self.videoWidget_HLayout.addWidget(self.img_label,1)

        self.videoLabel_total_widget = QtWidgets.QWidget(self.videoWidget_widget)
        self.videoLabel_total_widget.setGeometry(QtCore.QRect(10, 600, self.menu_width, 41))
        self.videoLabel_total_widget.setObjectName("videoLabel_total_widget")

        self.videoLabel_HLayout = QtWidgets.QHBoxLayout(self.videoLabel_total_widget)
        self.videoLabel_HLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLabel_HLayout.setObjectName("videoLabel_HLayout")

        self.videoLabel_1 = QtWidgets.QLabel(self.videoLabel_total_widget)
        self.videoLabel_1.setObjectName("videoLabel_1")
        self.videoLabel_1.setStyleSheet("font-size: 30px; font-weight: bold")
        self.videoLabel_HLayout.addWidget(self.videoLabel_1,1)
        self.videoLabel_1.setAlignment(QtCore.Qt.AlignHCenter)

        self.videoLabel_2 = QtWidgets.QLabel(self.videoLabel_total_widget)
        self.videoLabel_2.setObjectName("videoLabel_2")
        self.videoLabel_2.setStyleSheet("font-size: 30px; font-weight: bold")
        self.videoLabel_HLayout.addWidget(self.videoLabel_2,1)
        self.videoLabel_2.setAlignment(QtCore.Qt.AlignHCenter)

        self.heatmapHLayout = QtWidgets.QHBoxLayout()
        self.heatmapHLayout.setObjectName("heatmapHLayout")
        self.videoLabel_HLayout.addLayout(self.heatmapHLayout,1)
        self.heatmapHLayout.addStretch(1)

        self.videoLabel_3 = QtWidgets.QLabel()
        self.videoLabel_3.setObjectName("videoLabel_3")
        self.videoLabel_3.setStyleSheet("font-size: 30px; font-weight: bold")
        self.heatmapHLayout.addWidget(self.videoLabel_3)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.heatmapHLayout.addItem(spacerItem)

        self.manBtn = QtWidgets.QRadioButton("man")
        self.manBtn.setStyleSheet("font-size: 25px; font-weight: bold")
        self.manBtn.setObjectName("manBtn")
        # self.manBtn.setChecked(True)
        self.manBtn.clicked.connect(lambda: self.sex_btn_clicked(self.manBtn))
        self.heatmapHLayout.addWidget(self.manBtn)

        self.womanBtn = QtWidgets.QRadioButton("woman")
        self.womanBtn.setStyleSheet("font-size: 25px; font-weight: bold")
        self.womanBtn.setObjectName("womanBtn")
        self.womanBtn.clicked.connect(lambda: self.sex_btn_clicked(self.womanBtn))
        self.heatmapHLayout.addWidget(self.womanBtn)

        self.heatmapHLayout.addStretch(1)

        self.videoBtn_total_widget = QtWidgets.QWidget(self.vid_widget)
        self.videoBtn_total_widget.setGeometry(QtCore.QRect(520, 140, 280, 80))
        self.videoBtn_total_widget.setObjectName("videoBtn_total_widget")

        self.videoBtn_HLayout = QtWidgets.QHBoxLayout(self.videoBtn_total_widget)
        self.videoBtn_HLayout.setContentsMargins(0, 0, 0, 0)
        self.videoBtn_HLayout.setObjectName("videoBtn_HLayout")

        self.playBtn = QtWidgets.QPushButton(self.videoBtn_total_widget)
        self.playBtn.setObjectName("playBtn")
        self.playBtn.clicked.connect(self.play_btn_clicked)
        self.videoBtn_HLayout.addWidget(self.playBtn)
        self.playBtn.setIcon(QtGui.QIcon('./img/play_img.jpg'))
        self.playBtn.setIconSize(QtCore.QSize(70,70))
        self.playBtn.setStyleSheet('QPushButton {border-style: double; font-size: 30px; font-weight:bold}')

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.videoBtn_HLayout.addItem(spacerItem)

        self.stopBtn = QtWidgets.QPushButton(self.videoBtn_total_widget)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.clicked.connect(self.stop_btn_clicked)
        self.videoBtn_HLayout.addWidget(self.stopBtn)
        self.stopBtn.setIcon(QtGui.QIcon('./img/stop_img.jpg'))
        self.stopBtn.setIconSize(QtCore.QSize(70,70))
        self.stopBtn.setStyleSheet('QPushButton {border-style: double; font-size: 30px; font-weight:bold}')

        self.videoMenu_total_widget = QtWidgets.QWidget(self.vid_widget)
        self.videoMenu_total_widget.setGeometry(QtCore.QRect(10, 120, 421, 120))
        self.videoMenu_total_widget.setObjectName("videoMenu_total_widget")

        self.videoMenu_HLayout = QtWidgets.QHBoxLayout(self.videoMenu_total_widget)
        self.videoMenu_HLayout.setContentsMargins(0, 0, 0, 0)
        self.videoMenu_HLayout.setObjectName("videoMenu_HLayout")

        self.videoMenu_VLayout = QtWidgets.QVBoxLayout()
        self.videoMenu_VLayout.setObjectName("videoMenu_VLayout")

        self.dateMenu_HLayout = QtWidgets.QHBoxLayout()
        self.dateMenu_HLayout.setObjectName("dateMenu_HLayout")

        self.dateLabel = QtWidgets.QLabel(self.videoMenu_total_widget)
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setStyleSheet("font-size: 30px; font-weight: bold")
        self.dateMenu_HLayout.addWidget(self.dateLabel)
        

        self.dateEdit = QtWidgets.QDateEdit(self.videoMenu_total_widget)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setMinimumSize(50,50)
        self.dateEdit.setStyleSheet("font-size: 20px; font-weight: bold")
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateMenu_HLayout.addWidget(self.dateEdit)

        self.videoMenu_VLayout.addLayout(self.dateMenu_HLayout)

        self.timeLabel_HLayout = QtWidgets.QHBoxLayout()
        self.timeLabel_HLayout.setObjectName("timeLabel_HLayout")
        self.timeLabel = QtWidgets.QLabel(self.videoMenu_total_widget)
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setStyleSheet("font-size: 30px; font-weight: bold")
        self.timeLabel_HLayout.addWidget(self.timeLabel)

        self.time_list_1 = QtWidgets.QComboBox(self.videoMenu_total_widget)
        self.time_list_1.setObjectName("time_list_1")
        self.time_list_1.setMinimumSize(50,50)
        self.time_list_1.setStyleSheet("font-size: 20px; font-weight: bold")
        self.timeLabel_HLayout.addWidget(self.time_list_1)

        # time_list_1 item
        self.time_list_1.addItem('AM')
        self.time_list_1.addItem('PM')

        self.time_list_2 = QtWidgets.QComboBox(self.videoMenu_total_widget)
        self.time_list_2.setObjectName("time_list_2")
        self.time_list_2.setMinimumSize(50,50)
        self.time_list_2.setStyleSheet("font-size: 20px; font-weight: bold")
        self.timeLabel_HLayout.addWidget(self.time_list_2)

        # time_list_2 item
        for i in range(12):
            if (i == 0):
                self.time_list_2.addItem(str("12 ~ ") + self.make_time_format(i + 1))
                continue
            self.time_list_2.addItem(self.make_time_format(i) + str(" ~ ") + self.make_time_format(i + 1))

        self.videoMenu_VLayout.addLayout(self.timeLabel_HLayout)
        self.videoMenu_HLayout.addLayout(self.videoMenu_VLayout)

        self.time_list_Btn = QtWidgets.QPushButton(self.videoMenu_total_widget)
        self.time_list_Btn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.time_list_Btn.setObjectName("time_list_Btn")
        # self.condiLabel_1HLayout = QtWidgets.QHBoxLayout(self.condiLabel_1_widget)
        self.time_list_Btn.clicked.connect(self.time_list_btn_clicked)
        self.videoMenu_HLayout.addWidget(self.time_list_Btn)
        self.time_list_Btn.setIcon(QtGui.QIcon('./img/go_img.jpg'))
        self.time_list_Btn.setIconSize(QtCore.QSize(70,70))
        self.time_list_Btn.setStyleSheet('QPushButton {border-style: double;}')

        self.subject_label_2 = QtWidgets.QLabel(self.vid_widget)
        self.subject_label_2.setGeometry(QtCore.QRect(20, 20, 701, 50))
        self.subject_label_2.setObjectName("subject_label_2")
        self.subject_label_2.setStyleSheet("font-size: 45px; font-weight:bold")

        self.videoSpeed_widget = QtWidgets.QWidget(self.vid_widget)
        self.videoSpeed_widget.setGeometry(QtCore.QRect(860, 80, 181, 91))
        self.videoSpeed_widget.setObjectName("videoSpeed_widget")

        self.videoSpeed_total_widget = QtWidgets.QWidget(self.videoSpeed_widget)
        self.videoSpeed_total_widget.setGeometry(QtCore.QRect(10, 10, 160, 80))
        self.videoSpeed_total_widget.setObjectName("videoSpeed_total_widget")

        self.videoSpeed_HLayout = QtWidgets.QHBoxLayout(self.videoSpeed_total_widget)
        self.videoSpeed_HLayout.setContentsMargins(0, 0, 0, 0)
        self.videoSpeed_HLayout.setObjectName("videoSpeed_HLayout")

        self.videoSpeed_VLayout = QtWidgets.QVBoxLayout()
        self.videoSpeed_VLayout.setObjectName("videoSpeed_VLayout")

        self.videoSpeed_HLayout.addLayout(self.videoSpeed_VLayout)

        self.videoSpeed_label = QtWidgets.QLabel(self.videoSpeed_total_widget)
        self.videoSpeed_label.setObjectName("videoSpeed_label")
        self.videoSpeed_HLayout.addWidget(self.videoSpeed_label)

        self.vid_lay.addWidget(self.vid_widget, 0, 1, 1, 1)
        self.main_lay_2.addLayout(self.vid_lay, 0, 0, 1, 1)

        ###############
        ## menu 2 변수
        # self.findRoot = "C:/Users/bit/Desktop/seulgi/"
        self.findRoot = "/home/js/Mask_RCNN/save/"
        self.findDate = ""
        self.findTime = ""

        self.player_1 = QtMultimedia.QMediaPlayer(self.videoWidget_total_widget)
        self.player_2 = QtMultimedia.QMediaPlayer(self.videoWidget_total_widget)
        self.player_boolean = True
        self.isPlaying = True

        #
        self.player_1.setVideoOutput(self.vWidget_1)
        self.player_2.setVideoOutput(self.vWidget_2)

        ###########################
        ###########################
        ## menu 3
        self.main_menu3_widget = QtWidgets.QWidget(Form)
        self.main_menu3_widget.setGeometry(QtCore.QRect(self.menu_bar, 10, self.menu_width, 1000))
        self.main_menu3_widget.setObjectName("main_menu3_widget")

        self.main_lay_3 = QtWidgets.QGridLayout(self.main_menu3_widget)
        self.main_lay_3.setContentsMargins(0, 0, 0, 0)
        self.main_lay_3.setObjectName("main_lay_3")

        self.func_lay = QtWidgets.QGridLayout()
        self.func_lay.setObjectName("func_lay")

        self.func_widget = QtWidgets.QWidget(self.main_menu3_widget)
        self.func_widget.setObjectName("func_widget")

        self.subject_label_3 = QtWidgets.QLabel(self.func_widget)
        self.subject_label_3.setGeometry(QtCore.QRect(20, 20, 701, 50))
        self.subject_label_3.setObjectName("subject_label_3")
        self.subject_label_3.setStyleSheet("font-size: 45px; font-weight:bold")

        self.condiShow_total_widget = QtWidgets.QWidget(self.func_widget)
        self.condiShow_total_widget.setGeometry(QtCore.QRect(10, 430, self.menu_width, 500))
        self.condiShow_total_widget.setObjectName("condiShow_total_widget")
        # self.condiShow_total_widget.setStyleSheet("background-color: #cfdcd3")

        self.condiShow_HLayout = QtWidgets.QHBoxLayout(self.condiShow_total_widget)
        self.condiShow_HLayout.setContentsMargins(0, 0, 0, 0)
        self.condiShow_HLayout.setObjectName("condiShow_HLayout")

        self.condiShow1_widget = QtWidgets.QLabel(self.condiShow_total_widget)
        self.condiShow1_widget.setObjectName("condiShow1_widget")
        self.condiShow1_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.condiShow1_widget.setScaledContents(True)
        self.condiShow1_widget.setStyleSheet("background-color: #cfdcd3")
        # self.condiShow1_widget.setStyleSheet("border: 1px solid black")
        self.condiShow_HLayout.addWidget(self.condiShow1_widget)
        self.sex = 1
        self.man_heatmap = None
        self.woman_heatmap = None
        self.d_list = []
        self.dir_list = []

        self.condiShow2_widget = QtWidgets.QWidget(self.condiShow_total_widget)
        self.condiShow2_widget.setObjectName("condiShow2_widget")
        self.condiShow2_widget.setStyleSheet("background-color: #cfdcd3")
        self.condiShow_HLayout.addWidget(self.condiShow2_widget)

        self.condiLabel_total_widget = QtWidgets.QWidget(self.func_widget)
        self.condiLabel_total_widget.setGeometry(QtCore.QRect(9, 950, self.menu_width, 40))
        self.condiLabel_total_widget.setObjectName("condiLabel_total_widget")

        # self.condiLabel_1_Widget = QtWidgets.QWidget(self.condiLabel_total_widget)
        self.condiLabel_HLayout = QtWidgets.QHBoxLayout(self.condiLabel_total_widget)
        self.condiLabel_HLayout.setContentsMargins(0, 0, 0, 0)
        self.condiLabel_HLayout.setObjectName("condiLabel_HLayout")
        # self.condiLabel_1HLayout = QtWidgets.QHBoxLayout(self.condiLabel_1_widget)
        self.condiLabel_1HLayout = QtWidgets.QHBoxLayout()
        self.condiLabel_1HLayout.setObjectName("condiLabel_1HLayout")

        self.condiLabel_1HLayout.addStretch(1)

        self.condiLabel_1 = QtWidgets.QLabel()
        self.condiLabel_1.setObjectName("condiLabel_1")
        self.condiLabel_1.setStyleSheet("font-size: 30px; font-weight:bold")
        self.condiLabel_1HLayout.addWidget(self.condiLabel_1)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.condiLabel_1HLayout.addItem(spacerItem)

        self.condi_1_Btn2 = QtWidgets.QRadioButton("man")
        self.condi_1_Btn2.setObjectName("condi_1_Btn2")
        self.condi_1_Btn2.setStyleSheet("font-size: 25px; font-weight:bold")
        self.condi_1_Btn2.clicked.connect(lambda: self.condi_1_Btn_clicked(self.condi_1_Btn2))
        self.condiLabel_1HLayout.addWidget(self.condi_1_Btn2)

        self.condi_1_Btn1 = QtWidgets.QRadioButton("woman")
        self.condi_1_Btn1.setObjectName("condi_1_Btn1")
        self.condi_1_Btn1.setStyleSheet("font-size: 25px; font-weight:bold")
        self.condi_1_Btn1.clicked.connect(lambda: self.condi_1_Btn_clicked(self.condi_1_Btn1))
        self.condiLabel_1HLayout.addWidget(self.condi_1_Btn1)

        self.condiLabel_1HLayout.addStretch(1)

        self.condiLabel_HLayout.addLayout(self.condiLabel_1HLayout,1)

        self.condiLabel_2 = QtWidgets.QLabel(self.condiLabel_total_widget)
        self.condiLabel_2.setObjectName("condiLabel_2")
        self.condiLabel_2.setStyleSheet("font-size: 30px; font-weight:bold")
        self.condiLabel_HLayout.addWidget(self.condiLabel_2,1)
        self.condiLabel_2.setAlignment(QtCore.Qt.AlignHCenter)

        self.condi_1_widget = QtWidgets.QWidget(self.func_widget)
        self.condi_1_widget.setGeometry(QtCore.QRect(10, 120, 331, 200))
        self.condi_1_widget.setObjectName("widget")

        self.condi_1_VLayout = QtWidgets.QVBoxLayout(self.condi_1_widget)
        self.condi_1_VLayout.setContentsMargins(0, 0, 0, 0)
        self.condi_1_VLayout.setObjectName("condi_1_VLayout")

        self.radioBtn_1 = QtWidgets.QRadioButton(self.condi_1_widget)
        self.radioBtn_1.setObjectName("radioBtn_1")
        self.radioBtn_1.setStyleSheet("font-size: 30px; font-weight: bold")
        self.condi_1_VLayout.addWidget(self.radioBtn_1)
        self.radioBtn_1.clicked.connect(self.radioBtn_1_clicked)

        self.radioBtn_2 = QtWidgets.QRadioButton(self.condi_1_widget)
        self.radioBtn_2.setObjectName("radioBtn_2")
        self.radioBtn_2.setStyleSheet("font-size: 30px; font-weight: bold")
        self.condi_1_VLayout.addWidget(self.radioBtn_2)
        self.radioBtn_2.clicked.connect(self.radioBtn_2_clicked)

        self.radioBtn_3 = QtWidgets.QRadioButton(self.condi_1_widget)
        self.radioBtn_3.setObjectName("radioBtn_3")
        self.radioBtn_3.setStyleSheet("font-size: 30px; font-weight: bold")
        self.condi_1_VLayout.addWidget(self.radioBtn_3)
        self.radioBtn_3.clicked.connect(self.radioBtn_3_clicked)

        self.condi_2_widget = QtWidgets.QWidget(self.func_widget)
        self.condi_2_widget.setGeometry(QtCore.QRect(360, 100, 680, 300))
        self.condi_2_widget.setObjectName("condi_2_widget")

        self.group3_widget = QtWidgets.QWidget(self.condi_2_widget)
        self.group3_widget.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.group3_widget.setObjectName("group3_widget")

        self.groupBox_3 = QtWidgets.QGroupBox(self.group3_widget)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.groupBox_3.setStyleSheet("font-size: 20px; font-weight: bold")
        self.groupBox_3.setObjectName("groupBox_3")

        self.group2_widget = QtWidgets.QWidget(self.condi_2_widget)
        self.group2_widget.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.group2_widget.setObjectName("group2_widget")

        self.groupBox_2 = QtWidgets.QGroupBox(self.group2_widget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.groupBox_2.setStyleSheet("font-size: 20px; font-weight: bold")
        self.groupBox_2.setObjectName("groupBox_2")

        self.group1_widget = QtWidgets.QWidget(self.condi_2_widget)
        self.group1_widget.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.group1_widget.setObjectName("group1_widget")

        self.groupBox_1 = QtWidgets.QGroupBox(self.group1_widget)
        self.groupBox_1.setGeometry(QtCore.QRect(0, 0, 680, 300))
        self.groupBox_1.setStyleSheet("font-size: 20px; font-weight: bold")
        self.groupBox_1.setObjectName("groupBox_1")

        self.group1_widget.setVisible(False)
        self.group2_widget.setVisible(False)
        self.group3_widget.setVisible(False)

        ####
        ## condiShow2 그래프
        self.condiShow2_graph1_widget = QtWidgets.QWidget(self.condiShow_total_widget)
        self.condiShow2_graph1_widget.setObjectName("condiShow2_graph1_widget")
        self.condiShow2_graph1_widget.setGeometry(QtCore.QRect(900, 0, 900, 500))

        self.condiShow2_graph2_widget = QtWidgets.QWidget(self.condiShow_total_widget)
        self.condiShow2_graph2_widget.setObjectName("condiShow2_graph2_widget")
        self.condiShow2_graph2_widget.setGeometry(QtCore.QRect(900, 0, 900, 500))

        self.condiShow2_graph3_widget = QtWidgets.QWidget(self.condiShow_total_widget)
        self.condiShow2_graph3_widget.setObjectName("condiShow2_graph3_widget")
        self.condiShow2_graph3_widget.setGeometry(QtCore.QRect(900, 0, 900, 500))

        ####
        ## group 별로 item 추가
        # 1
        self.group1_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)

        self.group1_HLayout_1 = QtWidgets.QHBoxLayout(self.condi_2_widget)
        self.group1_HLayout_2 = QtWidgets.QHBoxLayout(self.condi_2_widget)

        self.group1_time_group = QtWidgets.QGroupBox(self.condi_2_widget)
        self.group1_time_group.setObjectName("group1_time_group")

        self.group1_hour_group = QtWidgets.QGroupBox(self.condi_2_widget)
        self.group1_hour_group.setObjectName("group1_hour_group")

        self.group1_time_1 = QtWidgets.QRadioButton("AM", self.condi_2_widget)
        self.group1_time_1.setObjectName("group1_time_1")
        self.group1_time_1.setChecked(True)
        self.group1_time_1.clicked.connect(lambda: self.radioBtn_1_time_clicked(self.group1_time_1))

        self.group1_time_2 = QtWidgets.QRadioButton("PM", self.condi_2_widget)
        self.group1_time_2.setObjectName("group1_time_2")
        self.group1_time_2.clicked.connect(lambda: self.radioBtn_1_time_clicked(self.group1_time_2))

        self.group1_HLayout_1.addWidget(self.group1_time_1)
        self.group1_HLayout_1.addWidget(self.group1_time_2)

        self.group1_radioBtn_1 = QtWidgets.QRadioButton("12 ~ 01 시", self.condi_2_widget)
        self.group1_radioBtn_1.setObjectName("group1_radioBtn_1")
        self.group1_radioBtn_1.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_1))

        self.group1_radioBtn_2 = QtWidgets.QRadioButton("01 ~ 02 시", self.condi_2_widget)
        self.group1_radioBtn_2.setObjectName("group1_radioBtn_2")
        self.group1_radioBtn_2.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_2))

        self.group1_radioBtn_3 = QtWidgets.QRadioButton("02 ~ 03 시", self.condi_2_widget)
        self.group1_radioBtn_3.setObjectName("group1_radioBtn_3")
        self.group1_radioBtn_3.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_3))

        self.group1_radioBtn_4 = QtWidgets.QRadioButton("03 ~ 04 시", self.condi_2_widget)
        self.group1_radioBtn_4.setObjectName("group1_radioBtn_4")
        self.group1_radioBtn_4.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_4))

        self.group1_radioBtn_5 = QtWidgets.QRadioButton("04 ~ 05 시", self.condi_2_widget)
        self.group1_radioBtn_5.setObjectName("group1_radioBtn_5")
        self.group1_radioBtn_5.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_5))

        self.group1_radioBtn_6 = QtWidgets.QRadioButton("05 ~ 06 시", self.condi_2_widget)
        self.group1_radioBtn_6.setObjectName("group1_radioBtn_6")
        self.group1_radioBtn_6.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_6))

        self.group1_radioBtn_7 = QtWidgets.QRadioButton("06 ~ 07 시", self.condi_2_widget)
        self.group1_radioBtn_7.setObjectName("group1_radioBtn_7")
        self.group1_radioBtn_7.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_7))

        self.group1_radioBtn_8 = QtWidgets.QRadioButton("07 ~ 08 시", self.condi_2_widget)
        self.group1_radioBtn_8.setObjectName("group1_radioBtn_8")
        self.group1_radioBtn_8.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_8))

        self.group1_radioBtn_9 = QtWidgets.QRadioButton("08 ~ 09 시", self.condi_2_widget)
        self.group1_radioBtn_9.setObjectName("group1_radioBtn_9")
        self.group1_radioBtn_9.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_9))

        self.group1_radioBtn_10 = QtWidgets.QRadioButton("09 ~ 10 시", self.condi_2_widget)
        self.group1_radioBtn_10.setObjectName("group1_radioBtn_10")
        self.group1_radioBtn_10.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_10))

        self.group1_radioBtn_11 = QtWidgets.QRadioButton("10 ~ 11 시", self.condi_2_widget)
        self.group1_radioBtn_11.setObjectName("group1_radioBtn_11")
        self.group1_radioBtn_11.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_11))

        self.group1_radioBtn_12 = QtWidgets.QRadioButton("11 ~ 12 시", self.condi_2_widget)
        self.group1_radioBtn_12.setObjectName("group1_radioBtn_12")
        self.group1_radioBtn_12.clicked.connect(lambda: self.radioBtn_1_hour_clicked(self.group1_radioBtn_12))

        self.group1_1_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group1_1_VLayout.addWidget(self.group1_radioBtn_1)
        self.group1_1_VLayout.addWidget(self.group1_radioBtn_2)
        self.group1_1_VLayout.addWidget(self.group1_radioBtn_3)

        self.group1_2_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group1_2_VLayout.addWidget(self.group1_radioBtn_4)
        self.group1_2_VLayout.addWidget(self.group1_radioBtn_5)
        self.group1_2_VLayout.addWidget(self.group1_radioBtn_6)

        self.group1_3_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group1_3_VLayout.addWidget(self.group1_radioBtn_7)
        self.group1_3_VLayout.addWidget(self.group1_radioBtn_8)
        self.group1_3_VLayout.addWidget(self.group1_radioBtn_9)

        self.group1_4_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group1_4_VLayout.addWidget(self.group1_radioBtn_10)
        self.group1_4_VLayout.addWidget(self.group1_radioBtn_11)
        self.group1_4_VLayout.addWidget(self.group1_radioBtn_12)

        self.group1_HLayout_2.addLayout(self.group1_1_VLayout)
        self.group1_HLayout_2.addLayout(self.group1_2_VLayout)
        self.group1_HLayout_2.addLayout(self.group1_3_VLayout)
        self.group1_HLayout_2.addLayout(self.group1_4_VLayout)

        self.group1_time_group.setLayout(self.group1_HLayout_1)
        self.group1_hour_group.setLayout(self.group1_HLayout_2)
        self.group1_VLayout.addWidget(self.group1_time_group)
        self.group1_VLayout.addWidget(self.group1_hour_group)
        self.groupBox_1.setLayout(self.group1_VLayout)

        # 2
        self.group2_HLayout = QtWidgets.QHBoxLayout(self.condi_2_widget)

        self.group2_radioBtn_1 = QtWidgets.QRadioButton("Monday", self.condi_2_widget)
        self.group2_radioBtn_1.setObjectName("group2_radioBtn_1")
        self.group2_radioBtn_1.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_1))

        self.group2_radioBtn_2 = QtWidgets.QRadioButton("Tuesday", self.condi_2_widget)
        self.group2_radioBtn_2.setObjectName("group2_radioBtn_2")
        self.group2_radioBtn_2.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_2))

        self.group2_radioBtn_3 = QtWidgets.QRadioButton("Wednesday", self.condi_2_widget)
        self.group2_radioBtn_3.setObjectName("group2_radioBtn_3")
        self.group2_radioBtn_3.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_3))

        self.group2_radioBtn_4 = QtWidgets.QRadioButton("Thursday", self.condi_2_widget)
        self.group2_radioBtn_4.setObjectName("group2_radioBtn_4")
        self.group2_radioBtn_4.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_4))

        self.group2_radioBtn_5 = QtWidgets.QRadioButton("Friday", self.condi_2_widget)
        self.group2_radioBtn_5.setObjectName("group2_radioBtn_5")
        self.group2_radioBtn_5.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_5))

        self.group2_radioBtn_6 = QtWidgets.QRadioButton("Saturday", self.condi_2_widget)
        self.group2_radioBtn_6.setObjectName("group2_radioBtn_6")
        self.group2_radioBtn_6.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_6))

        self.group2_radioBtn_7 = QtWidgets.QRadioButton("Sunday", self.condi_2_widget)
        self.group2_radioBtn_7.setObjectName("group2_radioBtn_7")
        self.group2_radioBtn_7.clicked.connect(lambda: self.radioBtn_2_groupBox_clicked(self.group2_radioBtn_7))

        self.group2_1_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group2_1_VLayout.addWidget(self.group2_radioBtn_1)
        self.group2_1_VLayout.addWidget(self.group2_radioBtn_2)
        self.group2_1_VLayout.addWidget(self.group2_radioBtn_3)

        self.group2_2_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group2_2_VLayout.addWidget(self.group2_radioBtn_4)
        self.group2_2_VLayout.addWidget(self.group2_radioBtn_5)
        self.group2_2_VLayout.addWidget(self.group2_radioBtn_6)
        self.group2_2_VLayout.addWidget(self.group2_radioBtn_7)

        self.group2_HLayout.addLayout(self.group2_1_VLayout)
        self.group2_HLayout.addLayout(self.group2_2_VLayout)

        self.groupBox_2.setLayout(self.group2_HLayout)

        # 3
        self.group3_HLayout = QtWidgets.QHBoxLayout(self.condi_2_widget)

        self.group3_radioBtn_1 = QtWidgets.QRadioButton("1월", self.condi_2_widget)
        self.group3_radioBtn_1.setObjectName("group3_radioBtn_1")
        self.group3_radioBtn_1.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_1))

        self.group3_radioBtn_2 = QtWidgets.QRadioButton("2월", self.condi_2_widget)
        self.group3_radioBtn_2.setObjectName("group3_radioBtn_2")
        self.group3_radioBtn_2.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_2))

        self.group3_radioBtn_3 = QtWidgets.QRadioButton("3월", self.condi_2_widget)
        self.group3_radioBtn_3.setObjectName("group3_radioBtn_3")
        self.group3_radioBtn_3.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_3))

        self.group3_radioBtn_4 = QtWidgets.QRadioButton("4월", self.condi_2_widget)
        self.group3_radioBtn_4.setObjectName("group3_radioBtn_4")
        self.group3_radioBtn_4.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_4))

        self.group3_radioBtn_5 = QtWidgets.QRadioButton("5월", self.condi_2_widget)
        self.group3_radioBtn_5.setObjectName("group3_radioBtn_5")
        self.group3_radioBtn_5.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_5))

        self.group3_radioBtn_6 = QtWidgets.QRadioButton("6월", self.condi_2_widget)
        self.group3_radioBtn_6.setObjectName("group3_radioBtn_6")
        self.group3_radioBtn_6.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_6))

        self.group3_radioBtn_7 = QtWidgets.QRadioButton("7월", self.condi_2_widget)
        self.group3_radioBtn_7.setObjectName("group3_radioBtn_7")
        self.group3_radioBtn_7.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_7))

        self.group3_radioBtn_8 = QtWidgets.QRadioButton("8월", self.condi_2_widget)
        self.group3_radioBtn_8.setObjectName("group3_radioBtn_8")
        self.group3_radioBtn_8.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_8))

        self.group3_radioBtn_9 = QtWidgets.QRadioButton("9월", self.condi_2_widget)
        self.group3_radioBtn_9.setObjectName("group3_radioBtn_9")
        self.group3_radioBtn_9.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_9))

        self.group3_radioBtn_10 = QtWidgets.QRadioButton("10월", self.condi_2_widget)
        self.group3_radioBtn_10.setObjectName("group3_radioBtn_10")
        self.group3_radioBtn_10.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_10))

        self.group3_radioBtn_11 = QtWidgets.QRadioButton("11월", self.condi_2_widget)
        self.group3_radioBtn_11.setObjectName("group3_radioBtn_11")
        self.group3_radioBtn_11.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_11))

        self.group3_radioBtn_12 = QtWidgets.QRadioButton("12월", self.condi_2_widget)
        self.group3_radioBtn_12.setObjectName("group3_radioBtn_12")
        self.group3_radioBtn_12.clicked.connect(lambda: self.radioBtn_3_groupBox_clicked(self.group3_radioBtn_12))

        self.group3_1_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group3_1_VLayout.addWidget(self.group3_radioBtn_1)
        self.group3_1_VLayout.addWidget(self.group3_radioBtn_2)
        self.group3_1_VLayout.addWidget(self.group3_radioBtn_3)
        self.group3_1_VLayout.addWidget(self.group3_radioBtn_4)

        self.group3_2_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group3_2_VLayout.addWidget(self.group3_radioBtn_5)
        self.group3_2_VLayout.addWidget(self.group3_radioBtn_6)
        self.group3_2_VLayout.addWidget(self.group3_radioBtn_7)
        self.group3_2_VLayout.addWidget(self.group3_radioBtn_8)

        self.group3_3_VLayout = QtWidgets.QVBoxLayout(self.condi_2_widget)
        self.group3_3_VLayout.addWidget(self.group3_radioBtn_9)
        self.group3_3_VLayout.addWidget(self.group3_radioBtn_10)
        self.group3_3_VLayout.addWidget(self.group3_radioBtn_11)
        self.group3_3_VLayout.addWidget(self.group3_radioBtn_12)

        self.group3_HLayout.addLayout(self.group3_1_VLayout)
        self.group3_HLayout.addLayout(self.group3_2_VLayout)
        self.group3_HLayout.addLayout(self.group3_3_VLayout)

        self.groupBox_3.setLayout(self.group3_HLayout)

        #################
        ## menu3 변수
        self.group1_fileName = 0
        self.bool = 1
        self.value_list = []

        ###
        # 그래프 계산
        self.set_graph()

        #################
        #################
        ## 맨끝 원래 있는거
        self.func_lay.addWidget(self.func_widget, 0, 1, 1, 1)
        self.main_lay_3.addLayout(self.func_lay, 0, 0, 1, 1)

        # 메인 화면
        self.main_menu1_widget.setVisible(False)
        self.main_menu2_widget.setVisible(False)
        self.main_menu3_widget.setVisible(False)

        # ////// 원래 있는거
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    ###########################
    ###########################
    ## function

    # 메뉴 list 보였다가 안보였다가
    def menu_btn_clicked(self):
        if self.menu_btn.isChecked():
            self.menu2_widget.setVisible(False)
        else:
            self.menu2_widget.setVisible(True)

    # 메뉴1 click
    def menu_Btn_1_clicked(self):
        self.main_menu1_widget.setVisible(True)
        self.main_menu2_widget.setVisible(False)
        self.main_menu3_widget.setVisible(False)
        self.main_widget.setVisible(False)

    # 메뉴2 click
    def menu_Btn_2_clicked(self):
        self.main_menu1_widget.setVisible(False)
        self.main_menu2_widget.setVisible(True)
        self.main_menu3_widget.setVisible(False)
        self.main_widget.setVisible(False)

    # 메뉴3 click
    def menu_Btn_3_clicked(self):
        self.main_menu1_widget.setVisible(False)
        self.main_menu2_widget.setVisible(False)
        self.main_menu3_widget.setVisible(True)
        self.main_widget.setVisible(False)

    # radioBtn_1 click
    def radioBtn_1_clicked(self):
        self.condiShow2_widget.setStyleSheet("background-color:white")
        self.group1_widget.setVisible(True)
        self.group2_widget.setVisible(False)
        self.group3_widget.setVisible(False)

        for item in self.group1_time_group.findChildren(QtWidgets.QRadioButton):
            if item.isChecked():
                item.setAutoExclusive(False)
                item.setChecked(False)
                item.setAutoExclusive(True)
                self.group1_time_1.setChecked(True)
                break

        for item in self.group1_hour_group.findChildren(QtWidgets.QRadioButton):
            if item.isChecked():
                item.setAutoExclusive(False)
                item.setChecked(False)
                item.setAutoExclusive(True)
                break

        self.condiShow2_graph1_widget.setVisible(True)
        self.condiShow2_graph2_widget.setVisible(False)
        self.condiShow2_graph3_widget.setVisible(False)

    # radioBtn_2 click
    def radioBtn_2_clicked(self):
        self.condiShow2_widget.setStyleSheet("background-color:white")
        self.group1_widget.setVisible(False)
        self.group2_widget.setVisible(True)
        self.group3_widget.setVisible(False)

        for item in self.groupBox_2.findChildren(QtWidgets.QRadioButton):
            if item.isChecked():
                item.setAutoExclusive(False)
                item.setChecked(False)
                item.setAutoExclusive(True)
                break

        self.condiShow2_graph1_widget.setVisible(False)
        self.condiShow2_graph2_widget.setVisible(True)
        self.condiShow2_graph3_widget.setVisible(False)

    # radioBtn_3 click
    def radioBtn_3_clicked(self):
        self.condiShow2_widget.setStyleSheet("background-color:white")
        self.group1_widget.setVisible(False)
        self.group2_widget.setVisible(False)
        self.group3_widget.setVisible(True)

        for item in self.groupBox_3.findChildren(QtWidgets.QRadioButton):
            if item.isChecked():
                item.setAutoExclusive(False)
                item.setChecked(False)
                item.setAutoExclusive(True)
                break

        self.condiShow2_graph1_widget.setVisible(False)
        self.condiShow2_graph2_widget.setVisible(False)
        self.condiShow2_graph3_widget.setVisible(True)

    def set_graph(self):
        self.make_valueList(24)
        self.radioBtn_1_clicked_calculate()
        self.make_barGraph()

        self.make_valueList(7)
        self.radioBtn_2_clicked_calculate()
        self.make_barGraph()

        self.make_valueList(12)
        self.radioBtn_3_clicked_calculate()
        self.make_barGraph()

        self.condiShow2_graph1_widget.setVisible(False)
        self.condiShow2_graph2_widget.setVisible(False)
        self.condiShow2_graph3_widget.setVisible(False)
        # self.condiShow2_graph3_widget.setStyleSheet("background-color: #e1e1df")

    ###############
    ###############
    ## heatmap 만들고 저장하기
    def save_heatmap(self, d_dir):
        man_coord_list = np.loadtxt(d_dir + "man.txt", delimiter=" ")

        if(len(man_coord_list)>0 and type(man_coord_list[0]) == np.float64):
            man_coord_list = [man_coord_list]
            man_coord_list = np.array(man_coord_list)

        woman_coord_list = np.loadtxt(d_dir + "woman.txt", delimiter=" ")

        if(len(woman_coord_list)>0 and type(woman_coord_list[0]) == np.float64):
            woman_coord_list = [woman_coord_list]
            woman_coord_list = np.array(woman_coord_list)

        ori_img_path = d_dir + "img.jpg"
        ori_img = Image.open(ori_img_path)

        heatmapper = Heatmapper()
        heatmapper2 = Heatmapper()
        man_heatmap = heatmapper.heatmap_on_img(man_coord_list, ori_img)
        woman_heatmap = heatmapper2.heatmap_on_img(woman_coord_list, ori_img)
        # RGBA as JPEG
        man_heatmap = man_heatmap.convert("RGB")
        woman_heatmap = woman_heatmap.convert("RGB")

        man_heatmap.save(d_dir + 'man_heatmap.jpg')
        woman_heatmap.save(d_dir + 'woman_heatmap.jpg')

    # heatmap 보여주기
    # 월, 요일
    def print_heatmap(self, dir_list):
        man_coord_list = []
        woman_coord_list = []
        qim = None
        qim2 = None

        for d_dir in dir_list:
            d_dir = self.findRoot + d_dir + "/"
            hourdir_list = os.listdir(d_dir)

            for hourdir in hourdir_list:
                hourdir = d_dir + hourdir + "/"
                man_load = np.loadtxt(hourdir + "man.txt", delimiter=" ")
                if(len(man_load)>0 and type(man_load[0]) == np.float64):
                    man_load = [man_load]
                    man_load = np.array(man_load)
                man_coord_list.extend(man_load)

                woman_load = np.loadtxt(hourdir + "woman.txt", delimiter=" ")
                if(len(woman_load)>0 and type(woman_load[0]) == np.float64):
                    woman_load = [woman_load]
                    woman_load = np.array(woman_load)
                woman_coord_list.extend(woman_load)
        # woman_coord_list.extend(np.loadtxt(self.findRoot + d_dir + "/" + "woman.txt", delimiter=" "))
        ori_dir_path = dir_list[0] + "/"
        ori_dir_name = ori_dir_path + os.listdir(self.findRoot + ori_dir_path)[0] + "/"
        ori_img_path = self.findRoot + ori_dir_name + "img.jpg"
        ori_img = Image.open(ori_img_path)

        heatmapper = Heatmapper()
        heatmapper2 = Heatmapper()
        man_heatmap = heatmapper.heatmap_on_img(man_coord_list, ori_img)
        woman_heatmap = heatmapper2.heatmap_on_img(woman_coord_list, ori_img)
        r1, g1, b1, a1 = man_heatmap.split()
        r2, g2, b2, a2 = woman_heatmap.split()
        img = Image.merge("RGBA", (b1, g1, r1, a1))
        img2 = Image.merge("RGBA", (b2, g2, r2, a2))
        data = img.tobytes("raw", "RGBA")
        data2 = img2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
        qim2 = QtGui.QImage(data2, img2.size[0], img2.size[1], QtGui.QImage.Format_ARGB32)
        print("heatmap_print1 complete")
        return qim, qim2

    # heatmap 보여주기
    # 시간
    def print_heatmap_2(self, dir_list):
        man_coord_list = []
        woman_coord_list = []
        ori_img = None
        qim = None
        qim2 = None
        for d_dir in dir_list:
            d_dir = self.findRoot + d_dir + "/" + self.group1_fileName + "/"
            if os.path.exists(d_dir):
                man_coord_list.extend(np.loadtxt(d_dir + "man.txt", delimiter=" "))
                woman_coord_list.extend(np.loadtxt(d_dir + "woman.txt", delimiter=" "))
                if ori_img is None:
                    ori_img_path = d_dir + "img.jpg"
                    ori_img = Image.open(ori_img_path)
            else:
                print("dir doesn't exists: " + d_dir)

        if ori_img is not None:
            heatmapper = Heatmapper()
            heatmapper2 = Heatmapper()
            man_heatmap = heatmapper.heatmap_on_img(man_coord_list, ori_img)
            woman_heatmap = heatmapper2.heatmap_on_img(woman_coord_list, ori_img)
            r1, g1, b1, a1 = man_heatmap.split()
            r2, g2, b2, a2 = woman_heatmap.split()
            img = Image.merge("RGBA", (b1, g1, r1, a1))
            img2 = Image.merge("RGBA", (b2, g2, r2, a2))
            data = img.tobytes("raw", "RGBA")
            data2 = img2.tobytes("raw", "RGBA")
            qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
            qim2 = QtGui.QImage(data2, img2.size[0], img2.size[1], QtGui.QImage.Format_ARGB32)
            print("heatmap_print complete")
        return qim, qim2

    def condi_1_Btn_clicked(self, button):
        if button.text() == "man":
            self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))
        else:
            self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.woman_heatmap))

    def real_play_btn_clicked(self):
        self.realBtn_bool = True
        self.exec_content()
    
    def real_stop_btn_clicked(self):
        self.realBtn_bool = False


    ## menu3  시간마다 함수
    # radioBtn_1 click & groupBox hour click
    def radioBtn_1_hour_clicked(self, button):
        self.group1_fileName = int(button.text()[:2])
        self.radioBtn_1_groupBox_check()
        self.condi_1_Btn2.setChecked(True)
        if len(self.dir_list):
            self.man_heatmap, self.woman_heatmap = self.print_heatmap_2(self.dir_list)
        else:
            self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))

    # radioBtn_1 click & groupBox time click
    def radioBtn_1_time_clicked(self, button):
        if (button.text() == "AM"):
            self.bool = 1
        else:
            self.bool = 2
        self.radioBtn_1_groupBox_check()

    def radioBtn_1_groupBox_check(self):
        if (self.group1_fileName != 0 and self.bool != 0):
            # 시간 폴더명 찾기
            if (self.group1_fileName == 12):
                self.group1_fileName = 0
            if (self.bool == 1):
                if (self.group1_fileName >= 12):
                    self.group1_fileName = self.group1_fileName - 12
            elif (self.bool == 2):
                self.group1_fileName = self.group1_fileName + 12
            self.group1_fileName = self.make_time_format(self.group1_fileName)

    # year와 month로 시작하는 폴더 찾기
    def radioBtn_1_clicked_calculate(self):
        self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))
        self.dir_list = self.find_fileList()

        for dir_name in self.dir_list:
            file_list = os.listdir(self.findRoot + dir_name)
            for file_name in file_list:
                path = self.findRoot + dir_name + "/" + file_name
                man_path = path + "/man.txt"
                woman_path = path + "/woman.txt"
                if (os.path.exists(man_path)):
                    self.value_list[int(file_name)][0] += 1
                    f_m = open(man_path, "r")
                    while True:
                        line = f_m.readline()
                        if not line: break
                        self.value_list[int(file_name)][2] += 1

                if (os.path.exists(woman_path)):
                    self.value_list[int(file_name)][1] += 1
                    f_w = open(woman_path, "r")
                    while True:
                        line = f_w.readline()
                        if not line: break
                        self.value_list[int(file_name)][3] += 1
                f_m.close()
                f_w.close()

    ###############
    ###############
    ## menu3 요일 마다 함수
    #
    def radioBtn_2_groupBox_clicked(self, button):
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        want_day = button.text()[:3]
        want_dir = [d_dir for d_dir in self.dir_list if d_dir[-3:] == want_day]
        self.condi_1_Btn2.setChecked(True)
        if len(want_dir):
            self.man_heatmap, self.woman_heatmap = self.print_heatmap(want_dir)
        else:
            self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))

    def radioBtn_2_clicked_calculate(self):
        self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        self.dir_list = self.find_fileList()
        for dir_name in self.dir_list:
            index = [i for i, v in enumerate(week) if v == dir_name[-3:]]
            file_list = os.listdir(self.findRoot + dir_name)
            for file_name in file_list:
                path = self.findRoot + dir_name + "/" + file_name
                if (os.path.exists(path + "/man.txt")):
                    self.value_list[index[0]][0] += 1
                    f_m = open(path + "/man.txt", "r")
                    while True:
                        line = f_m.readline()
                        if not line: break
                        self.value_list[index[0]][2] += 1

                if (os.path.exists(path + "/woman.txt")):
                    self.value_list[index[0]][1] += 1
                    f_w = open(path + "/woman.txt", "r")
                    while True:
                        line = f_w.readline()
                        if not line: break
                        self.value_list[index[0]][3] += 1
                    f_m.close()
                    f_w.close()

    ###############
    ###############
    ## menu3 월 마다 함수
    #
    def radioBtn_3_groupBox_clicked(self, button):
        want_month = self.make_time_format(int(button.text()[:-1]))
        want_dir = [d_dir for d_dir in self.d_list if d_dir[4:6] == want_month]
        self.condi_1_Btn2.setChecked(True)
        if len(want_dir):
            self.man_heatmap, self.woman_heatmap = self.print_heatmap(want_dir)
        else:
            self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))

    def radioBtn_3_clicked_calculate(self):
        self.man_heatmap, self.woman_heatmap = None, None
        self.condiShow1_widget.setPixmap(QPixmap.fromImage(self.man_heatmap))
        year = datetime.now().year - 1
        month = datetime.now().month

        day = []
        for i in range(12):
            if (month > 12):
                month = 1
                year += 1
            day.append(str(year) + self.make_time_format(month))
            month += 1

        dir_list = os.listdir(self.findRoot)
        dir_list.sort()
        print("전체 dir 리스트 :", dir_list)
        self.d_list = []
        for d in day:
            self.d_list.extend([file for file in dir_list if file.startswith(d)])

        print("해당 dir 리스트 :", self.d_list)

        for dir_name in self.d_list:
            index = int(dir_name[4:6])
            file_list = os.listdir(self.findRoot + dir_name)
            for file_name in file_list:
                path = self.findRoot + dir_name + "/" + file_name
                if (os.path.exists(path + "/man.txt")):
                    self.value_list[index - 1][0] += 1
                    f_m = open(path + "/man.txt", "r")
                    while True:
                        line = f_m.readline()
                        if not line: break
                        self.value_list[index - 1][2] += 1

                if (os.path.exists(path + "/woman.txt")):
                    self.value_list[index - 1][1] += 1
                    f_w = open(path + "/woman.txt", "r")
                    while True:
                        line = f_w.readline()
                        if not line: break
                        self.value_list[index - 1][3] += 1
                    f_m.close()
                    f_w.close()

    # 해당 날짜가 무슨 요일인지 찾기
    def find_weekday(self):
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def make_barGraph(self):
        value_m = []
        value_w = []

        figure = Figure()
        canvas = FigureCanvas(figure)
        canvas.setStyleSheet('background-color : white')

        can1_vLayout = QtWidgets.QVBoxLayout()
        can1_vLayout.addWidget(canvas)

        ax = canvas.figure.add_subplot(111)

        for index in range(len(self.value_list)):
            v = []
            if (self.value_list[index][0] == 0):
                value_m.append(0)
            else:
                value_m.append(self.value_list[index][2] / self.value_list[index][0])
            if (self.value_list[index][1] == 0):
                value_w.append(0)
            else:
                value_w.append(self.value_list[index][3] / self.value_list[index][1])

        wid = 0.4
        if (len(self.value_list) == 24):
            label_y = "hour"
            label_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            self.condiShow2_graph1_widget.setLayout(can1_vLayout)
        elif (len(self.value_list) == 7):
            label_y = "week"
            label_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            self.condiShow2_graph2_widget.setLayout(can1_vLayout)
        else:
            label_y = "month"
            label_list = ["Jan", 'Feb', 'Mar', 'Apr', "May", 'Jun', "Jul", 'Aug', "Sep", 'Oct', "Nov", "Dec"]
            self.condiShow2_graph3_widget.setLayout(can1_vLayout)

        x = np.arange(len(label_list))

        bar_m = ax.bar(x - wid / 2, value_m, wid, label='Men')
        bar_w = ax.bar(x + wid / 2, value_w, wid, label='Women')

        ax.set_xticks(x)
        ax.set_xticklabels(label_list)
        ax.legend()

        # 막대그래프에서 막대 값 적어주기
        # def autolabel(rects):
        #     """Attach a text label above each bar in *rects*, displaying its height."""
        #     for rect in rects:
        #         height = rect.get_height()
        #         self.ax.annotate('{}'.format(height),
        #                          xy=(rect.get_x() + rect.get_width() / 2, height),
        #                          xytext=(0, 1.5),  # 3 points vertical offset,
        #                          size=6,
        #                          textcoords="offset points",
        #                          ha='center', va='bottom')

        # autolabel(bar_m)
        # autolabel(bar_w)

        canvas.draw()  # update graph

    # 폴더에서 해당 파일 찾기
    def find_fileList(self):
        year = datetime.now().year
        month = datetime.now().month
        if (month == 1):
            year -= 1
            month = 12
        else:
            month -= 1
        dirName = self.make_time_format(year) + self.make_time_format(month)

        dir_list = os.listdir(self.findRoot)
        dir_list.sort()
        print("전체 dir 리스트 :", dir_list)
        dir_list = [file for file in dir_list if file.startswith(dirName)]
        print("해당 dir 리스트 :", dir_list)

        return dir_list

    # value_list 초기화
    def make_valueList(self, cnt):
        self.value_list = []
        for i in range(cnt):
            self.value_list.append([0, 0, 0, 0])

    # 폴더명 찾기
    def time_list_btn_clicked(self):
        # findDate
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        date = self.dateEdit.date()
        year, month, day = QDate.getDate(date)
        bday = week[date.dayOfWeek() - 1]
        self.findDate = str(year) + self.make_time_format(month) + self.make_time_format(day) + '_' + bday

        # findTime
        time_1 = self.time_list_1.currentText()
        time_2 = self.time_list_2.currentText()
        time = int(time_2.split(' ')[0])
        if (time_1 == 'PM'):
            time += 12
        if (time == 12):
            time = 0
        if (time == 24):
            time = 12
        self.findTime = self.make_time_format(time)
        self.file_name_go_btn_clicked()
        self.manBtn.setChecked(True)
    # 숫자를 2자리 형태로 ( 1 ==> 01 )
    def make_time_format(self, time):
        if (time < 10):
            time = '0' + str(time)
            return time
        time = str(time)
        return time

    # GO 버튼 실행
    def file_name_go_btn_clicked(self):
        path = self.findRoot + self.findDate + "/" + self.findTime + "/"
        path_ori = path + "ori" + self.file_ext(1, path)
        path_bbox = path + "bbox" + self.file_ext(2, path)
        path_img = path + "man_heatmap" + self.file_ext(3, path)

        self.player_1.setMedia(QUrl.fromLocalFile(path_ori))
        self.player_1.setVideoOutput(self.vWidget_1)

        self.player_2.setMedia(QUrl.fromLocalFile(path_bbox))
        self.player_2.setVideoOutput(self.vWidget_2)

        self.player_1.play()
        self.player_1.pause()
        self.player_2.play()
        self.player_2.pause()

        image = QtGui.QImage(path_img)
        image = image.scaled(self.img_label.size())
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(image))

        ### 재생 속도
        self.videoSpeed = 0.04
        self.player_1.setPlaybackRate(self.videoSpeed)
        self.player_2.setPlaybackRate(self.videoSpeed)
        self.player_1.playbackRate()
        self.player_2.playbackRate()
            

    # GO 버튼 실행
    def sex_btn_clicked(self, button):
        path = self.findRoot + self.findDate + "/" + self.findTime + "/"
        if button.text() == "man":
            path_img = path + "man_heatmap" + self.file_ext(3, path)
        else:
            path_img = path + "woman_heatmap" + self.file_ext(3, path)

        image = QtGui.QImage(path_img)
        image = image.scaled(self.img_label.size())
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(image))

    # 파일 확장자 찾기
    def file_ext(self, index, path):
        filenames = os.listdir(path)
        for file in filenames:
            s = os.path.splitext(file)
            if (index == 1 and s[0] == 'ori'):
                return s[1]
            elif (index == 2 and s[0] == 'bbox'):
                return s[1]
            elif (index == 3 and s[0] == 'man_heatmap'):
                return s[1]

    def play_btn_clicked(self):
        self.player_1.play()
        self.player_2.play()

    def stop_btn_clicked(self):
        self.player_1.pause()
        self.player_2.pause()


    # 영상 파일 검색
    def dirBtn_clicked(self):
        file_name = QFileDialog.getOpenFileName(None, "FileSearch", "/home/js/Mask_RCNN/videos",
                                                "Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v)")
        self.file_name = file_name[0]

        if(os.path.isfile(self.file_name)):
            self.dirBtn_label.setText(self.file_name)
            self.dirBtn_label.setStyleSheet("color: black; font-size: 30px")

            self.realBtn_bool = True

            t = threading.Thread(target=self.execBtn_clicked())
            t.daemon = True
            t.start()
        else:
            self.dirBtn_label.setText("No File")
            self.dirBtn_label.setStyleSheet("color: red")


    def display_instances(self, image, image2, boxes, masks, ids, names, scores):
        """
            take the image and results and apply the mask, box, and Label
        """
        n_instances = boxes.shape[0]

        if not n_instances:
            print('NO INSTANCES TO DISPLAY')
        else:
            assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

        for i in range(n_instances):
            if not np.any(boxes[i]):
                continue

            y1, x1, y2, x2 = boxes[i]

            # x,y 좌표 넣기
            location = [x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2]

            # scroll 변수
            scroll_txt_w = ""
            scroll_txt_m = ""

            txt = str(location[0]) + " " + str(location[1])
            if (ids[i] == 1):
                self.f_woman.write(str(location[0]))
                self.f_woman.write(" ")
                self.f_woman.write(str(location[1]))
                self.f_woman.write('\n')
                # scroll
                self.scroll_w += 1
                scroll_txt_w = "여자    " + txt + "     " + str(self.scroll_w) + "\n"
                scroll_txt_w = scroll_txt_w + self.content_1_widget.text()
                self.content_1_widget.setText(scroll_txt_w)

            elif (ids[i] == 2):
                self.f_man.write(str(location[0]))
                self.f_man.write(" ")
                self.f_man.write(str(location[1]))
                self.f_man.write('\n')
                # scroll
                self.scroll_m += 1
                scroll_txt_m = "남자    " + txt + "     " + str(self.scroll_m) + "\n"
                scroll_txt_m = scroll_txt_m + self.content_2_widget.text()
                self.content_2_widget.setText(scroll_txt_m)


            label = names[ids[i]]
            score = scores[i] if scores is not None else None
            caption = '{} {:.2f}'.format(label, score) if score else label
            mask = masks[:, :, i]
            # image = frame
            if (ids[i] == 1):
                # image = self.apply_mask(image, mask, (255, 0, 0))
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 4)
                image = cv2.putText(
                    image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 0, 0), 2
                )
            else:
                # image = self.apply_mask(image, mask, (0, 0, 255))
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 4)
                image = cv2.putText(
                    image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2
                )

        self.vid.write(image)
        self.vid2.write(image2)

        assert (np.max(image) <= 255)
        image = image.astype(np.uint8, order='C', casting='unsafe')
        image2 = image2.astype(np.uint8, order='C', casting='unsafe')
        height, width, colors = image.shape
        height2, width2, colors2 = image2.shape
        bytesPerLine = 3 * width
        bytesPerLine2 = 3 * width

        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()

        image2 = QImage(image2.data, width2, height2, bytesPerLine2, QImage.Format_RGB888)
        image2 = image2.rgbSwapped()

        if image.isNull() or image2.isNull():
            print("img not load")

        self.realShow1_widget.setPixmap(QPixmap.fromImage(image))
        QtGui.QGuiApplication.processEvents()


    # 디렉토리 확인 및 생성
    def makedir(self):  
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        now = datetime.now()
        nowDate = now.strftime('%Y%m%d_')
        weekday = now.weekday()
        file_type = os.path.splitext(self.file_name)

        make_dir = self.findRoot + nowDate + week[weekday] + "/"
        if os.path.isdir(make_dir):
            if not os.listdir(make_dir):
                self.dir_cnt = 0
            else:
                self.dir_cnt = int(sorted(os.listdir(make_dir))[-1]) + 1
            hour_dir = self.make_time_format(self.dir_cnt)
            make_dir = make_dir + hour_dir + "/"
            os.mkdir(make_dir)
        else:
            os.mkdir(make_dir)
            make_dir = make_dir + "00/"
            os.mkdir(make_dir)
        bbox_vid = make_dir + "bbox" + file_type[1]
        ori_vid = make_dir + "ori" + file_type[1]

        return make_dir, bbox_vid, ori_vid

    def apply_mask(self, image, mask, color, alpha=0.5):
        """apply mask to image"""
        for n, c in enumerate(color):
            image[:, :, n] = np.where(
                mask == 1,
                image[:, :, n] * (1 - alpha) + alpha * c,
                image[:, :, n]
            )
        return image

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    # Inference 및 영상 동시 재생
    def execBtn_clicked(self):
        # pass

        self.content_1_widget.setText("")
        self.content_2_widget.setText("")


        if self.file_name is None:
            return

        self.save_dir, self.bbox_vid, self.ori_vid = self.makedir()
        self.f_man = open(self.save_dir + 'man.txt', 'w')
        self.f_woman = open(self.save_dir + 'woman.txt', 'w')

        self.capture = cv2.VideoCapture(self.file_name)

        self.frames = []
        self.frames2 = []
        self.frame_count = 0
        self.vid = None
        self.vid2 = None
        self.size = None

        self.exec_content()


    def exec_content(self):
        format = "fmp4"
        fourcc = VideoWriter_fourcc(*format)

        frame_rec = 10
        frame_save = 18000
        while True:
            if(self.realBtn_bool==False):
                return

            ret, frame = self.capture.read()
            
            # Bail out when the video file ends
            if not ret:
                break

            frame2 = frame.copy()
            # Save each frame of the video to a list
            self.frame_count += 1

            if (self.frame_count % frame_rec != 0) & (self.frame_count != frame_save):
                continue
            elif self.frame_count == frame_save:
                self.f_man.close()
                self.f_woman.close()
                self.save_heatmap(self.save_dir)
                self.frame_count = 0
                self.vid.release()
                self.vid2.release()
                self.save_dir, self.bbox_vid, self.ori_vid = self.makedir()
                self.vid = VideoWriter(self.bbox_vid, fourcc, float(30), self.size, True)
                self.vid2 = VideoWriter(self.ori_vid, fourcc, float(30), self.size, True)
                self.f_man = open(self.save_dir + 'man.txt', 'w')
                self.f_woman = open(self.save_dir + 'woman.txt', 'w')
            if self.frame_count == frame_rec:
                cv2.imwrite(self.save_dir + 'img.jpg', frame)
            self.frames.append(frame)
            self.frames2.append(frame2)
            print('frame_count :{0}'.format(self.frame_count))
            if len(self.frames) == batch_size:
                results = model.detect(self.frames, verbose=0)
                for i, item in enumerate(zip(self.frames, self.frames2, results)):
                    frame = item[0]
                    frame2 = item[1]
                    r = item[2]
                    if self.vid is None or self.vid2 is None:
                        if self.size is None:
                            self.size = frame.shape[1], frame.shape[0]
                        self.vid = VideoWriter(self.bbox_vid, fourcc, float(30), self.size, True)
                        self.vid2 = VideoWriter(self.ori_vid, fourcc, float(30), self.size, True)
                    if self.size[0] != frame.shape[1] and self.size[1] != frame.shape[0]:
                        frame = resize(frame, self.size)
                    frame = self.display_instances(
                        frame, frame2, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    )
                # Clear the frames array to start the next batch
                self.frames = []
                self.frames2 = []

        self.f_man.close()
        self.f_woman.close()
        self.save_heatmap(self.save_dir)
        self.capture.release()
        self.vid.release()
        self.vid2.release()


    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.menu_btn.setText(QtWidgets.QApplication.translate("Form", "메뉴", None, -1))
        self.menu_Btn_1.setText(QtWidgets.QApplication.translate("Form", "실시간영상", None, -1))
        self.menu_Btn_2.setText(QtWidgets.QApplication.translate("Form", "전체보기", None, -1))
        self.menu_Btn_3.setText(QtWidgets.QApplication.translate("Form", "조건검색", None, -1))
        # main
        # self.mainlabel_1.setText(QtWidgets.QApplication.translate("Form", "Heat Map", None, -1))
        # self.mainlabel_2.setText(QtWidgets.QApplication.translate("Form", "in CCTV", None, -1))
        self.mainlabel.setText(QtWidgets.QApplication.translate("Form", "남녀의 분포를 Heat Map으로 표현하는 CCTV", None, -1))
        # menu1
        self.subject_label_1.setText(QtWidgets.QApplication.translate("Form", "실시간 비교 영상", None, -1))
        self.dirBtn.setText(QtWidgets.QApplication.translate("Form", "파일", None, -1))
        self.real_playBtn.setText(QtWidgets.QApplication.translate("Form", "재생", None, -1))
        self.real_stopBtn.setText(QtWidgets.QApplication.translate("Form", "정지", None, -1))
        # self.execBtn.setText(QtWidgets.QApplication.translate("Form", "실행", None, -1))
        self.info_label_1.setText(QtWidgets.QApplication.translate("Form", "여자 좌표", None, -1))
        self.info_label_2.setText(QtWidgets.QApplication.translate("Form", "남자 좌표", None, -1))
        # menu2
        self.videoLabel_1.setText(QtWidgets.QApplication.translate("Form", "원본 영상", None, -1))
        self.videoLabel_2.setText(QtWidgets.QApplication.translate("Form", "처리 영상", None, -1))
        self.videoLabel_3.setText(QtWidgets.QApplication.translate("Form", "히트맵", None, -1))
        self.playBtn.setText(QtWidgets.QApplication.translate("Form", "재생", None, -1))
        self.stopBtn.setText(QtWidgets.QApplication.translate("Form", "정지", None, -1))
        self.dateLabel.setText(QtWidgets.QApplication.translate("Form", "Date", None, -1))
        self.timeLabel.setText(QtWidgets.QApplication.translate("Form", "Time", None, -1))
        self.time_list_Btn.setText(QtWidgets.QApplication.translate("Form", "", None, -1))
        self.subject_label_2.setText(QtWidgets.QApplication.translate("Form", "전체 보기", None, -1))
        # menu3
        self.subject_label_3.setText(QtWidgets.QApplication.translate("Form", "조건 검색", None, -1))
        self.radioBtn_1.setText(QtWidgets.QApplication.translate("Form", "시간 마다", None, -1))
        self.radioBtn_2.setText(QtWidgets.QApplication.translate("Form", "요일 마다", None, -1))
        self.radioBtn_3.setText(QtWidgets.QApplication.translate("Form", "월 마다", None, -1))
        self.condiLabel_2.setText(QtWidgets.QApplication.translate("Form", "그래프 분석", None, -1))
        self.condiLabel_1.setText(QtWidgets.QApplication.translate("Form", "히트맵", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("Form", "월 마다", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Form", "요일 마다", None, -1))
        self.groupBox_1.setTitle(QtWidgets.QApplication.translate("Form", "시간 마다", None, -1))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    # Form.show()
    Form.showFullScreen()
    sys.exit(app.exec_())

