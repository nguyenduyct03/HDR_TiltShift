from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QPushButton, QMainWindow, QWidget, QHBoxLayout, QTextEdit,
                             QLabel, QApplication, QLineEdit, QGridLayout, QSlider, QFileDialog)
from PyQt5.QtCore import pyqtSlot, QFileInfo, Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtGui
import os
import cv2
import numpy as np

import sys

from tkinter import filedialog
from tkinter import *

"""
lineEdit :
    linepath 
Button:
    open
    start_hdr
    hdr
    finish_hdr
    tiltshift_x
    tiltshift_y
    manual

Ruler :
    ruler
QWidget:
    hinh1
    hinh2 


"""


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        ui = uic.loadUi('./system/mainwindow.ui', self)

        li = ui.open.clicked.connect(self.pushOpen)

        manual_button = ui.manual.clicked.connect(self.manual_click)
        
        blur_button_x = ui. tiltshift_x.clicked.connect(self.tiltshift_x_click)
        blur_button_y = ui.tiltshift_y.clicked.connect(self.tiltshift_y_click)

        start_hdr_button = ui.start_hdr.clicked.connect(self.start_hdr_click)
        hdr_button = ui.hdr.clicked.connect(self.hdr_process)
        finish_hdr_button = ui.finish_hdr.clicked.connect(self.finish_hdr_click)
        
        ui.ruler.setMinimum(3)
        ui.ruler.setMaximum(21)
        ui.ruler.setValue(7)
        ui.ruler.setSingleStep(2)
        ui.ruler.setTickPosition(QSlider.TicksBelow)
        ui.ruler.setTickInterval(10)

        self.kernel = ui.ruler.value()

        self.widget_1 = ui.hinh1
        self.label = QLabel(self.widget_1)

        self.widget_2 = ui.hinh2
        self.label_2 = QLabel(self.widget_2)

        img = QImage('./system/white.png')
        pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(pixmap)
        self.show()

    def pushOpen(self):
        
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/')
        # d = QFileInfo(str(fname)).absoluteDir()
        # self.absolute = d.absolutePath()
        # text = str(self.absolute).split('\'')[1]
        # self.linepath.setText(text)
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir = "/home/duy/Downloads/",title = "Chọn file ảnh",filetypes = (("jpeg files",".jpg"),("all files",".*")))
        self.linepath.setText(root.filename)
        print(root.filename)
        root.destroy()

    def manual_click(self):

        img = cv2.imread('./system/README.jpg')
        cv2.imshow('./system/README.jpg', img)

    def start_hdr_click(self):
       
        image = cv2.imread(self.linepath.text())

        new_image1 = np.zeros(image.shape, image.dtype)
        new_image2 = np.zeros(image.shape, image.dtype)
        new_image3 = np.zeros(image.shape, image.dtype)
        new_image4 = np.zeros(image.shape, image.dtype)
        new_image5 = np.zeros(image.shape, image.dtype)
        new_image6 = np.zeros(image.shape, image.dtype)

        print(' Processing. Please wait !')
        print('-------------------------')

        alpha = 1.0
        beta = 30
        beta2 = 60
        beta3 = 120
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                for c in range(image.shape[2]):
                    # toi
                    new_image1[y,x,c] = np.clip(alpha*image[y,x,c] - beta3, 0, 255)
                    
                    new_image2[y,x,c] = np.clip(alpha*image[y,x,c] - beta2, 0, 255)
                    
                    new_image3[y,x,c] = np.clip(alpha*image[y,x,c] - beta, 0, 255)
                   # sang
                    new_image4[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)
                    
                    new_image5[y,x,c] = np.clip(alpha*image[y,x,c] + beta2, 0, 255)
                    
                    new_image6[y,x,c] = np.clip(alpha*image[y,x,c] + beta3, 0, 255)

        cv2.imwrite('EV1.jpg', new_image1)
        cv2.imwrite('EV2.jpg', new_image2)
        cv2.imwrite('EV3.jpg', new_image3)

        cv2.imwrite('EV4.jpg', image)

        cv2.imwrite('EV5.jpg', new_image4)
        cv2.imwrite('EV6.jpg', new_image5)
        cv2.imwrite('EV7.jpg', new_image6)

        

        with open("list.txt",'w',encoding = 'utf-8') as f:
            f.write("EV1.jpg\n")
            f.write("EV2.jpg\n")
            f.write("EV3.jpg\n")
            f.write("EV4.jpg\n")
            f.write("EV5.jpg\n")
            f.write("EV6.jpg\n")
            f.write("EV7.jpg\n")

        print("Ok roi Chu Tich !")

    def finish_hdr_click(self):
        
        os.remove("list.txt")
        os.remove("EV1.jpg")
        os.remove("EV2.jpg")
        os.remove("EV3.jpg")
        os.remove("EV4.jpg")
        os.remove("EV5.jpg")
        os.remove("EV6.jpg")
        os.remove("EV7.jpg") 

            

    def tiltshift_x_click(self):
        # print(self.linepath.text())

        self.blurer(0, str(self.linepath.text()))

    def tiltshift_y_click(self):
        # blurer(1)
        self.blurer(1, str(self.linepath.text()))

    def getvalue(self, path):

        li = list()
        images = list()
        times = 0
        with open('./list.txt') as f:
            content = f.readlines()
        get_img = str(content[0]).split()[0]
        #
        # print(get_img)
        ev = float()
        hinhLayMucXam = cv2.imread(os.path.join(path, get_img), 0)
        hinhLayMucXam = np.array(hinhLayMucXam)
        # print(hinhLayMucXam.shape)
        mucXamtb = np.average(hinhLayMucXam)
        if (mucXamtb >= 0 and mucXamtb < 10):
            ev = 0.03125
        if (mucXamtb >= 10 and mucXamtb < 20):
            ev = 0.0625
        if (mucXamtb >= 20 and mucXamtb < 30):
            ev = 0.125
        if (mucXamtb >= 30 and mucXamtb < 40):
            ev = 0.25
        if (mucXamtb >= 40 and mucXamtb < 50):
            ev = 0.5
        if (mucXamtb >= 50 and mucXamtb < 60):
            ev = 1.0
        if (mucXamtb >= 60 and mucXamtb < 70):
            ev = 2.0
        if (mucXamtb >= 70 and mucXamtb < 80):
            ev = 4.0
        if (mucXamtb >= 80 and mucXamtb < 90):
            ev = 8.0
        if (mucXamtb >= 90 and mucXamtb < 100):
            ev = 16.0
        if (mucXamtb >= 100 and mucXamtb < 110):
            ev = 32.0
        if (mucXamtb >= 110 and mucXamtb < 120):
            ev = 64.0

        for line in content:
            # global times
            tokens = line.split()
            images.append(cv2.imread(os.path.join(path, tokens[0])))
            times = times+1
            li.append(ev)
            ev = ev*2
        li = np.array(li, dtype=np.float32)
        return images, li

    def hdr_process(self):
        
        images, times = self.getvalue('.')
        # [Load images and exposure times]
        print(times)
        # [Estimate camera response] cau hinh tham so camera
        calibrate = cv2.createCalibrateDebevec()
        response = calibrate.process(images, times)
        # [Estimate camera response]

        # [Make HDR image]
        merge_debevec = cv2.createMergeDebevec()
        hdr = merge_debevec.process(images, times, response)
        # [Make HDR image]
        cv2.imwrite('hdr.jpg', hdr * 255)  # hdr

        (w, h, _) = hdr.shape
        img = QImage('hdr.jpg')
        pixmap = QPixmap.fromImage(img)
        self.label_2.setPixmap(pixmap)
        # self.widget_2.setGeometry(0, 0, 500, 500)
        cv2.imshow('hdr', hdr)
        cv2.waitKey(0)
        self.widget_1.show()

        

    def blurer(self, typer, path):
        img = cv2.imread(path)
        cv2.waitKey(1)
        if (POSITION['start'] == (0, 0) or POSITION['end'] == (0, 0)):
            pass
        else:
            print(path)
            img = cv2.imread(path)

            imgB = img.copy()

            if (typer == 0):
                imgR = img[int(POSITION['start'][1]):int(POSITION['end'][1]), :]
                # imgB = cv2.GaussianBlur(imgB, (self.kernel, self.kernel), 0)
                imgB = cv2.blur(imgB, (self.kernel, self.kernel), 0)
                imgB[int(POSITION['start'][1]):int(
                    POSITION['end'][1]), :] = imgR
            if (typer == 1):
                imgR = img[:, int(POSITION['start'][0]):int(POSITION['end'][0])]
                # imgB = cv2.GaussianBlur(imgB, (self.kernel, self.kernel), 0)
                imgB = cv2.blur(imgB, (self.kernel, self.kernel), 0)

                imgB[:, int(POSITION['start'][0]):int(
                    POSITION['end'][0])] = imgR

                print("B: ", imgB[:, int(POSITION['start'][0]):int(
                    POSITION['end'][0])].shape, " R: ", imgR.shape)
            
            #     cv2.imwrite("tift.png",imgB)

            
            # # cv2.imwrite("tift.png", cv2.resize(imgB, dim, interpolation = cv2.INTER_AREA))

            

            # img = QImage("tift.png")
            # pixmap = QPixmap.fromImage(img)
            

            # self.label_2.setPixmap(pixmap)


            # img2 = QImage(path)
            # pixmap2 = QPixmap.fromImage(img2)
            
            # resized_2 = cv2.resize(pixmap2, dim, interpolation = cv2.INTER_AREA)

            # self.label.setPixmap(resized_2)

            
            # self.widget_2.setGeometry(0, 0, 1000, 500)
            
            #ghi ra tam hinh
            cv2.imwrite("tift.png", imgB)

            width = 850
            height = 530
            dim = (width, height)
            
            img_resize = cv2.imread("tift.png")
            cv2.imwrite("image_resize.png", cv2.resize(img_resize, dim, interpolation = cv2.INTER_AREA))

            #anh tiltshift
            img = QImage("image_resize.png")
            pixmap = QPixmap.fromImage(img)
            
            self.label_2.setPixmap(pixmap)

            #anh goc
            # img2 = QImage(path)
            # pixmap2 = QPixmap.fromImage(img2)

            # self.label.setPixmap(pixmap2)
            

        cv2.imshow('test', img)
        cv2.waitKey(1)


# mac dinh
POSITION = {'start': (0, 0), 'end': (0, 0)}

# counter
i = 0
# nhan chuot


def mouse_drawing(event, x, y, flags, params):
    global i
    if event == cv2.EVENT_LBUTTONDOWN:
        if i % 2 == 0:
            POSITION['start'] = (x, y)
        else:
            POSITION['end'] = (x, y)
        i = i + 1
        print(POSITION)

        # cv2.imshow("test",img)
        cv2.waitKey(1)


# HDR process image
def loadExposureSeq(path):
    images = []
    times = []
    with open(os.path.join(path, 'list.txt')) as f:
        content = f.readlines()
    for line in content:
        tokens = line.split()
        images.append(cv2.imread(os.path.join(path, tokens[0])))
        times.append(1 / float(tokens[1]))

    return images, np.asarray(times, dtype=np.float32)


if __name__ == '__main__':
    cv2.namedWindow("test")
    cv2.setMouseCallback("test", mouse_drawing)
    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
