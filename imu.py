# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 17:11:58 2013

@author: -
"""

#
# -*- coding: utf-8 -*-
#
"""
Created on Tue Oct 18 19:10:38 2011

@author: -
"""
import sys
from PyQt4 import QtCore, QtGui, uic
import PyQt4.Qwt5 as Qwt
import serial
import scipy.signal
import numpy as np
import string as st


#
# -*- coding: utf-8 -*-
#
"""
Created on Tue Oct 18 19:10:38 2011

@author: -
"""
import sys
from PyQt4 import QtCore, QtGui, uic
import PyQt4.Qwt5 as Qwt
import serial
import scipy.signal
import numpy as np
import string as st
from neurolab.core import Train, Trainer, TrainStop
import neurolab as nl


class MyGraph(Qwt.QwtPlot):
    def __init__(self,widget):
        Qwt.QwtPlot.__init__(self,widget)
 
         
class MainWindow(QtGui.QDialog):
    def __init__(self):
       self.ardu =serial.Serial('/dev/ttyACM0', 38400)
       QtGui.QDialog.__init__(self)
       uic.loadUi('imu.ui', self)      
       (self.h,self.w)=(self.frame.height(),self.frame.width())
       self.myplot = MyGraph(self.frame)
       self.myplot.resize(self.w,self.h)

       (self.h,self.w)=(self.frame_3.height(),self.frame_3.width())
       self.myplot1 = MyGraph(self.frame_3)
       self.myplot1.resize(self.w,self.h)

       self.t=np.array([])       
       self.ax=np.array([])
       self.ay=np.array([])       
       self.az=np.array([])
       self.wx=np.array([])
       self.wy=np.array([])       
       self.wz=np.array([])
       self.i=1;
            
       self.pl_ax = Qwt.QwtPlotCurve('ax')
       self.pl_ax.attach(self.myplot)             
       self.pl_ax.setPen(QtGui.QPen(QtGui.QColor.red))
       self.pl_ay = Qwt.QwtPlotCurve('ay')
       self.pl_ay.attach(self.myplot)             
       self.pl_ay.setPen(QtGui.QPen(QtGui.QColor.green))
       self.pl_az = Qwt.QwtPlotCurve('az')
       self.pl_az.attach(self.myplot)             
       self.pl_ay.setPen(QtGui.QPen(QtGui.QColor.blue))

       self.pl_wx = Qwt.QwtPlotCurve('ax')
       self.pl_wx.attach(self.myplot1)             
       self.pl_wx.setPen(QtGui.QPen(QtGui.QColor.red))
       self.pl_wy = Qwt.QwtPlotCurve('ay')
       self.pl_wy.attach(self.myplot1)             
       self.pl_wy.setPen(QtGui.QPen(QtGui.QColor.green))
       self.pl_wz = Qwt.QwtPlotCurve('az')
       self.pl_wz.attach(self.myplot1)             
       self.pl_wy.setPen(QtGui.QPen(QtGui.QColor.blue))


       self.timer = QtCore.QTimer()
       self.timer.setInterval(5)
       QtCore.QObject.connect(self.timer,QtCore.SIGNAL('timeout()'),self.ugraph)      
       self.timer.start()

    def ugraph(self):
        s=self.ardu.readline()
        print s        
        [aax,aay,aaz,wwx,wwy,wwz]=s.split(';')
        self.t=np.append(self.t,self.i)
        
        self.ax=np.append(self.ax,st.atof(aax))
        self.ay=np.append(self.ay,st.atof(aay))
        self.az=np.append(self.az,st.atof(aaz))

        self.wx=np.append(self.wx,st.atof(wwx))
        self.wy=np.append(self.wy,st.atof(wwy))
        self.wz=np.append(self.wz,st.atof(wwz))

        self.pl_ax.setData(self.t,self.ax)
        self.pl_ay.setData(self.t,self.ay)
        self.pl_az.setData(self.t,self.az)

        self.pl_wx.setData(self.t,self.wx)
        self.pl_wy.setData(self.t,self.wy)
        self.pl_wz.setData(self.t,self.wz)

        self.i=self.i+1   
        self.myplot.replot()        
        self.myplot1.replot()        


              

app  = QtGui.QApplication(sys.argv)
mw = MainWindow()
mw.show()
app.exec_()