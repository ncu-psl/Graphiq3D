import sys, os, random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton,QMessageBox,QLineEdit,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from numba import jit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


class AppForm(QMainWindow,QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        icon=QIcon("32959206.png")
        self.setWindowIcon(icon)
        self.setWindowTitle('Graphic3D')
        self.setup(self)
        self.create_main_frame()
        self.create_menu()
        
        
    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("#MainWindow { border-image: url(bg.png) 0 0 0 0 stretch stretch; }")
        self.centralwidget =QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
    
    def create_menu(self):   
        #self.statusBar()
        #self.setFocus()
        openfile = QAction(QIcon('icons/Blue_Flower.ico'), 'Open', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open new file')
        openfile.triggered.connect(self.openfile)
        quitui = QAction(QIcon('icons/Blue_Flower.ico'), 'Quit', self)
        quitui.setShortcut('Ctrl+Q')
        quitui.setStatusTip('Quit')
        quitui.triggered.connect(self.close)
        saveplot = QAction(QIcon('icons/Blue_Flower.ico'), 'Save Plot', self)
        saveplot.setShortcut('Ctrl+S')
        saveplot.setStatusTip('Save Plot')
        saveplot.triggered.connect(self.save_plot)
        about = QAction(QIcon('icons/Blue_Flower.ico'), 'About', self)
        about.setShortcut('Ctrl+A')
        about.setStatusTip('About')
        about.triggered.connect(self.on_about)
        
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(openfile)
        file.addAction(saveplot)
        file.addAction(quitui)
        helpabout = menubar.addMenu('&Help')
        helpabout.addAction(about)
     
        
    def mainaxes(self):
        self.axes = self.fig.add_subplot(1,2,1,projection='3d')
        self.axes.set_alpha(0)
        self.axes.patch.set_alpha(0) 
        self.axes.set_aspect('equal')
        self.axes.set_xlim3d(-1,42)
        self.axes.set_ylim3d(-1,42)
        self.axes.set_zlim3d(-1,63)
        self.axes.set_xlabel('x-axis')
        self.axes.set_ylabel('y-axis')
        self.axes.set_zlabel('z-axis')
        xmajorLocator=MultipleLocator(5)
        ymajorLocator=MultipleLocator(5)
        zmajorLocator=MultipleLocator(5)
        self.axes.xaxis.set_major_locator(xmajorLocator)
        self.axes.yaxis.set_major_locator(ymajorLocator)
        self.axes.zaxis.set_major_locator(zmajorLocator)
        
    def create_main_frame(self):
        #self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((15.0, 12.0), dpi=self.dpi)
        self.fig.set_facecolor('none')
        self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)
        self.canvas.setParent(self.centralwidget)
        self.canvas.setStyleSheet("background-color:transparent;")
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        self.fig.subplots_adjust(left=0.03, bottom=0.08, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
        self.mainaxes()
        xmajorLocator=MultipleLocator(5)
        ymajorLocator=MultipleLocator(5)
        xminorLocator=MultipleLocator(1)
        yminorLocator=MultipleLocator(1)
        self.axx = self.fig.add_subplot(243)
        self.axx.set_xlim(0,41)
        self.axx.set_ylim(0,62)
        self.axx.grid(color='k', linestyle='--', linewidth=0.5,which='minor')
        self.axx.xaxis.set_major_locator(xmajorLocator)
        self.axx.yaxis.set_major_locator(ymajorLocator)
        self.axx.xaxis.set_minor_locator(xminorLocator)
        self.axx.yaxis.set_minor_locator(yminorLocator)
        self.axx.set_title('Y-Z section',loc='center')
        #self.axx.set_aspect('equal')
        self.axy = self.fig.add_subplot(244)
        self.axy.set_xlim(0,41)
        self.axy.set_ylim(0,62)
        self.axy.grid(color='k', linestyle='--', linewidth=0.5,which='minor')
        self.axy.xaxis.set_major_locator(xmajorLocator)
        self.axy.yaxis.set_major_locator(ymajorLocator)
        self.axy.xaxis.set_minor_locator(xminorLocator)
        self.axy.yaxis.set_minor_locator(yminorLocator)
        self.axy.set_title('X-Z section',loc='center')
        #self.axy.set_aspect('equal')
        self.axz = self.fig.add_subplot(248)
        self.axz.set_xlim(0,41)
        self.axz.set_ylim(0,41)
        self.axz.grid(color='k', linestyle='--', linewidth=0.5,which='minor')
        xmajorLocator=MultipleLocator(5)
        ymajorLocator=MultipleLocator(5)
        xminorLocator=MultipleLocator(1)
        yminorLocator=MultipleLocator(1)
        self.axz.xaxis.set_major_locator(xmajorLocator)
        self.axz.yaxis.set_major_locator(ymajorLocator)
        self.axz.xaxis.set_minor_locator(xminorLocator)
        self.axz.yaxis.set_minor_locator(yminorLocator)
        self.axz.set_title('X-Y section',loc='center')
        #self.axz.set_aspect('equal')
        self.logo=self.fig.add_subplot(247)
        self.logo.set_aspect('equal')
        #self.logo.set_xlim(-100,300)
        #self.logo.set_ylim(250,-70)
        img = mpimg.imread('color.png')
        imgplot = self.logo.imshow(img)
        self.logo.set_axis_off()
        self.fig.canvas.mpl_connect('button_press_event',self.onpressx)
        self.fig.canvas.mpl_connect('button_press_event',self.onpressy)
        self.fig.canvas.mpl_connect('button_press_event',self.onpressz)
        
        
        font = QFont() 
        font.setFamily('Comic Sans MS')
        font.setBold(True) 
        #大小
        font.setPointSize(10) 
        font.setWeight(60) 
        slider_labelcolor = QLabel('Show:')
        slider_labelcolor.setFont(font) 
        #slider_labelcolor.setText("<font color=%s>%s</font>" %('#000000', "Show:"))

        self.comboboxcolor = QComboBox(self)
        colors=['View All','vsave < 3','3 < vsave < 4','4 < vsave < 5','5 < vsave < 6','6 < vsave < 7','8 < vsave']
        self.comboboxcolor.addItems(colors)
        #self.comboboxcolor.setMaxVisibleItems(5) 
        self.comboboxcolor.setStyleSheet("border: 1px solid gray;border-radius:3px;padding: 1px 18px 1px 3px;min-width: 5em;selection-background-color: darkgray;")
        self.comboboxcolor.setFont(font) 
        self.comboboxcolor.activated.connect(self.onecolor)
        
        
        self.returnbtn = QPushButton()
        self.returnbtn.setFont(font) 
        self.returnbtn.clicked.connect(self.zoom)
        self.returnbtn.setStyleSheet('QPushButton{border-image:url(return.png)}')
        self.zoombutton=QPushButton()
        self.zoombutton.setText('ZOOM')
        self.zoombutton.setFont(font) 
        self.zoombutton.setStyleSheet("color:white;background-color:black;border-radius:4px;min-width: 5em;")
        self.i=0
        self.zoombutton.clicked.connect(self.count)
        self.sliderfig = QSlider(Qt.Horizontal)
        self.sliderfig.setRange(0,99)
        self.sliderfig.setStyleSheet("QSlider::handle:horizontal { border-radius:3px;border-image:url(rb.png);}")
        self.sliderfig.valueChanged.connect(self.zoomin)
        self.labezoomin = QLabel(self)
        self.labezoomout = QLabel(self)
        self.pixmapin = QPixmap('zo_opt.png')
        self.labezoomin.setPixmap(self.pixmapin)
        self.pixmapout = QPixmap('zi_opt.png')
        self.labezoomout.setPixmap(self.pixmapout)
        
        textboxx_label = QLabel('  Y-Z section : ')
        self.textboxx = QLineEdit(self)
        self.textboxx.setText('0')
        textboxx_label.setFont(font) 
        self.textboxx.setStyleSheet("border: 1px solid gray;border-radius:4px;padding: 1px 18px 1px 3px;min-width: 3em;")
        textboxy_label = QLabel('  X-Z section : ')
        self.textboxy = QLineEdit(self)
        self.textboxy.setText('0')
        textboxy_label.setFont(font) 
        self.textboxy.setStyleSheet("border: 1px solid gray;border-radius:4px;padding: 1px 18px 1px 3px;min-width: 3em;")
        textboxz_label = QLabel('  X-Y section : ')
        self.textboxz = QLineEdit(self)
        self.textboxz.setText('0')
        textboxz_label.setFont(font) 
        self.textboxz.setStyleSheet("border: 1px solid gray;border-radius:4px;padding: 1px 18px 1px 3px;min-width: 3em;")
        
        self.drawbutton=QPushButton()
        self.drawbutton.setText('DRAW')
        self.drawbutton.setFont(font) 
        self.drawbutton.setStyleSheet("color:white;background-color:black;border-radius:4px;min-width: 5em;")
        self.drawbutton.clicked.connect(self.drawsection)
              
        hbox = QHBoxLayout()
        
        for w in [  self.zoombutton,self.returnbtn,self.labezoomin,self.sliderfig,self.labezoomout,slider_labelcolor,
                  self.comboboxcolor,textboxx_label,self.textboxx
                    ,textboxy_label,self.textboxy,textboxz_label,self.textboxz,self.drawbutton]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)
            
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        
        #self.main_frame.setLayout(vbox)
        #self.setCentralWidget(self.main_frame)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(vbox)
        #self.setCentralWidget.setMouseTracking(True) 
        
    
    def on_about(self):
        msg = """
                    * Choose .pvel file
* Input the number which scale of the 
  sections in three axis separately
  you want to display then push the 
  'DRAW' button to show the 2D sections
* Use the slider to zoom in/out the 
  3D model of the .pvel file
* You can display single layer in
  3D model by using the combobox
                                                         """
        QMessageBox.about(self, "About Graphic3D", msg.strip())
    
    def count(self):
        self.i+=1
        if self.i%2==1:
            self.zoombutton.setStyleSheet("color:white;background-color:red;border-radius:4px;min-width: 5em;")
            self.zoomcenter()
            self.zoom()
        else:
            self.zoombutton.setStyleSheet("color:white;background-color:black;border-radius:4px;min-width: 5em;")
            self.setMouseTracking(False)
            self.fig.delaxes(self.zoomin)
            self.mainaxes()
            self.on_draw()
        
    def zoomcenter(self):
        if self.i%2==1:
            #self.fig.canvas.mpl_connect('button_press_event',self.onpress)
            self.fig.canvas.mpl_connect('button_release_event',self.onrelease)
            self.pressevent=None
            
    def onpressx(self,event):
        if event.inaxes !=self.axx:
            return
        self.pressevent=None
        self.x=event.xdata
        self.y=event.ydata
        val=self.textboxx.text()
        v=int(val)
        x=int(self.x)
        y=int(self.y)
        print(v,x,y)
        msg="You've clicked on a point : ( %s ,"%v + " %s ,"%x+" %s )\n"%y+"Value：%f "%self.data[v,x,y]
        QMessageBox.information(self, "Click!",msg)
        
    def onpressy(self,event):
        if event.inaxes !=self.axy:
            return
        self.pressevent=None
        self.x=event.xdata
        self.y=event.ydata
        val=self.textboxy.text()
        v=int(val)
        x=int(self.x)
        y=int(self.y)
        print(x,v,y)
        msg="You've clicked on a point : ( %s ,"%x + " %s ,"%v+" %s )\n"%y+"Value：%f "%self.data[x,v,y]
        QMessageBox.information(self, "Click!",msg)
        
    def onpressz(self,event):
        if event.inaxes !=self.axz:
            return
        self.pressevent=None
        self.x=event.xdata
        self.y=event.ydata
        val=self.textboxz.text()
        v=int(val)
        x=int(self.x)
        y=int(self.y)
        print(x,y,v)
        msg="You've clicked on a point : ( %s ,"%x + " %s ,"%y+" %s )\n"%v+"Value：%f "%self.data[x,y,v]
        QMessageBox.information(self, "Click!",msg)
    
    def onrelease(self,event):
        self.pressevent=None
        self.x=event.xdata
        self.y=event.ydata
        print(self.x,self.y)
    
    
    def zoom(self):
        extent = self.axes.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        self.fig.savefig('axeszoom.png', bbox_inches=extent.expanded(1.1, 1.2),dpi=200,transparent=True)
        self.fig.delaxes(self.axes)
        self.zoomin=self.fig.add_subplot(121)
        img = mpimg.imread('axeszoom.png')
        imgplot = self.zoomin.imshow(img)
        self.setMouseTracking(True)
        self.zoomin.set_xlim(150,1650)
        self.zoomin.set_ylim(1750,180)
        #self.zoomin.set_aspect('equal')
        self.zoomin.set_alpha(0)
        self.zoomin.patch.set_alpha(0)
        self.zoomin.set_axis_off()
        print('AA')
        
    def zoomin(self):
        print(self.sliderfig.value())
        z=self.sliderfig.value()
        self.zoomin.set_xlim(self.x-(self.x-150)*(100-z)/100,self.x+(1650-self.x)*(100-z)/100)
        self.zoomin.set_ylim(self.y+(1750-self.y)*(100-z)/100,self.y-(self.y-180)*(100-z)/100)
        #self.zoomin.set_aspect('equal')
        print('aa')
    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices)
        extent = self.axes.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        self.fig.savefig('3Dmodel.png', bbox_inches=extent.expanded(1.1, 1.2),dpi=200,transparent=True)
        extent = self.axx.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        self.fig.savefig('YZ_section.png', bbox_inches=extent.expanded(1.1, 1.2),dpi=200,transparent=True)
        extent = self.axy.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        self.fig.savefig('XZ_section.png', bbox_inches=extent.expanded(1.1, 1.2),dpi=200,transparent=True)
        extent = self.axz.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        self.fig.savefig('XY_section.png', bbox_inches=extent.expanded(1.1, 1.2),dpi=200,transparent=True)
        if path:
            self.canvas.print_figure(path[0], dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
    @jit
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
                   self.data[i,j,k]=self.test[x]
                   
                   if self.test[x]<3:
                       self.color[i,j,k]=0
                   elif self.test[x]>3 and self.test[x]<4:
                       self.color[i,j,k]=1
                   elif self.test[x]>4 and self.test[x]<5:
                       self.color[i,j,k]=2
                   elif self.test[x]>5 and self.test[x]<6:
                       self.color[i,j,k]=3
                   elif self.test[x]>6 and self.test[x]<7:
                       self.color[i,j,k]=4
                   elif self.test[x]>7 and self.test[x]<8:
                       self.color[i,j,k]=5
                   elif self.test[x]>8:
                       self.color[i,j,k]=6
                   x=x+1
                   i=i+1
               k=k+1
            j=j+1        
        print(self.color[40,40,61])
        print(self.test[104221])
        self.on_draw()
    @jit
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)    
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)          
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)
                
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
                self.faces = Poly3DCollection(self.edges,color='k',linewidth=0.5,zorder=1)
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
        
    @jit     
    def coloronly(self,index,r,b,g,a):
        self.canvas.draw()
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
        self.axes.set_alpha(0)
        self.axes.patch.set_alpha(0) 
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
        #self.plot(xsec,ysec,zsec)
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
    @jit    
    def showsection(self,a,b,c):
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
                    rectangle = mpatches.Rectangle((0+i,0+k),1,1,color=(0.5,0.2,0.9,1))
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
