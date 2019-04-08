import sys, os, random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton,QMessageBox,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('哈囉')
        self.create_main_frame()
        self.on_draw()
        self.create_menu()
        self.line()
     
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.help_menu = self.menuBar().addMenu("&Help")
    
    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    
    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((15.0, 12.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.   
        self.axes = self.fig.add_subplot(1,2,2,projection='3d')
        self.axes.set_xlim3d(-1100,1100)
        self.axes.set_ylim3d(-1100,1100)
        self.axes.set_zlim3d(-1100,1100)
        xmajorLocator=MultipleLocator(250)
        ymajorLocator=MultipleLocator(250)
        zmajorLocator=MultipleLocator(250)
        self.axes.xaxis.set_major_locator(xmajorLocator)
        self.axes.yaxis.set_major_locator(ymajorLocator)
        self.axes.zaxis.set_major_locator(zmajorLocator)
         
        self.axx = self.fig.add_subplot(321)
        self.axy = self.fig.add_subplot(323)
        self.axz = self.fig.add_subplot(325)
        
        self.cb1 = QCheckBox("red")
        self.cb2 = QCheckBox("yellow")
        self.cb3 = QCheckBox("green")
        self.cb4 = QCheckBox("blue")
        self.cb5 = QCheckBox("purple")
        self.cb1.setChecked(True)
        self.cb2.setChecked(True)
        self.cb3.setChecked(True)
        self.cb4.setChecked(True)
        self.cb5.setChecked(True)
        
        self.cb1.stateChanged.connect(self.on_draw)
        self.cb2.stateChanged.connect(self.on_draw)
        self.cb3.stateChanged.connect(self.on_draw)
        self.cb4.stateChanged.connect(self.on_draw)
        self.cb5.stateChanged.connect(self.on_draw)
        
        
       # slider_labelx = QLabel('X:')
       # self.sliderx = QSlider(Qt.Horizontal)
       # slider_labely = QLabel('Y:')
       # self.slidery = QSlider(Qt.Horizontal)
       # slider_labelz = QLabel('Z:')
       # self.sliderz = QSlider(Qt.Horizontal)
        
        slider_labelfigp = QLabel('+')
        self.sliderfig = QSlider(Qt.Horizontal)
        slider_labelfigm = QLabel('-')
        
        textboxx_label = QLabel('X:')
        self.textboxx = QLineEdit(self)
        textboxy_label = QLabel('Y:')
        self.textboxy = QLineEdit(self)
        textboxz_label = QLabel('Z:')
        self.textboxz = QLineEdit(self)
        
        self.drawbutton=QPushButton()
        self.drawbutton.setText('DRAW')
        self.drawbutton.clicked.connect(self.drawsection)
        
        
        hbox = QHBoxLayout()
        
        for w in [  self.cb1, self.cb2, self.cb3,
                    self.cb4,self.cb5,
                    slider_labelfigp,self.sliderfig,slider_labelfigm,textboxx_label,self.textboxx
                    ,textboxy_label,self.textboxy,textboxz_label,self.textboxz,self.drawbutton]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
    def on_draw(self):
        b=0
        while b<2000:
            self.edges = [
            [(-1000,-1000,-1000+b),(-1000,-1000,-600+b),(-1000,1000,-600+b),(-1000,1000,-1000+b)],
            [(-1000,1000,-1000+b),(-1000,1000,-600+b),(1000,1000,-600+b),(1000,1000,-1000+b)],
            [(1000,1000,-1000+b),(1000,-1000,-1000+b),(1000,-1000,-600+b),(1000,1000,-600+b)],
            [(1000,-1000,-1000+b),(1000,-1000,-600+b),(-1000,-1000,-600+b),(-1000,-1000,-1000+b)],
            [(-1000,-1000,-1000+b),(1000,-1000,-1000+b),(1000,1000,-1000+b),(-1000,1000,-1000+b)],
            [(-1000,-1000,-600+b),(1000,-1000,-600+b),(1000,1000,-600+b),(-1000,1000,-600+b)]]
            b=b+400
            print(b)
            self.faces = Poly3DCollection(self.edges)
            #,linewidths=1,edgecolors='k'
            if b==400 and self.cb1.isChecked():
                self.faces.set_facecolor((1,0,0,0.5))
            elif b==800 and self.cb2.isChecked():
                self.faces.set_facecolor((1,1,0,0.5))
            elif b==1200 and self.cb3.isChecked():
                self.faces.set_facecolor((0,0.5,0,0.5))
            elif b==1600 and self.cb4.isChecked():
                self.faces.set_facecolor((0,0,1,0.5))
            elif b==2000 and self.cb5.isChecked():
                self.faces.set_facecolor((0.5,0,1,0.5))

            self.axes.add_collection3d(self.faces)
        
        self.axes.set_aspect('equal')
        self.canvas.draw()
       
        
    def colorclickboxes(self):
        print('hi')
    
    def drawsection(self):
        xsec=self.textboxx.text()
        ysec=self.textboxy.text()
        zsec=self.textboxz.text()
        self.plot(xsec,ysec,zsec)
             
    def plot(self,a,b,c):
        aa=float(a)
        bb=float(b)
        cc=float(c)
        self.line1 = self.axes.plot([aa,aa], [1010,-1010], [1010,1010], '-', c='k',linewidth=3)
        self.line2 = self.axes.plot([aa,aa], [-1010,-1010], [1010,-1010], '-', c='k',linewidth=3)
        self.line3 = self.axes.plot([aa,aa], [1010,1010], [1010,-1010], '-', c='k',linewidth=3)
        self.line4 = self.axes.plot([aa,aa], [-1010,1010], [-1010,-1010], '-', c='k',linewidth=3)
        
        self.line5 = self.axes.plot([1010,-1010], [bb,bb], [1010,1010], '-', c='k',linewidth=3)
        self.line6 = self.axes.plot([-1010,-1010], [bb,bb], [1010,-1010], '-', c='k',linewidth=3)
        self.line7 = self.axes.plot([1010,1010], [bb,bb], [1010,-1010], '-', c='k',linewidth=3)
        self.line8 = self.axes.plot([-1010,1010], [bb,bb], [-1010,-1010], '-', c='k',linewidth=3)
        
        self.line9 = self.axes.plot([1010,1010], [1010,-1010], [cc,cc], '-', c='k',linewidth=3)
        self.line10 = self.axes.plot([1010,-1010], [-1010,-1010], [cc,cc], '-', c='k',linewidth=3)
        self.line11 = self.axes.plot([-1010,1010], [1010,1010], [cc,cc], '-', c='k',linewidth=3)
        self.line12 = self.axes.plot([-1010,-1010], [-1010,1010], [cc,cc], '-', c='k',linewidth=3)
        
        self.canvas.draw()
    
    def line(self):
        ymin,ymax=self.axes.get_ylim()
        ymid=0.5*(ymin+ymax)
        self.line=self.axes.axhline(ymid,color='r')
        self.fig.canvas.mpl_connect('button_press_event',self.onpress)
        self.fig.canvas.mpl_connect('button_release_event',self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event',self.onmove)
        self.pressevent=None
    
    def onpress(self,event):
        if event.inaxes !=self.axes:
            return
        self.pressevent=event
    
    def onrelease(self,event):
        self.pressevent=None
        print(event.ydata)
    
    def onmove(self,event):
        if self.pressevent is None or event.inaxes != self.pressevent.inaxes:
            return
        self.line.set_ydata((event.ydata,event.ydata))
        self.fig.canvas.draw()

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
