import sys, os, random

import timeit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton,QMessageBox,QLineEdit,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

import numpy as np
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from numba import*
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
        icon=QIcon("32959206.png")
        self.setWindowIcon(icon)
        self.setWindowTitle('哈囉')
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.create_main_frame()
        #self.on_draw()
        self.create_menu()
        
     
    def create_menu(self):   
        self.statusBar()
        self.setFocus()
        
        exit = QAction(QIcon('icons/Blue_Flower.ico'), 'Open', self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new file')
        
        exit.triggered.connect(self.openfile)
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
    
    
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
        self.fig.subplots_adjust(left=0.01, bottom=0.08, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
        self.axes = self.fig.add_subplot(1,2,1,projection='3d')
        self.axes.set_aspect('equal')
        self.axes.set_xlim3d(-1,42)
        self.axes.set_ylim3d(-1,42)
        self.axes.set_zlim3d(-1,63)
        xmajorLocator=MultipleLocator(5)
        ymajorLocator=MultipleLocator(5)
        zmajorLocator=MultipleLocator(5)
        self.axes.xaxis.set_major_locator(xmajorLocator)
        self.axes.yaxis.set_major_locator(ymajorLocator)
        self.axes.zaxis.set_major_locator(zmajorLocator)
         
        self.axx = self.fig.add_subplot(243)
        self.axx.set_xlim(0,41)
        self.axx.set_ylim(0,62)
        self.axx.grid(color='k', linestyle='--', linewidth=0.5)
        #self.axx.set_aspect('equal')
        self.axy = self.fig.add_subplot(244)
        self.axy.set_xlim(0,41)
        self.axy.set_ylim(0,62)
        self.axy.grid(color='k', linestyle='--', linewidth=0.5)
        #self.axy.set_aspect('equal')
        self.axz = self.fig.add_subplot(247)
        self.axz.set_xlim(0,41)
        self.axz.set_ylim(0,41)
        self.axz.grid(color='k', linestyle='--', linewidth=0.5)
       # self.axz.set_aspect('equal')
        self.logo=self.fig.add_subplot(248)
        self.logo.set_aspect('equal')
        self.logo.set_xlim(-100,300)
        self.logo.set_ylim(250,-70)
        img = mpimg.imread('32959206.png')
        imgplot = self.logo.imshow(img)
        self.logo.set_axis_off()
        
        slider_labelcolor = QLabel('顯示數值：')
        self.comboboxcolor = QComboBox(self)
        colors=['我全都要','vsave<3','3<vsave<4','4<vsave<5','5<vsave<6','6<vsave<7','8<vsave']
        self.comboboxcolor.addItems(colors)
        self.comboboxcolor.setMaxVisibleItems(5) 
        self.comboboxcolor.activated.connect(self.onecolor)
        
        slider_labelx = QLabel('X:')
        self.sliderx = QSlider(Qt.Horizontal)
        slider_labely = QLabel('Y:')
        self.slidery = QSlider(Qt.Horizontal)
        slider_labelz = QLabel('Z:')
        self.sliderz = QSlider(Qt.Horizontal)
        
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
        
        for w in [  slider_labelcolor,self.comboboxcolor,
                    slider_labelfigp,self.sliderfig,slider_labelfigm,textboxx_label,self.textboxx
                    ,self.sliderx,textboxy_label,self.textboxy,self.slidery,textboxz_label,self.textboxz,self.sliderz,self.drawbutton]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
    def openfile(self):
        filename,  _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        file=open(filename)
        line = file.readline()
        self.test=[]
        while line:
            fline=float(line)
            if fline==0:
                break
            else:
                self.test.append(fline)
                line = file.readline()
        #print(self.test)
        
        self.data= np.zeros((41,41,62), dtype=np.float)
        self.color= np.zeros((41,41,62), dtype=np.int)
        i=0
        j=0
        k=0
        x=0
        while j<41:
            k=0
            while k<62:
               i=0
               while i<41:
                   self.data[i,j,61-k]=self.test[x]
                   
                   if self.test[x]<3:
                       self.color[i,j,61-k]=0
                   elif self.test[x]>3 and self.test[x]<4:
                       self.color[i,j,61-k]=1
                   elif self.test[x]>4 and self.test[x]<5:
                       self.color[i,j,61-k]=2
                   elif self.test[x]>5 and self.test[x]<6:
                       self.color[i,j,61-k]=3
                   elif self.test[x]>6 and self.test[x]<7:
                       self.color[i,j,61-k]=4
                   elif self.test[x]>7 and self.test[x]<8:
                       self.color[i,j,61-k]=5
                   elif self.test[x]>8:
                       self.color[i,j,61-k]=6
                   x=x+1
                   i=i+1
               k=k+1
            j=j+1        
        print(self.color[40,40,61])
        print(self.test[104221])
        self.on_draw()
    
    def on_draw(self):
        b=0
        while b<41:
            c=0
            while c<62:
                self.edges = [
                        [(0,0+b,0+c),(1,0+b,0+c),(1,1+b,0+c),(0,1+b,0+c)],
                        [(1,0+b,0+c),(1,1+b,0+c),(1,1+b,1+c),(1,0+b,1+c)],
                        [(0,1+b,0+c),(0,1+b,1+c),(1,1+b,1+c),(1,1+b,0+c)],
                        [(0,1+b,1+c),(0,1+b,0+c),(0,0+b,0+c),(0,0+b,1+c)],
                        [(0,0+b,0+c),(0,0+b,1+c),(1,0+b,1+c),(1,0+b,0+c)],
                        [(0,1+b,1+c),(0,0+b,1+c),(1,0+b,1+c),(1,1+b,1+c)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)
                if self.color[0,b,c]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[0,b,c]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[0,b,c]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[0,b,c]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[0,b,c]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[0,b,c]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[0,b,c]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                c=c+1
            b=b+1
        
        b=0
        while b<41:
            c=0
            while c<62:
                self.edges = [
                        [(40,0+b,0+c),(41,0+b,0+c),(41,1+b,0+c),(40,1+b,0+c)],
                        [(41,0+b,0+c),(41,1+b,0+c),(41,1+b,1+c),(41,0+b,1+c)],
                        [(40,1+b,0+c),(40,1+b,1+c),(41,1+b,1+c),(41,1+b,0+c)],
                        [(40,1+b,1+c),(40,1+b,0+c),(40,0+b,0+c),(40,0+b,1+c)],
                        [(40,0+b,0+c),(40,0+b,1+c),(41,0+b,1+c),(41,0+b,0+c)],
                        [(40,1+b,1+c),(40,0+b,1+c),(41,0+b,1+c),(41,1+b,1+c)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)
                if self.color[40,b,c]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[40,b,c]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[40,b,c]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[40,b,c]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[40,b,c]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[40,b,c]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[40,b,c]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                c=c+1
            b=b+1
        
        a=0
        while a<41:
            c=0
            while c<62:
                self.edges = [
                        [(0+a,40,0+c),(1+a,40,0+c),(1+a,41,0+c),(0+a,41,0+c)],
                        [(1+a,40,0+c),(1+a,41,0+c),(1+a,41,1+c),(1+a,40,1+c)],
                        [(0+a,41,0+c),(0+a,41,1+c),(1+a,41,1+c),(1+a,41,0+c)],
                        [(0+a,41,1+c),(0+a,41,0+c),(0+a,40,0+c),(0+a,40,1+c)],
                        [(0+a,40,0+c),(0+a,40,1+c),(1+a,40,1+c),(1+a,40,0+c)],
                        [(0+a,41,1+c),(0+a,40,1+c),(1+a,40,1+c),(1+a,41,1+c)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)    
                if self.color[a,40,c]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[a,40,c]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[a,40,c]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[a,40,c]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[a,40,c]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[a,40,c]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[a,40,c]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                c=c+1
            a=a+1
        
        a=0
        while a<41:
            c=0
            while c<62:
                self.edges = [
                        [(0+a,0,0+c),(1+a,0,0+c),(1+a,1,0+c),(0+a,1,0+c)],
                        [(1+a,0,0+c),(1+a,1,0+c),(1+a,1,1+c),(1+a,0,1+c)],
                        [(0+a,1,0+c),(0+a,1,1+c),(1+a,1,1+c),(1+a,1,0+c)],
                        [(0+a,1,1+c),(0+a,1,0+c),(0+a,0,0+c),(0+a,0,1+c)],
                        [(0+a,0,0+c),(0+a,0,1+c),(1+a,0,1+c),(1+a,0,0+c)],
                        [(0+a,1,1+c),(0+a,0,1+c),(1+a,0,1+c),(1+a,1,1+c)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)          
                if self.color[a,0,c]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[a,0,c]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[a,0,c]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[a,0,c]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[a,0,c]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[a,0,c]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[a,0,c]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                c=c+1
            a=a+1
        
        a=0
        while a<41:
            b=0
            while b<41:
                self.edges = [
                        [(0+a,0+b,0),(1+a,0+b,0),(1+a,1+b,0),(0+a,1+b,0)],
                        [(1+a,0+b,0),(1+a,1+b,0),(1+a,1+b,1),(1+a,0+b,1)],
                        [(0+a,1+b,0),(0+a,1+b,1),(1+a,1+b,1),(1+a,1+b,0)],
                        [(0+a,1+b,1),(0+a,1+b,0),(0+a,0+b,0),(0+a,0+b,1)],
                        [(0+a,0+b,0),(0+a,0+b,1),(1+a,0+b,1),(1+a,0+b,0)],
                        [(0+a,1+b,1),(0+a,0+b,1),(1+a,0+b,1),(1+a,1+b,1)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)
                
                if self.color[a,b,0]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[a,b,0]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[a,b,0]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[a,b,0]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[a,b,0]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[a,b,0]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[a,b,0]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                b=b+1
            a=a+1
            
        a=0
        while a<41:
            b=0
            while b<41:
                self.edges = [
                        [(0+a,0+b,61),(1+a,0+b,61),(1+a,1+b,61),(0+a,1+b,61)],
                        [(1+a,0+b,61),(1+a,1+b,61),(1+a,1+b,62),(1+a,0+b,62)],
                        [(0+a,1+b,61),(0+a,1+b,62),(1+a,1+b,62),(1+a,1+b,61)],
                        [(0+a,1+b,62),(0+a,1+b,61),(0+a,0+b,61),(0+a,0+b,62)],
                        [(0+a,0+b,61),(0+a,0+b,62),(1+a,0+b,62),(1+a,0+b,61)],
                        [(0+a,1+b,62),(0+a,0+b,62),(1+a,0+b,62),(1+a,1+b,62)]]
                self.faces = Poly3DCollection(self.edges,zorder=1)
                if self.color[a,b,61]==0:
                    self.faces.set_facecolor((1,0,0.1,1))
                elif self.color[a,b,61]==1:
                    self.faces.set_facecolor((1,0.5,0,1))
                elif self.color[a,b,61]==2:
                    self.faces.set_facecolor((1,1,0,1))
                elif self.color[a,b,61]==3:
                    self.faces.set_facecolor((0.5,1,0,1))
                elif self.color[a,b,61]==4:
                    self.faces.set_facecolor((0,1,1,1))
                elif self.color[a,b,61]==5:
                    self.faces.set_facecolor((0,0,1,1))
                elif self.color[a,b,61]==6:
                    self.faces.set_facecolor((0.5,0.2,0.9,1))
                self.axes.add_collection3d(self.faces)
                b=b+1
            a=a+1
        self.canvas.draw()
        
        
    def coloronly(self,index,r,b,g,a):
        self.axes.cla()
        self.axes.set_xlim3d(-1,42)
        self.axes.set_ylim3d(-1,42)
        self.axes.set_zlim3d(-1,63)
        xmajorLocator=MultipleLocator(5)
        ymajorLocator=MultipleLocator(5)
        zmajorLocator=MultipleLocator(5)
        self.axes.xaxis.set_major_locator(xmajorLocator)
        self.axes.yaxis.set_major_locator(ymajorLocator)
        self.axes.zaxis.set_major_locator(zmajorLocator)
        i=0
        while i<41:
            j=0
            while j<41:
                k=0
                while k<62: 
                    if self.color[i,j,k]==index:
                        print(self.color[i,j,k],index)
                        self.edges = [
                                [(0+i,0+j,0+k),(1+i,0+j,0+k),(1+i,1+j,0+k),(0+i,1+j,0+k)],
                                [(1+i,0+j,0+k),(1+i,1+j,0+k),(1+i,1+j,1+k),(1+i,0+j,1+k)],
                                [(0+i,1+j,0+k),(0+i,1+j,1+k),(1+i,1+j,1+k),(1+i,1+j,0+k)],
                                [(0+i,1+j,1+k),(0+i,1+j,0+k),(0+i,0+j,0+k),(0+i,0+j,1+k)],
                                [(0+i,0+j,0+k),(0+i,0+j,1+k),(1+i,0+j,1+k),(1+i,0+j,0+k)],
                                [(0+i,1+j,1+k),(0+i,0+j,1+k),(1+i,0+j,1+k),(1+i,1+j,1+k)]]
                        self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)
                        self.faces.set_facecolor((r,b,g,a))
                        self.axes.add_collection3d(self.faces)
                    k=k+1
                j=j+1
            i=i+1
        print('finish',r,b,g,a)
        self.canvas.draw()
    def onecolor(self):
        r=0
        b=0
        g=0
        a=0
        index=self.comboboxcolor.currentIndex()
        print(index*index)
        if index==0:
            self.on_draw()
        else:
            if index==1:
                r=1
                b=0
                g=0.1
                a=1
            elif index==2:
                r=1
                b=0.5
                g=0
                a=1
            elif index==3:
                r=1
                b=1
                g=0
                a=1
            elif index==4:
                r=0.5
                b=1
                g=0
                a=1
            elif index==5:
                r=0
                b=1
                g=1
                a=1
            elif index==6:
                r=0
                b=0
                g=1
                a=1
            elif index==7:
                r=0.5
                b=0.2
                g=0.9
                a=1
            self.coloronly(index-1,r,b,g,a)            

    
    def drawsection(self):
        xsec=self.textboxx.text()
        ysec=self.textboxy.text()
        zsec=self.textboxz.text()
        self.plot(xsec,ysec,zsec)
        self.showsection(xsec,ysec,zsec)
    
    def plot(self,a,b,c):
        #self.axes.cla()
        aa=float(a)
        bb=float(b)
        cc=float(c)
        
        line1 = self.axes.plot([aa,aa], [45,-1], [63,63], '-', c='k',linewidth=3,zorder=20)
        line2 = self.axes.plot([aa,aa], [-1,-1], [63,-1], '-', c='k',linewidth=3,zorder=20)
        line3 = self.axes.plot([aa,aa], [45,45], [63,-1], '-', c='k',linewidth=3,zorder=20)
        line4 = self.axes.plot([aa,aa], [-1,45], [-1,-1], '-', c='k',linewidth=3,zorder=20)
        
        line5 = self.axes.plot([42,-1], [bb,bb], [63,63], '-', c='k',linewidth=3,zorder=20)
        line6 = self.axes.plot([-1,-1], [bb,bb], [63,-1], '-', c='k',linewidth=3,zorder=20)
        line7 = self.axes.plot([42,42], [bb,bb], [63,-1], '-', c='k',linewidth=3,zorder=20)
        line8 = self.axes.plot([-1,42], [bb,bb], [-1,-1], '-', c='k',linewidth=3,zorder=20)
        
        line9 = self.axes.plot([42,42], [42,-1], [cc,cc], '-', c='k',linewidth=3,zorder=20)
        line10 = self.axes.plot([42,-1], [-1,-1], [cc,cc], '-', c='k',linewidth=3,zorder=20)
        line11 = self.axes.plot([-1,42], [42,42], [cc,cc], '-', c='k',linewidth=3,zorder=20)
        line12 = self.axes.plot([-1,-1], [-1,42], [cc,cc], '-', c='k',linewidth=3,zorder=20)
        
        self.canvas.draw()
        
    def showsection(self,a,b,c):
        #self.axx.cla()
        #self.axy.cla()
        #self.axz.cla()
        #self.axz.set_aspect('equal')
        aa=int(a)
        bb=int(b)
        cc=int(c)
      
        j=0
        k=0
        while j<41:
            k=0
            while k<62:
                if self.data[aa,j,k]<3:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(1,0,0.1,1))
                elif self.data[aa,j,k]>3 and self.data[aa,j,k]<4:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(1,0.5,0,1))
                elif self.data[aa,j,k]>4 and self.data[aa,j,k]<5:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(1,1,0,1))
                elif self.data[aa,j,k]>5 and self.data[aa,j,k]<6:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(0.5,1,0,1))
                elif self.data[aa,j,k]>6 and self.data[aa,j,k]<7:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(0,1,1,1))
                elif self.data[aa,j,k]>7 and self.data[aa,j,k]<8:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(0,0,1,1))
                elif self.data[aa,j,k]>8:
                    rectangle = mpatches.Rectangle((0+j,0+k),1,1,color=(0.5,0.2,0.9,1))
                print(self.data[aa,j,k])
                self.axx.add_patch(rectangle)
                k=k+1
            j=j+1
        self.canvas.draw()
        
        i=0
        k=0
        while i<41:
            k=0
            while k<62:
                if self.data[i,bb,k]<3:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(1,0,0.1,1))
                elif self.data[i,bb,k]>3 and self.data[i,bb,k]<4:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(1,0.5,0,1))
                elif self.data[i,bb,k]>4 and self.data[i,bb,k]<5:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(1,1,0,1))
                elif self.data[i,bb,k]>5 and self.data[i,bb,k]<6:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(0.5,1,0,1))
                elif self.data[i,bb,k]>6 and self.data[i,bb,k]<7:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(0,1,1,1))
                elif self.data[i,bb,k]>7 and self.data[i,bb,k]<8:
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(0,0,1,1))
                elif self.data[i,bb,k]>8:
                    rectangle = mpatches.Rectangle((0+i,61-k),1,1,color=(0.5,0.2,0.9,1))
                print(self.data[i,bb,k])
                self.axy.add_patch(rectangle)
                k=k+1
            i=i+1
        self.canvas.draw()
        
        i=0
        j=0
        while i<41:
            j=0
            while j<41:
                if self.data[i,j,cc]<3:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(1,0,0.1,1))
                elif self.data[i,j,cc]>3 and self.data[i,j,cc]<4:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(1,0.5,0,1))
                elif self.data[i,j,cc]>4 and self.data[i,j,cc]<5:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(1,1,0,1))
                elif self.data[i,j,cc]>5 and self.data[i,j,cc]<6:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(0.5,1,0,1))
                elif self.data[i,j,cc]>6 and self.data[i,j,cc]<7:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(0,1,1,1))
                elif self.data[i,j,cc]>7 and self.data[i,j,cc]<8:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(0,0,1,1))
                elif self.data[i,j,cc]>8:
                    rectangle = mpatches.Rectangle((0+i,0+j),1,1,color=(0.5,0.2,0.9,1),)
                print(self.data[i,j,cc])
                self.axz.add_patch(rectangle)
                j=j+1
            i=i+1
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
