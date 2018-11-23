# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:43:52 2015
@author:
Mechelonic version 0.2
"""
import numpy as np
import os
import re
import matplotlib.animation as animation
import sys
import subprocess
import time
import serial
import serial.tools.list_ports
import bz2
from   thread import start_new_thread
from   matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from   matplotlib.figure import Figure
from   PyQt4.QtGui import * 
from   PyQt4.QtCore import *
#from   keyFile import *
import base64


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #pixmap = QPixmap('D:\Mechlonic\Work\logo (3).png')
#        self.verifyLicense()   # to check the license 
        self.fontSetting()
        self.createdir()     # create job/datalog directory
        self.setWindowTitle('WELDGuru V1.2')  
        self.mainLayout=QVBoxLayout() #set main layout
        self.setLayout(self.mainLayout)
#LOGIN Widget-------------------------loginwid
        self.loginLayout=QGridLayout() #login layout
        self.loginW=QWidget()          #login widget
        self.mainLayout.addWidget(self.loginW)
        self.loginW.setLayout(self.loginLayout)
#Login widget controls        
         
        self.setStyleSheet("background-color:%s"%(self.backgroudColor))
        self.headingL   =  QLabel("   mechelonic   ")
        self.headingL1  =  QLabel("             WELDGuru V1.2   ")
        self.userMode   =  QComboBox()
        self.userNameL  =  QLabel("Username")
        self.passwordL  =  QLabel("Password")
        self.modeL      =  QLabel("Mode")
        
        self.userName   =  QLineEdit("")
        self.password   =  QLineEdit("")
        self.dummy      =  QLabel("")
        self.password.setEchoMode(QLineEdit.Password)   
        self.login      =  QPushButton("Login")
        self.userMode.addItem("Operator")
        self.userMode.addItem("Engineering")
        self.login.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))   
#Login Widget Fonts  
        self.headingL.setFont(self.fontL)        
        self.headingL1.setFont(self.fontHead1)  
        self.userNameL.setFont(self.fontTable)        
        self.passwordL.setFont(self.fontTable)  
        self.userName.setFont(self.fontTable)        
        self.password.setFont(self.fontTable)  
        self.userMode.setFont(self.fontTable)  
        self.modeL.setFont(self.fontTable)  
        self.login.setFont(self.fontTable)  
        
        self.headingL.setStyleSheet('QLabel  {background-color:%s;}'%(self.headingColour))
        self.headingL1.setStyleSheet('QLabel  {background-color:%s;}'%(self.headingColour))
        #self.headingL.setPixmap(pixmap)
#Login Widget controls to layout and manage layout       
        self.loginLayout.addWidget(self.headingL,1,1,1,2)
        self.loginLayout.addWidget(self.headingL1,2,1,1,2)
        self.loginLayout.addWidget(self.userNameL,4,1)
        self.loginLayout.addWidget(self.passwordL,5,1)
        self.loginLayout.addWidget(self.userName,4,2)
        self.loginLayout.addWidget(self.password,5,2)
        self.loginLayout.addWidget(self.userMode,6,2)
        self.loginLayout.addWidget(self.modeL,6,1)
        self.loginLayout.addWidget(self.login,7,2)
        #self.loginLayout.setColumnStretch(1, 1)
        self.loginLayout.setColumnStretch(4, 1)
        self.loginLayout.setColumnStretch(0, 1)
        self.loginLayout.setRowStretch(3, 1)
        self.loginLayout.setRowStretch(8, 1)
        #self.dummy.setFixedSize(100,10)
#Login widget Events       
        self.login.clicked.connect(self.ModeSelection)    
#ENGINEERING Widget------------------------------------------------------------------------engwid
               
        self.engineerLayout=QGridLayout()
        self.engineerW=QTabWidget()
        self.mainLayout.addWidget(self.engineerW)
        self.engineerW.setLayout(self.engineerLayout)
        self.engineerW.setStyleSheet("background-color:%s"%(self.buttonColour))
#Engineering Tab1   
        self.engineerWTab1 = QWidget()
        self.editJoblayout = QGridLayout() 
        self.engineerW.addTab(self.engineerWTab1,"    Engineering Mode    ")
        self.engineerWTab1.setLayout(self.editJoblayout)
        #self.engineerW.setStyleSheet("QLineEdit { border: 1px solid  }")        
        self.engineerW.setStyleSheet("QTabBar::tab {font-size: 8pt; font-family: Arial; font-weight:bold;  background-color:%s;border:1px solid;border-top-left-radius: 4px;border-top-right-radius: 4px;}"%(self.buttonColour)) 
        self.engineerWTab1.setStyleSheet("QLineEdit{border:1px solid}") 
        
#Engineering Tab1 controls
        self.headingE        =  QLabel("                 mechelonic")
        self.headingE1       =  QLabel(" WELDGuru V1.2 ")
        self.modeE           =  QLabel("Engineering Mode")
        self.selectMenulabelE=  QLabel("SelectMenu")
        self.selectMenuE     =  QComboBox()
        self.loadjobLabelE   =  QLabel("Load Jobs From")
        self.selectJobLabelE =  QLabel("Select Job Number")
        self.displayJobE     =  QPushButton("Display Job") 
        self.deleteJobE      =  QPushButton("Delete Job") 
        self.jobNolabel      =  QLabel("Enter Job No")
        self.saveJobE        =  QPushButton("SaveJob to Computer")  
        self.loadFromE       =  QComboBox()
        self.selectJobE      =  QComboBox()
        self.jobNo           =  QLineEdit("")
        self.saveMenu        =  QPushButton("SaveMenu") 
        self.dummy           =  QLabel("  ")        
        self.ftdistatusL     =  QLabel("  COM Status:")
        self.ftdistatus      =  QLabel("")
        self.ftdibaudrate    =  QComboBox()
        self.SentParamter    =  QPushButton("Sent Paramter") 
        self.SentJob         =  QPushButton("Download Job To Timer")
        
        self.doc1_EL            =  QLabel("  Weld Title")
        self.doc2_EL            =  QLabel("  Weld Force")
        self.doc3_EL            =  QLabel("  Top Sheet Material")        
        self.doc4_EL            =  QLabel("  Top Sheet Thickness,mm")        
        self.doc5_EL            =  QLabel("  Bottom Sheet Material")
        self.doc6_EL            =  QLabel("  Bottom Sheet Thickness,mm")        
        self.doc7_EL            =  QLabel("  Upper Electrode Dwg No")        
        self.doc8_EL            =  QLabel("  Lower Electrode Dwg No")   
        self.doc9_EL            =  QLabel("  Force Mode(High or Low)")   
        self.doc10_EL           =  QLabel("  Air Pressure(Top)")   
        self.doc11_EL           =  QLabel("  Air Pressure(Bottom)")           
        self.doc12_EL           =  QLabel("  Remarks")
        
        self.doc1_E             =  QLineEdit("")
        self.doc2_E             =  QLineEdit("")        
        self.doc3_E             =  QLineEdit("")        
        self.doc4_E             =  QLineEdit("")
        self.doc5_E             =  QLineEdit("")        
        self.doc6_E             =  QLineEdit("")        
        self.doc7_E             =  QLineEdit("")        
        self.doc8_E             =  QLineEdit("")
        self.doc9_E             =  QLineEdit("") 
        self.doc10_E            =  QLineEdit("")
        self.doc11_E            =  QLineEdit("")        
        self.doc12_E            =  QTextEdit("")
        
        self.ftdibaudrate.setCurrentIndex(10)        
        self.selectMenuE.addItems('ScheduleJob Counter-Config-Weld'.split())
        self.loadFromE.addItems('Computer Timer'.split())
        self.jobTable = QTableWidget()
        self.jobTable.verticalHeader().setVisible(False)
        self.jobTable.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.jobTable.setStyleSheet("QHeaderView::section { background-color:%s}"
                                    "QTableCornerButton::section {background-color: transparent;}"%(self.buttonColour))
        self.doc12_E.setStyleSheet("QTextEdit{border:1px solid}")        
               
        self.jobTable.setRowCount(16)
        self.jobTable.setColumnCount(3)
        self.jobTable.setHorizontalHeaderLabels(('Parameter','Values','Units'))        
        for cnt in np.arange(16):
           self.jobTable.setRowHeight(cnt,29)
        #self.jobTable.setRowHeight(13,28) # adjusted to fit table in geometry
        self.jobTable.setRowHeight(14,28) # adjusted to fit table in geometry
#Engineering tab1 Fonts  and bg colour       
        self.headingE.setFont(self.fontHead)
        self.headingE1.setFont(self.fontHead1)
        self.jobTable.setFont(self.fontTable)
        self.saveJobE.setFont(self.fontTable)
        self.saveMenu.setFont(self.fontTable)
        self.displayJobE.setFont(self.fontTable)
        self.deleteJobE.setFont(self.fontTable)
        self.SentParamter.setFont(self.fontTable)
        self.SentJob.setFont(self.fontTable)
        self.loadFromE.setFont(self.fontTable)
        self.selectMenuE.setFont(self.fontTable)
        self.selectJobE.setFont(self.fontTable)
        self.ftdistatusL.setFont(self.fontTable)
        self.ftdistatus.setFont(self.fontTable)
        self.loadjobLabelE.setFont(self.fontTable)
        self.selectJobLabelE.setFont(self.fontTable)        
        self.jobNolabel.setFont(self.fontTable)
        self.jobNo.setFont(self.fontTable)                
        
        self.doc1_EL.setFont(self.fontTable)                
        self.doc2_EL.setFont(self.fontTable)                
        self.doc3_EL.setFont(self.fontTable)                
        self.doc4_EL.setFont(self.fontTable)                
        self.doc5_EL.setFont(self.fontTable)                
        self.doc6_EL.setFont(self.fontTable)                
        self.doc7_EL.setFont(self.fontTable)                
        self.doc8_EL.setFont(self.fontTable)                
        self.doc9_EL.setFont(self.fontTable)   
        self.doc10_EL.setFont(self.fontTable)                
        self.doc11_EL.setFont(self.fontTable)   
        self.doc12_EL.setFont(self.fontTable)   
        
        self.doc1_E.setFont(self.fontTable)                
        self.doc2_E.setFont(self.fontTable)                
        self.doc3_E.setFont(self.fontTable)                
        self.doc4_E.setFont(self.fontTable)                
        self.doc5_E.setFont(self.fontTable)                
        self.doc6_E.setFont(self.fontTable)                
        self.doc7_E.setFont(self.fontTable)                
        self.doc8_E.setFont(self.fontTable)                
        self.doc9_E.setFont(self.fontTable)
        self.doc10_E.setFont(self.fontTable)
        self.doc11_E.setFont(self.fontTable)
        self.doc12_E.setFont(self.fontTable)
        
        self.jobTable.horizontalHeader().setFont(self.fontTable)
        self.headingE.setStyleSheet('QLabel {background-color: %s;}'%(self.headingColour))
        self.headingE1.setStyleSheet('QLabel {background-color:%s;}'%(self.headingColour))
        self.saveJobE.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))   
        self.saveMenu.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour)) 
        self.displayJobE.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))   
        self.deleteJobE.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour)) 
        self.SentParamter.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour)) 
        self.SentJob.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))
#Engineering tab1 add controls and layput manage    
        self.selectMenuE.setFixedSize(465,26)         
        self.SentJob.setFixedSize(240,26)
        
        self.selectJobE.setFixedSize(200,26)
        self.loadFromE.setFixedSize(200,26)
        self.jobNo.setFixedSize(200,26)
        self.ftdistatus.setFixedSize(200,26)
        self.ftdistatusL.setFixedSize(200,26)
        
        self.jobTable.setColumnWidth(0,175)
        self.jobTable.setColumnWidth(1,143)    
        self.jobTable.setColumnWidth(2,145) 
        
        self.doc1_E.setFixedSize(240,25) 
        self.doc2_E.setFixedSize(240,25) 
        self.doc3_E.setFixedSize(240,25) 
        self.doc4_E.setFixedSize(240,25) 
        self.doc5_E.setFixedSize(240,25)                 
        self.doc6_E.setFixedSize(240,25) 
        self.doc7_E.setFixedSize(240,25) 
        self.doc8_E.setFixedSize(240,25) 
        self.doc9_E.setFixedSize(240,25) 
        self.doc10_E.setFixedSize(240,25) 
        self.doc11_E.setFixedSize(240,25) 
        self.doc12_E.setFixedSize(240,45) 
        
        self.editJoblayout.addWidget(self.headingE,1,5)
        self.editJoblayout.addWidget(self.headingE1,1,7)
        self.editJoblayout.addWidget(self.dummy,1,4)
        self.editJoblayout.addWidget(self.jobTable,3,5,16,1)
        self.editJoblayout.addWidget(self.loadjobLabelE,2,2)
        self.editJoblayout.addWidget(self.selectMenuE,2,5)
        self.editJoblayout.addWidget(self.loadFromE,2,3)
        self.editJoblayout.addWidget(self.selectJobLabelE,3,2)
        self.editJoblayout.addWidget(self.selectJobE,3,3)
        self.editJoblayout.addWidget(self.displayJobE,4,3)  
        self.editJoblayout.addWidget(self.deleteJobE,5,3) 
        self.editJoblayout.addWidget(self.jobNolabel,15,2)
        self.editJoblayout.addWidget(self.jobNo,15,3)
        self.editJoblayout.addWidget(self.saveJobE,16,3)
        self.editJoblayout.addWidget(self.ftdistatusL,15,6)
        self.editJoblayout.addWidget(self.ftdistatus,15,7)
        self.editJoblayout.addWidget(self.SentJob,16,7,1,1)
        
        self.editJoblayout.addWidget(self.doc1_EL,3,6)
        self.editJoblayout.addWidget(self.doc2_EL,4,6)
        self.editJoblayout.addWidget(self.doc3_EL,5,6)
        self.editJoblayout.addWidget(self.doc4_EL,6,6)
        self.editJoblayout.addWidget(self.doc5_EL,7,6)
        self.editJoblayout.addWidget(self.doc6_EL,8,6)
        self.editJoblayout.addWidget(self.doc7_EL,9,6)
        self.editJoblayout.addWidget(self.doc8_EL,10,6)
        self.editJoblayout.addWidget(self.doc9_EL,11,6)
        self.editJoblayout.addWidget(self.doc10_EL,12,6)
        self.editJoblayout.addWidget(self.doc11_EL,13,6)
        self.editJoblayout.addWidget(self.doc12_EL,14,6)
     
     
        self.editJoblayout.addWidget(self.doc1_E,3,7)
        self.editJoblayout.addWidget(self.doc2_E,4,7)
        self.editJoblayout.addWidget(self.doc3_E,5,7)
        self.editJoblayout.addWidget(self.doc4_E,6,7)
        self.editJoblayout.addWidget(self.doc5_E,7,7)
        self.editJoblayout.addWidget(self.doc6_E,8,7)
        self.editJoblayout.addWidget(self.doc7_E,9,7)
        self.editJoblayout.addWidget(self.doc8_E,10,7)
        self.editJoblayout.addWidget(self.doc9_E,11,7)
        self.editJoblayout.addWidget(self.doc10_E,12,7)
        self.editJoblayout.addWidget(self.doc11_E,13,7)
        self.editJoblayout.addWidget(self.doc12_E,14,7)
        #self.editJoblayout.setColumnStretch(3,1)
#Engineering tab1 Event is       
        self.loadFromE.activated.connect(self.loadFromeventEng)         
        self.saveJobE.clicked.connect(self.SaveToComputereventEng) 
        self.displayJobE.clicked.connect(self.displayJobeventEng)
        self.deleteJobE.clicked.connect(self.deleteJobeventEng)
        self.selectMenuE.activated.connect(self.selectMenueventEng) 
        self.SentJob.clicked.connect(self.sentJobeventEng) 
        self.jobTable.cellChanged.connect(self.saveMenueventEng)        
#Datalog Tab2 ----------------
        self.engineerWTab2 = QWidget()
        self.engineerW.addTab(self.engineerWTab2,"   Datalog   ")
        self.datalog = QGridLayout()   
        self.engineerWTab2.setLayout(self.datalog)
        self.engineerWTab2.setDisabled(1)
#Datalog Controls        
        self.headingD        =  QLabel("mechelonic      ")
        self.headingD1       =  QLabel("WELDGuru V1.2   ")
        self.modeD           =  QLabel("Engineering Mode")
        self.jobNumberL      =  QLabel("Enter Job Number")
        self.WeldNumberL     =  QLabel("Enter Weld Number")
        self.dataLogjobNumber=  QLineEdit("")
        self.xmin            =  QLineEdit("")
        self.xmax            =  QLineEdit("")
        self.ymin            =  QLineEdit("")
        self.ymax            =  QLineEdit("")
        self.minL            =  QLabel("Min")
        self.maxL            =  QLabel("Max")
        self.Xlab            =  QLabel("\t\tX")
        self.Ylab            =  QLabel("\t\tY")        
        self.interval        =  QLineEdit("1")
        self.intervalL       =  QLabel("UpdateInterval(Sec)")
        self.bufferSizeL     =  QLabel("BufferSize")
        self.bufferSize      =  QLineEdit("1024")
        self.apply           =  QPushButton("Apply")
        self.applyInterval   =  QPushButton("Apply")
        self.datalogTimer    =  QPushButton("Start")
        self.liveplotPause   =  QPushButton("Pause")
        self.datalogComputer =  QPushButton("Open")
        self.saveDatalog     =  QPushButton("Save")
        self.updateplot      =  QPushButton("Show plot")
        self.plotoption      =  QComboBox()
        self.plotoption.addItems('WeldCurrent ForceValue'.split())
        self.dataTable       = QTableWidget()
        self.clearLog        =  QPushButton("ClearLog And Buffer")
        self.datalogTimer.setFixedSize(170,20)
        self.liveplotPause.setFixedSize(170,20)
        self.datalogComputer.setFixedSize(170,20)
        self.saveDatalog.setFixedSize(170,20)
        self.clearLog.setFixedSize(163,20)
        self.bufferSize.setFixedSize(100,20)
        self.interval.setFixedSize(100,20)        
        self.bufferSizeL.setFixedSize(70,20)
        self.apply.setFixedSize(100,20)
        self.applyInterval.setFixedSize(100,20)
        self.dataTable.verticalHeader().setVisible(False)
        self.dataTable.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.dataTable.setStyleSheet("QHeaderView::section { background-color:%s}"
                                    "QTableCornerButton::section {background-color: transparent;}"%(self.backgroudColor))
        self.dataTable.setRowCount(1024)
        self.dataTable.setColumnCount(11)
        self.dataTable.setHorizontalHeaderLabels(("Date","Time","JobNumber","WeldNumber","WeldCurr","U-Limit","L-Limit","Forceval","U-Limit","L-limit","PASS/FAIL"))
        for cnt in np.arange(11):
           self.dataTable.setColumnWidth(cnt,77)
        self.fig = Figure((2.0, 2.0), dpi=100,facecolor='white')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.engineerW)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        self.fig.subplots_adjust(left=0.05, right=0.98, top=0.91, bottom=0.15)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
#Datalog fonts ans styke      
        self.datalogTimer.setFont(self.fontTable)        
        self.liveplotPause.setFont(self.fontTable)        
        self.datalogComputer.setFont(self.fontTable)        
        self.saveDatalog.setFont(self.fontTable)        
        self.clearLog.setFont(self.fontTable)        
        self.plotoption.setFont(self.fontTable)        
        self.dataTable.setFont(self.fontTable)        
        self.bufferSizeL.setFont(self.fontTable)        
        self.apply.setFont(self.fontTable)        
        self.bufferSize.setFont(self.fontTable)        
        self.intervalL.setFont(self.fontTable)        
        self.applyInterval.setFont(self.fontTable) 
        self.minL.setFont(self.fontTable) 
        self.maxL.setFont(self.fontTable) 
        self.Xlab.setFont(self.fontTable) 
        self.Xlab.setFont(self.fontTable) 
        self.Ylab.setFont(self.fontTable) 
        self.xmin.setFont(self.fontTable) 
        self.xmax.setFont(self.fontTable)  
        self.ymin.setFont(self.fontTable) 
        self.ymax.setFont(self.fontTable)  
        self.dataTable.horizontalHeader().setFont(self.fontTable)
        self.datalogTimer.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.datalogComputer.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))          
        self.saveDatalog.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.updateplot.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.clearLog.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.liveplotPause.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
#Datalog Layout        
        self.datalog.addWidget(self.datalogTimer,1,1)
        self.datalog.addWidget(self.liveplotPause,1,2)
        self.datalog.addWidget(self.datalogComputer,1,3)
        self.datalog.addWidget(self.saveDatalog,1,4)
        self.datalog.addWidget(self.clearLog,1,5)
        self.datalog.addWidget(self.plotoption,11,1,1,8) 
        self.datalog.addWidget(self.dataTable,2,1,8,5)
        self.datalog.addWidget(self.bufferSizeL,2,6)
        self.datalog.addWidget(self.bufferSize,2,7)
        self.datalog.addWidget(self.apply,2,8)
        self.datalog.addWidget(self.intervalL,3,6)        
        self.datalog.addWidget(self.interval,3,7) 
        self.datalog.addWidget(self.applyInterval,3,8)
        self.datalog.addWidget(self.minL,7,7) 
        self.datalog.addWidget(self.maxL,7,8) 
        self.datalog.addWidget(self.Xlab,8,6) 
        self.datalog.addWidget(self.Ylab,9,6) 
        self.datalog.addWidget(self.xmin,8,7)
        self.datalog.addWidget(self.xmax,8,8)
        self.datalog.addWidget(self.ymin,9,7)
        self.datalog.addWidget(self.ymax,9,8)
        self.datalog.addWidget(self.canvas,12,1,1,8)
        self.datalog.setRowStretch(6, 1)
#Datalog Events
        self.apply.clicked.connect(self.applyEvent)
        self.applyInterval.clicked.connect(self.applyIntervalevent)
        self.clearLog.clicked.connect(self.clearDatalog)
        self.liveplotPause.clicked.connect(self.pausePlotevent)
        self.datalogTimer.clicked.connect(self.startDatalogevent)
        self.saveDatalog.clicked.connect(self.saveDatalogevent)
        self.datalogComputer.clicked.connect(self.datalogComputerevent)
#Setting Tab        
        self.engineerWTab3 = QWidget()
        self.engineerW.addTab(self.engineerWTab3,"  Setting  ")
        self.setting = QGridLayout()   
        self.engineerWTab3.setLayout(self.setting)
        
        self.modeOpL       =  QLabel("OperatorMode")
        self.userNameOpL   =  QLabel("UserName")
        self.passwordOpL   =  QLabel("Password")
        self.repasswordOpL =  QLabel("Retype Password")
        self.userNameOp    =  QLineEdit("")
        self.passwordOp    =  QLineEdit("")
        self.repasswordOp  =  QLineEdit("")
        self.updateOp      =  QPushButton("Update")
        self.passwordOp.setEchoMode(QLineEdit.Password)   
        self.repasswordOp.setEchoMode(QLineEdit.Password) 
        self.modeEgL       =  QLabel("EngineeringMode")
        self.userNameEgL   =  QLabel("UserName")
        self.passwordEgL   =  QLabel("Password")
        self.repasswordEgL =  QLabel("Retype Password")
        self.userNameEg    =  QLineEdit("")
        self.passwordEg    =  QLineEdit("")
        self.repasswordEg  =  QLineEdit("")
        self.updateEg      =  QPushButton("Update")
        self.passwordEg.setEchoMode(QLineEdit.Password)   
        self.repasswordEg.setEchoMode(QLineEdit.Password) 
#setting tab fonts and style
        self.modeOpL.setFont(self.fontTable)
        self.userNameOpL.setFont(self.fontTable)
        self.passwordOpL.setFont(self.fontTable)
        self.repasswordOpL.setFont(self.fontTable)
        self.updateOp.setFont(self.fontTable) 
        self.userNameOp.setFont(self.fontTable)
        self.passwordOp.setFont(self.fontTable)
        self.userNameOpL.setFont(self.fontTable)
        self.repasswordOp.setFont(self.fontTable)
        self.repasswordOpL.setFont(self.fontTable)
        self.modeEgL.setFont(self.fontTable) 
        self.userNameEgL.setFont(self.fontTable) 
        self.passwordEgL.setFont(self.fontTable) 
        self.repasswordEgL.setFont(self.fontTable) 
        self.userNameEg.setFont(self.fontTable) 
        self.passwordEg.setFont(self.fontTable) 
        self.passwordEgL.setFont(self.fontTable) 
        self.repasswordEg.setFont(self.fontTable) 
        self.updateEg.setFont(self.fontTable) 
        
#layout       
        self.setting.addWidget(self.modeOpL,0,1)
        self.setting.addWidget(self.userNameOpL,1,0)
        self.setting.addWidget(self.passwordOpL,2,0)
        self.setting.addWidget(self.repasswordOpL,3,0)
        self.setting.addWidget(self.userNameOp,1,1)
        self.setting.addWidget(self.passwordOp,2,1)
        self.setting.addWidget(self.repasswordOp,3,1)
        self.setting.addWidget(self.updateOp,4,1)
        self.setting.addWidget(self.modeEgL,5,1)
        self.setting.addWidget(self.userNameEgL,6,0)
        self.setting.addWidget(self.passwordEgL,7,0)
        self.setting.addWidget(self.repasswordEgL,8,0)
        self.setting.addWidget(self.userNameEg,6,1)
        self.setting.addWidget(self.passwordEg,7,1)
        self.setting.addWidget(self.repasswordEg,8,1)
        self.setting.addWidget(self.updateEg,9,1)
        
        self.setting.setRowStretch(10, 1)
        self.setting.setColumnStretch(2, 1)
        self.updateOp.clicked.connect(self.updatePasswordOpevent)
        self.updateEg.clicked.connect(self.updatePasswordEgevent)        
        
#OPERATOR WIDGET--------------------------------------- opwid   
        self.operatorLayout=QGridLayout()
        self.operatorW=QWidget()
        self.mainLayout.addWidget(self.operatorW)
        self.operatorW.setLayout(self.operatorLayout)
        self.operatorW.setStyleSheet("background-color:%s;"%(self.backgroudColor))
        self.updateEg.setStyleSheet("background-color:%s;"%(self.buttonColour))
        self.updateOp.setStyleSheet("background-color:%s;"%(self.buttonColour))
#Operator Widgets controls
        self.heading         =  QLabel("                  mechelonic")
        self.heading1        =  QLabel(" WELDGuru V1.2 ")
        self.selectMenuOp    =  QComboBox()
        self.mode            =  QLabel("Operator Mode")
        self.loadjobLabel    =  QLabel("Load Jobs From")
        self.loadFrom        =  QComboBox()
        self.selectJobLabel  =  QLabel("Select Job Number")
        self.selectJob       =  QComboBox()
        self.loadFrom.addItems('Computer Timer'.split())
        self.displayJob      =  QPushButton("Display Job")  
        #self.dummyop         =  QLabel("    ")
        self.download        =  QPushButton("Download This Job to Timer")  
        self.run             =  QPushButton("Run")  
        self.ftdistatusOpL   =  QLabel("  COM Status:")
        self.ftdistatusOp    =  QLabel("")
        self.selectMenuOp.addItems('ScheduleJob Counter-Config-Weld'.split())
        
        self.doc1_OPL            =  QLabel("  Weld Title")
        self.doc2_OPL            =  QLabel("  Weld Force")
        self.doc3_OPL            =  QLabel("  Top Sheet Material")        
        self.doc4_OPL            =  QLabel("  Top Sheet Thickness,mm")        
        self.doc5_OPL            =  QLabel("  Bottom Sheet Material")
        self.doc6_OPL            =  QLabel("  Bottom Sheet Thickness,mm")        
        self.doc7_OPL            =  QLabel("  Upper Electrode Dwg No")        
        self.doc8_OPL            =  QLabel("  Lower Electrode Dwg No")        
        self.doc9_OPL            =  QLabel("  Force Mode(High or Low)")   
        self.doc10_OPL           =  QLabel("  Air Pressure(Top)")   
        self.doc11_OPL           =  QLabel("  Air Pressure(Bottom)")      
        self.doc12_OPL           =  QLabel("  Remarks")
        
        self.doc1_OP             =  QLineEdit("")
        self.doc2_OP             =  QLineEdit("")
        self.doc3_OP             =  QLineEdit("")        
        self.doc4_OP             =  QLineEdit("")        
        self.doc5_OP             =  QLineEdit("")
        self.doc6_OP             =  QLineEdit("")        
        self.doc7_OP             =  QLineEdit("")        
        self.doc8_OP             =  QLineEdit("")        
        self.doc9_OP             =  QLineEdit("")        
        self.doc10_OP            =  QLineEdit("")        
        self.doc11_OP            =  QLineEdit("")        
        self.doc12_OP            =  QTextEdit("")
        
        self.doc1_OP.setReadOnly(True)
        self.doc2_OP.setReadOnly(True)
        self.doc3_OP.setReadOnly(True)
        self.doc4_OP.setReadOnly(True)
        self.doc5_OP.setReadOnly(True)
        self.doc6_OP.setReadOnly(True)
        self.doc7_OP.setReadOnly(True)
        self.doc8_OP.setReadOnly(True)
        self.doc9_OP.setReadOnly(True)        
        self.doc10_OP.setReadOnly(True)        
        self.doc11_OP.setReadOnly(True)        
        self.doc12_OP.setReadOnly(True)        
        
        self.selectMenuOp.setFixedSize(510,26) 
        self.loadFrom.setFixedSize(210,26)  
        self.selectJob.setFixedSize(210,26)  
        self.displayJob.setFixedSize(210,26)          
        
        self.doc1_OP.setFixedSize(240,26)
        self.doc2_OP.setFixedSize(240,26)
        self.doc3_OP.setFixedSize(240,26)
        self.doc4_OP.setFixedSize(240,26)
        self.doc5_OP.setFixedSize(240,26)
        self.doc6_OP.setFixedSize(240,26)
        self.doc7_OP.setFixedSize(240,26)
        self.doc8_OP.setFixedSize(240,26)
        self.doc9_OP.setFixedSize(240,26)
        self.doc10_OP.setFixedSize(240,26)
        self.doc11_OP.setFixedSize(240,26)
        self.doc12_OP.setFixedSize(240,50)       
        
        self.download.setFixedSize(240,26)  
        self.ftdistatusOp.setFixedSize(200,26) 
        
        #self.heading1.setFixedSize(200,20) 
        self.operatorJob = QTableWidget()
        self.operatorJob.verticalHeader().setVisible(False)
        self.operatorJob.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.operatorJob.setStyleSheet("QHeaderView::section { background-color:%s}"
                                    "QTableCornerButton::section {background-color: transparent;}"%(self.buttonColour))
        self.operatorJob.setRowCount(16)
        self.operatorJob.setColumnCount(3)
        self.operatorJob.setColumnWidth(0,175)
        self.operatorJob.setColumnWidth(1,164)
        self.operatorJob.setColumnWidth(2,165)
        for cnt in np.arange(16):
           self.operatorJob.setRowHeight(cnt,29)
        self.operatorJob.setRowHeight(13,31)#to adjust the layout   
        self.operatorJob.setRowHeight(12,31)#to adjust the layout
        self.operatorJob.setRowHeight(11,31)#to adjust the layout
        
        
        self.operatorJob.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.operatorJob.setHorizontalHeaderLabels(('Parameter','Values','Units'))        
#operator  Fonts        
        self.heading.setFont(self.fontHead)
        self.heading1.setFont(self.fontHead1)
        self.loadFrom.setFont(self.fontTable)
        self.selectJobLabel.setFont(self.fontTable)
        self.selectJob.setFont(self.fontTable)
        self.displayJob.setFont(self.fontTable)
        self.operatorJob.setFont(self.fontTable)
        self.selectMenuOp.setFont(self.fontTable)
        self.download.setFont(self.fontTable)
        self.ftdistatusOpL.setFont(self.fontTable)
        self.ftdistatusOp.setFont(self.fontTable)
        self.loadjobLabel.setFont(self.fontTable)
        self.operatorJob.horizontalHeader().setFont(self.fontTable)      

        self.doc1_OPL.setFont(self.fontTable)
        self.doc2_OPL.setFont(self.fontTable)
        self.doc3_OPL.setFont(self.fontTable)
        self.doc4_OPL.setFont(self.fontTable)
        self.doc5_OPL.setFont(self.fontTable)
        self.doc6_OPL.setFont(self.fontTable)
        self.doc7_OPL.setFont(self.fontTable)
        self.doc8_OPL.setFont(self.fontTable)
        self.doc9_OPL.setFont(self.fontTable)
        self.doc10_OPL.setFont(self.fontTable)
        self.doc11_OPL.setFont(self.fontTable)
        self.doc12_OPL.setFont(self.fontTable)
        
        self.doc1_OP.setFont(self.fontTable)
        self.doc2_OP.setFont(self.fontTable)
        self.doc3_OP.setFont(self.fontTable)
        self.doc4_OP.setFont(self.fontTable)
        self.doc5_OP.setFont(self.fontTable)
        self.doc6_OP.setFont(self.fontTable)
        self.doc7_OP.setFont(self.fontTable)
        self.doc8_OP.setFont(self.fontTable)
        self.doc9_OP.setFont(self.fontTable)
        self.doc10_OP.setFont(self.fontTable)
        self.doc11_OP.setFont(self.fontTable)
        self.doc12_OP.setFont(self.fontTable)
       
        self.download.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.displayJob.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.run.setStyleSheet('QPushButton {background-color:%s;}'%(self.buttonColour))  
        self.heading.setStyleSheet('QLabel {background-color:%s;}'%(self.headingColour))  
        self.heading1.setStyleSheet('QLabel {background-color:%s;}'%(self.headingColour))  
#operator  adding controls to layout and Layout management     
        self.operatorLayout.addWidget(self.heading,1,4)        
        self.operatorLayout.addWidget(self.heading1,1,9)
        self.operatorLayout.addWidget(self.loadjobLabel,2,1)
        self.operatorLayout.addWidget(self.loadFrom,2,2)
        self.operatorLayout.addWidget(self.selectJobLabel,3,1)
        self.operatorLayout.addWidget(self.selectJob,3,2)
        
        self.operatorLayout.addWidget(self.displayJob,4,2)
        self.operatorLayout.addWidget(self.operatorJob,3,4,15,1)
        self.operatorLayout.addWidget(self.selectMenuOp,2,4)
        self.operatorLayout.addWidget(self.download,16,9)
        self.operatorLayout.addWidget(self.ftdistatusOpL,15,8)
        self.operatorLayout.addWidget(self.ftdistatusOp,15,9)
        
        self.operatorLayout.addWidget(self.doc1_OPL,3,8)
        self.operatorLayout.addWidget(self.doc2_OPL,4,8)
        self.operatorLayout.addWidget(self.doc3_OPL,5,8)
        self.operatorLayout.addWidget(self.doc4_OPL,6,8)
        self.operatorLayout.addWidget(self.doc5_OPL,7,8)
        self.operatorLayout.addWidget(self.doc6_OPL,8,8)
        self.operatorLayout.addWidget(self.doc7_OPL,9,8)
        self.operatorLayout.addWidget(self.doc8_OPL,10,8)
        self.operatorLayout.addWidget(self.doc9_OPL,11,8)
        self.operatorLayout.addWidget(self.doc10_OPL,12,8)
        self.operatorLayout.addWidget(self.doc11_OPL,13,8)
        self.operatorLayout.addWidget(self.doc12_OPL,14,8)               
               
        self.operatorLayout.addWidget(self.doc1_OP,3,9)
        self.operatorLayout.addWidget(self.doc2_OP,4,9)
        self.operatorLayout.addWidget(self.doc3_OP,5,9)
        self.operatorLayout.addWidget(self.doc4_OP,6,9)
        self.operatorLayout.addWidget(self.doc5_OP,7,9)
        self.operatorLayout.addWidget(self.doc6_OP,8,9)
        self.operatorLayout.addWidget(self.doc7_OP,9,9)
        self.operatorLayout.addWidget(self.doc8_OP,10,9)
        self.operatorLayout.addWidget(self.doc9_OP,11,9)
        self.operatorLayout.addWidget(self.doc10_OP,12,9)
        self.operatorLayout.addWidget(self.doc11_OP,13,9)
        self.operatorLayout.addWidget(self.doc12_OP,14,9)     
        #self.operatorLayout.setColumnStretch(3, 0)
#operator event
        self.loadFrom.activated.connect(self.loadFromevent)         
        self.displayJob.clicked.connect(self.displayJobevent) 
        self.download.clicked.connect(self.downloadJobtevent) 
        self.selectMenuOp.activated.connect(self.selectMenuOpevent) 
#Main widgets geometry--GLOBAL VARIABLES---------------------globalvar
         #self.isFloat()
        self.userUpdate = 1
        self.ser = None
        self.com = 1
        self.t1 = 0
        self.t2 = 0
        self.wait = 1
        self.sentcnt = 0
        self.buffer = 1024        
        self.validData =  0    #receive data is valied or not
        self.packetLength = 9  #header + weldcurr,min,max,force volt,min,max+footer
        self.packetCount = 0   #counts no of packets received
        self.paramCount = 0    #counts the parameters received inside a packets      
        self.pausePlot = 0     #to pause ploting
        self.job = 0           #select receive job or datalog(weld curr or force volt)    
        self.globalPause = 1   #pause datalog  update
        self.read = 1          #to receive any data from FTDI     
        self.validJob = 0      #to check received job is valid
        #to display job / datalog on Gui
        self.dataList = np.zeros((self.buffer,self.packetLength),dtype = np.uint8)
        self.jobList = np.ma.masked_array(np.zeros(25,dtype=np.float),mask = True) #old 24
        self.docList = np.chararray(12,1000)
        #command /data pakcter sent to contoller-command packet to tell controller receive/transmit                
        self.commandPacket = np.zeros(5,dtype =np.uint8)        
        self.dataPacket= np.zeros(32,dtype =np.uint16) #header +job number + 24+footer 
        #receiveJob and Log receives data from controller
        #self.receiveJob = np.zeros(26,dtype =np.uint8) ##header+24+footer       
        self.receiveJob=np.ma.masked_array(np.zeros(27,dtype=np.uint8),mask = True)
        self.receiveLog = np.zeros((self.buffer,self.packetLength),dtype=np.uint8)
        self.dat = ['']*self.buffer
        self.tim = ['']*self.buffer
        self.headername = 0xAA
        self.footername = 0xBB
        #self.globalList = ["SqueezeDelay","Squeeze","Forge","CurrentRef","Upslope","Weld1","Heat1","Cool1","Weld2","Heat2","Pulses","Cool2","Hold","Off","Mode","CountUpto","Continue","FactoryDefault","CurrentCheck","RemoteTrim","BeatMode","2Hand","Frequency","WELD"]
        self.connectftdi()        
        self.t1 = start_new_thread(self.readftdi,(1,))   
        #for the plot animation to work the widget which contain the plot canvas need to show first
        #this gives user warning 
        self.loadFromeventEng()
        self.loadFromevent()
        self.selectMenuOpevent()
        self.selectMenueventEng()        
        
        self.engineerW.setCurrentIndex(1)
        self.loginW.setVisible(0)
        self.engineerW.setVisible(1)
        self.operatorW.setVisible(0)
        ani=animation.FuncAnimation(self.fig,self.updatePlot,interval=1000)
        self.show()
        self.close()
        #---login widget is shown first
        self.engineerW.setCurrentIndex(0)
        self.loginW.setVisible(1)
        self.engineerW.setVisible(0)
        self.operatorW.setVisible(0)
        
        self.setGeometry(40,40,1292, 605)
        #self.setMaximumSize(1160+100,580)
        #self.setMinimumSize(1160+100,580)
        self.setFixedSize(1292,605)
        self.show()
#main WIdget Events
    def ModeSelection(self): 
        if(self.userMode.currentText() == "Engineering"):
            f=open(self.pdir+"\AuthEgU","rb")
            self.usernameRead = bz2.decompress(f.read())
            f.close()            
            f=open(self.pdir+"\AuthEgP","rb")           
            self.passwordRead = bz2.decompress(f.read())
            f.close()
            if((str(self.userName.text()) == self.usernameRead and str(self.password.text()) == self.passwordRead and str(self.userName.text()) != "" and str(self.password.text()) != ""  ) or (str(self.userName.text()) == "root" and str(self.password.text()) == "root")) :
                self.engineerW.setVisible(1)
                self.loginW.setVisible(0)
                self.operatorW.setVisible(0)
            else:
                self.result = QMessageBox.question(self, 'Message', "Authentication error", QMessageBox.Close)
        else:    
            f=open(self.pdir+"\AuthOpU","rb")
            self.usernameRead = bz2.decompress(f.read())
            f.close()            
            f=open(self.pdir+"\AuthOpP","rb")            
            self.passwordRead = bz2.decompress(f.read())
            f.close()
            if((str(self.userName.text()) == self.usernameRead and str(self.password.text()) == self.passwordRead and  str(self.userName.text()) != "" and str(self.password.text()) != "") or (str(self.userName.text()) == "root" and str(self.password.text()) == "root")) :
                self.engineerW.setVisible(0)
                self.loginW.setVisible(0)
                self.operatorW.setVisible(1)
            else:
                self.result = QMessageBox.question(self, 'Message', "Authentication error", QMessageBox.Close)
           
#define functions called in GUI load        
    def fontSetting(self):
        self.backgroudColor = "rgb(210, 255, 200)"
        self.buttonColour   = "rgb(220, 255, 190)" 
        self.headingColour  = "rgb(140, 190, 92)"
        self.fontL = QFont('impact')
        self.fontL.setBold(True)
        self.fontL.setPointSize(40)
        
        self.fontHead = QFont('impact')
        self.fontHead.setBold(True)
        self.fontHead.setPointSize(30)
        self.fontHead1 = QFont('Arial')
        self.fontHead1.setPointSize(15)
        self.fontHead1.setItalic(True)
        self.fontHead1.setBold(True)
        
        self.fontTable= QFont('Arial')
        self.fontTable.setPointSize(8)
        self.fontTable.setBold(True)
        
#Creatae directory for saving jobs and saving datalog     
    def createdir(self):
        self.printdir = os.getcwd()+"\print"
        if(os.path.isdir(self.printdir) == False):
             os.mkdir(self.printdir)
        self.cdir = os.getcwd()+"\jobs"
        if(os.path.isdir(self.cdir) == False):
             os.mkdir(self.cdir)
        self.ddir = os.getcwd()+"\dataLog"
        if(os.path.isdir(self.ddir) == False):
             os.mkdir(self.ddir)
        self.pdir = os.getcwd()+"\Auth"
        if(os.path.isdir(self.pdir) == False):
             os.mkdir(self.pdir)
        if not(os.path.isfile(self.pdir+"\AuthOpU")):             
             f=open(self.pdir+"\AuthOpU","wb")
             f.close()
        if not(os.path.isfile(self.pdir+"\AuthOpP")):             
             f=open(self.pdir+"\AuthOpP","wb")
             f.close()     
        if not(os.path.isfile(self.pdir+"\AuthEgU")):                  
             f=open(self.pdir+"\AuthEgU","wb")
             f.close()
        if not(os.path.isfile(self.pdir+"\AuthEgP")):                  
             f=open(self.pdir+"\AuthEgP","wb")
             f.close()     
           
#OPERATOR TAB EVENTS---------------------------------------------------------opfunc 
    def loadFromevent(self):#disply all jobssaved in computer
        if(str(self.loadFrom.currentText()) == 'Computer'):
            self.selectJob.clear()
            for f in os.listdir(self.cdir):
                jobNumber = re.findall(r'\d+', f)
                self.selectJob.addItems(jobNumber)
        else:
             self.selectJob.clear()
             for f in np.arange(1,9):
                 self.selectJob.addItems(str(f))
           
    def displayJobevent(self): #disply all job paramters    
          if(str(self.loadFrom.currentText()) == 'Computer'):
             self.jobfile = self.cdir+'\job'+str(self.selectJob.currentText())+'.npy' 
             if(os.path.isfile(self.jobfile)):                          
                   self.jobList[:] = np.load(self.jobfile)[:25]
                   self.docList[:] = np.load(self.jobfile)[25:25+12] 
                   self.doc1_OP.setText(self.docList[0])
                   self.doc2_OP.setText(self.docList[1])
                   self.doc3_OP.setText(self.docList[2])
                   self.doc4_OP.setText(self.docList[3])
                   self.doc5_OP.setText(self.docList[4])
                   self.doc6_OP.setText(self.docList[5])
                   self.doc7_OP.setText(self.docList[6])
                   self.doc8_OP.setText(self.docList[7])
                   self.doc9_OP.setText(self.docList[8])
                   self.doc10_OP.setText(self.docList[9])
                   self.doc11_OP.setText(self.docList[10])
                   self.doc12_OP.setPlainText(self.docList[11])  
             else:    
                   self.jobList[:].mask = True            
             if(any(self.jobList.mask==1)):
                    self.message(3) # error in download    
          else:           
                self.jobList[:].mask = True                
                self.commandPacket[0] = self.headername
                self.commandPacket[1] = 0xF1
                self.commandPacket[2] = int(self.selectJob.currentText())
                self.commandPacket[3] = 0x00
                self.commandPacket[4] = self.footername
                self.writeFtdi(0,self.commandPacket)              
                self.job = 1
                time.sleep(0.2)#wait 200ms assuming job is received in 200 ms   
                self.jobList[:2] = self.receiveJob[:2]
                self.jobList[2] = self.receiveJob[2] * 256 + self.receiveJob[3]
                if(all(self.receiveJob[4:6].mask == False)):                
                    self.jobList[3] = float(str(self.receiveJob[5])+"."+str(self.receiveJob[4]))
                self.jobList[4:16] = self.receiveJob[6:18]
                self.jobList[16] = self.receiveJob[18] * 256 + self.receiveJob[19]
                self.jobList[17:25] = self.receiveJob[20:28]
                self.message(99)        #check com error        
                self.doc1_OP.setText("")
                self.doc2_OP.setText("")
                self.doc3_OP.setText("")
                self.doc4_OP.setText("")
                self.doc5_OP.setText("")
                self.doc6_OP.setText("")
                self.doc7_OP.setText("")
                self.doc8_OP.setText("")
                self.doc9_OP.setText("")
                self.doc10_OP.setText("")
                self.doc11_OP.setText("")
                self.doc12_OP.setPlainText("") 
                if(any(self.jobList.mask==1) and self.com == 1):
                    self.message(3) # error in download       
         
          if(str(self.selectMenuOp.currentText()) == 'ScheduleJob'):
              for cnt in np.arange(16):#disply the first tab 
                  if(cnt == 3 and self.jobList[cnt:cnt+1].mask == False):        
                      self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(self.jobList[cnt])))
                  elif(self.jobList[cnt:cnt+1].mask == False):        
                      self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt]))))
                  self.operatorJob.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
          else:
              for cnt in np.arange(0,2):#disply the first tab 
                  if(self.jobList[cnt+16:cnt+17].mask == False):        
                      self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt+16]))))
                  self.operatorJob.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
              for cnt in np.arange(0,6):#disply the first tab 
                  if(self.jobList[cnt+18:cnt+19].mask == False):        
                      self.operatorJob.setItem(cnt+3,1, QTableWidgetItem(str(int(self.jobList[cnt+18]))))
                      self.operatorJob.item(cnt+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

              if(self.jobList[24:25].mask == False):        
                  self.operatorJob.setItem(10,1, QTableWidgetItem(str(int(self.jobList[24]))))    
              self.operatorJob.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
              
    def selectMenuOpevent(self):
        for cnt in np.arange(25):
            self.operatorJob.setItem(cnt,0, QTableWidgetItem(''))
            self.operatorJob.setItem(cnt,2, QTableWidgetItem('')) 
            self.operatorJob.setItem(cnt,1, QTableWidgetItem(''))
        if(str(self.selectMenuOp.currentText()) == 'ScheduleJob'):
            shedule = ["SqueezeDelay (0 - 999)","Squeeze (0 - 99)","Forge (0 - 4999)","CurrentRef (00.0 - 99.9)","CurrentTol (5 - 15)","Upslope (0 - 99)","Weld1 (0 - 99)","Heat1 (0 - 99)","Cool1 (0 - 99)","Weld2 (0 - 99)","Heat2 (0 - 99)","Pulses (0 - 99)","Cool2 (0 - 99)","Hold (0 - 99)","Off (0 - 99)","REPEAT Mode (Enable/Disable)"]
            units = ["Cycles","Cycles","mSec","% of FullScale","% Tolerance", "Cycles","Cycles","%","Cycles","Cycles","%","Cycles","Cycles","Cycles","Cycles","0=Disable,1=Enable"]        
            
            for cnt in np.arange(16):#disply the first tab 
                 self.operatorJob.setItem(cnt,0, QTableWidgetItem(shedule[cnt]))
                 self.operatorJob.setItem(cnt,2, QTableWidgetItem(units[cnt]))
                 self.operatorJob.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                 self.operatorJob.item(cnt,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)                
                 if(cnt == 3 and self.jobList[cnt:cnt+1].mask == False):         
                     self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(self.jobList[cnt])))
                 elif(self.jobList[cnt:cnt+1].mask == False):        
                      self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt]))))
                 self.operatorJob.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        else:
             counter = ["CountUpto(0-9999)","At CountEnd"]
             units =["No of Welds ","0=Continue,1=Stop"]
             for cnt in np.arange(0,2):#disply the first tab 
                  self.operatorJob.setItem(cnt,0, QTableWidgetItem(counter[cnt]))
                  self.operatorJob.setItem(cnt,2, QTableWidgetItem(units[cnt]))
                  if (self.jobList[cnt+16:cnt+17].mask == False):
                      self.operatorJob.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt+16]))))
                  self.operatorJob.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                  self.operatorJob.item(cnt,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
         
             Configure = ["FactoryDefault","CurrentCheck","RemoteTrim","BeatMode","2Hand","Frequency"]
             units = ["0=No,1=Yes","0=Disable,1=Enable","0=Disable,1=Enable","0=Disable,1=Enable","0=Disable,1=Enable","0=50Hz,1=60Hz"]
             for cnt in np.arange(0,6):
                 self.operatorJob.setItem(cnt+3,0, QTableWidgetItem(Configure[cnt]))
                 self.operatorJob.setItem(cnt+3,2, QTableWidgetItem(units[cnt]))
                 if (self.jobList[cnt+18:cnt+19].mask == False):
                     self.operatorJob.setItem(cnt+3,1, QTableWidgetItem(str(int(self.jobList[cnt+18]))))
                 self.operatorJob.item(cnt+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                 self.operatorJob.item(cnt+3,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
             
             self.operatorJob.setItem(10,0, QTableWidgetItem("Software Weld Control"))  
             self.operatorJob.setItem(10,2, QTableWidgetItem("0=Weld Disable,1=Weld Enable"))
             if (self.jobList[24:25].mask == False):
                 self.operatorJob.setItem(10,1, QTableWidgetItem(str(int(self.jobList[24])))) 
             self.operatorJob.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
             self.operatorJob.item(10,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
   
    def downloadJobtevent(self): #downloadjobtotimer
       if(any(self.jobList.mask==1) or str(self.selectJob.currentText()).isdigit()==False):
            self.message(2) # error in job list/jobnumber              
       else:
            self.jobnumber  =  int(self.selectJobE.currentText())
            self.commandPacket[0] = self.headername
            self.commandPacket[1] = 0xF0
            self.commandPacket[2] = 0x00
            self.commandPacket[3] = 0x00
            self.commandPacket[4] = self.footername
            self.writeFtdi(0,self.commandPacket)              
            self.dataPacket[0]    = self.headername
            self.dataPacket[1]    = self.jobnumber
            self.dataPacket[2]    = (int(self.jobList[0]) & 0xFF00)>>8  #Sq delay msb
            self.dataPacket[3]    = (int(self.jobList[0]) & 0xFF)       #Sq delay lsb
            self.dataPacket[4]    = self.jobList[1]
            self.dataPacket[5]    = (int(self.jobList[2]) & 0xFF00)>>8  #forge lsb
            self.dataPacket[6]    = (int(self.jobList[2]) & 0xFF)       #forge Msb     
            self.dataPacket[7]    = str(self.jobList[3]).split(".")[1]  #current ref decimal
            self.dataPacket[8]    = str(self.jobList[3]).split(".")[0]  #current ref int
            self.dataPacket[9:21] = self.jobList[4:16]  
            self.dataPacket[21]   = (int(self.jobList[16]) & 0xFF00)>>8  #count upto lsb
            self.dataPacket[22]   = (int(self.jobList[16]) & 0xFF)       #count Msb
            self.dataPacket[23:31]= self.jobList[17:25]       
            self.dataPacket[-1:]  = self.footername
            self.writeFtdi(1,self.dataPacket)           
            self.message(0)    
        
#ENGINEERING TAB EVENts-----------------------------------------------------------------------------engfunc
    def selectMenueventEng(self):
        self.userUpdate = 0
        for cnt in np.arange(24):
            self.jobTable.setItem(cnt,0, QTableWidgetItem(''))
            self.jobTable.setItem(cnt,2, QTableWidgetItem('')) 
            self.jobTable.setItem(cnt,1, QTableWidgetItem(''))
        if(str(self.selectMenuE.currentText()) == 'ScheduleJob'):    
            self.shedule = ["SqueezeDelay (0 - 999)","Squeeze (0 - 99)","Forge (0 - 4999)","CurrentRef (00.0 - 99.9)","CurrentTol (5 - 15)","Upslope (0 - 99)","Weld1 (0 - 99)","Heat1 (0 - 99)","Cool1 (0 - 99)","Weld2 (0 - 99)","Heat2 (0 - 99)","Pulses (0 - 99)","Cool2 (0 - 99)","Hold (0 - 99)","Off (0 - 99)","REPEAT Mode (Enable/Disable)"]
            self.units = ["Cycles","Cycles","mSec","% of FullScale","% Tolerance", "Cycles","Cycles","%","Cycles","Cycles","%","Cycles","Cycles","Cycles","Cycles","0=Disable,1=Enable"]                
            self.jobTable.setHorizontalHeaderLabels(('Parameter','Values','Units'))        
            for cnt in np.arange(16):
                self.jobTable.setItem(cnt,0, QTableWidgetItem(self.shedule[cnt])) 
                self.jobTable.item(cnt,0).setFlags(Qt.ItemIsEnabled)
                self.jobTable.setItem(cnt,2, QTableWidgetItem(self.units[cnt])) 
                self.jobTable.item(cnt,2).setFlags(Qt.ItemIsEnabled)
                if(cnt == 3 and self.jobList[cnt:cnt+1].mask == False):         
                     self.jobTable.setItem(cnt,1, QTableWidgetItem(str(self.jobList[cnt])))
                elif(self.jobList[cnt:cnt+1].mask == False):        
                     self.jobTable.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt]))))
                self.jobTable.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.jobTable.item(cnt,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.jobTable.item(0,0).setToolTip('SQUEEZE DELAY-(0-99 Cycles): Solenoid Valves is operated,<a>corresponding to start switch closure respectively</a> This time delay can be set to 99 cycles max.This delay is skipped during repeat operation')
            self.jobTable.item(1,0).setToolTip('SQUEEZE-(0-99 Cycles): The time duration for the electrodes to close on the work <a> and build up pressure before WELD time begins</a>')
            self.jobTable.item(2,0).setToolTip('FORGE VALVE -(0-4999mSec):The output provide to trigger an additional solenoid valves.<a>This way it is possible to generate additinal pressure.</a>This timming of the signal can be programmable. <a>It can be set with start of the SQZ at the earliest.</a>The timmer is forced to reset the output at the end of the HOLD at the latest.')
            self.jobTable.item(3,0).setToolTip('CURRENT REF -(0-XX.X): <a>Actual current can be set for </a>Alaram limits for current')
            self.jobTable.item(4,0).setToolTip('CURRENT TOL -(5-15): <a>% Tolerance')
            self.jobTable.item(5,0).setToolTip('UPSLOPE - (0-99 Cycles):<a>To determine the time span in which </a>the mementary current shall be increased from starting current to the command current')
            self.jobTable.item(6,0).setToolTip('WELD1 -(0-99 Cycles)  :<a>The time for first weld period</a>')
            self.jobTable.item(7,0).setToolTip('HEAT1 -(0-99%) :<a>The Heat of the first period</a>')
            self.jobTable.item(8,0).setToolTip('COOL1 -(0-99 Cycles) :<a>The Cool time between first</a> and second weld period')
            self.jobTable.item(9,0).setToolTip('WELD2 -(0-99 Cycles) :<a>The time of first weld period</a>')
            self.jobTable.item(10,0).setToolTip('HEAT2 -(0-99%) :<a>The heat of first weld period</a>')
            self.jobTable.item(11,0).setToolTip('PULSES -(0-99 Cycles)  :<a>The number of WELD2 times repeated</a>')
            self.jobTable.item(12,0).setToolTip('COOL2 -(0-99 Cycles)  :<a>Cool time between first and second weld period</a>')
            self.jobTable.item(13,0).setToolTip('HOLD -(0-99 Cycles):The time for which welding pressure is maintained <a>on  the weld after welding current has stopped flowing in this time</a>The solenoid valves is releases at the end of the HOLD and<a> clectrodes get opns.The output triggers the ed of weld.</a>')
            self.jobTable.item(14,0).setToolTip('OFF -(0-99 Cycles) :If the Repeat switch is ON and Start Sw.<a>is closed then operation loops back SQUEEZE.</a>If there was an error and thus the ALARM output was ON,<a>then Repeat is not acted upon.')
            self.jobTable.item(15,0).setToolTip('MODE -Non-Repeat :Non-Repeat swquence the weld timer reacts to the start signal<a> and starts the welding process.If the start signal is still</a>at the end of the hold time.the solenoid willbe switched off.<a>The electrodes open.Repeat sequence operation,performs </a>successive weld sequences for the duration of the start/initiation signal.')
        else :    
            self.counter = ["CountUpto(0-9999)","At CountEnd"]
            self.units =["No of Welds ","0=Continue,1=Stop"]
            for cnt in np.arange(2):
                self.jobTable.setItem(cnt,0, QTableWidgetItem(self.counter[cnt]))
                self.jobTable.item(cnt,0).setFlags(Qt.ItemIsEnabled)
                self.jobTable.setItem(cnt,2, QTableWidgetItem(self.units[cnt]))
                self.jobTable.item(cnt,2).setFlags(Qt.ItemIsEnabled)
                if(self.jobList[cnt+16:cnt+17].mask == False):
                    self.jobTable.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt+16]))))
                self.jobTable.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.jobTable.item(cnt,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)    
            self.jobTable.item(0,0).setToolTip(':Counter can be adjustable from 0-9999 counts')
            self.jobTable.item(1,0).setToolTip(':ATEND-CONTINUE or STOP-if set is STOP at the end of set count,machine will stop, if set is<a>CONTINUE - after completetion od set count,</a>machine will continue')    
            self.Configure = ["FactoryDefault","CurrentCheck","RemoteTrim","BeatMode","2Hand","Frequency"]
            self.units = ["0=No,1=Yes","0=Disable,1=Enable","0=Disable,1=Enable","0=Disable,1=Enable","0=Disable,1=Enable","0=50Hz,1=60Hz"]
            self.jobTable.item(2,0).setFlags(Qt.ItemIsEnabled)            
            self.jobTable.item(2,1).setFlags(Qt.ItemIsEnabled)            
            self.jobTable.item(2,2).setFlags(Qt.ItemIsEnabled)            
            for cnt in np.arange(0,6):
                self.jobTable.setItem(cnt+3,0, QTableWidgetItem(self.Configure[cnt]))
                self.jobTable.item(cnt+3,0).setFlags(Qt.ItemIsEnabled)
                self.jobTable.setItem(cnt+3,2, QTableWidgetItem(self.units[cnt]))
                self.jobTable.item(cnt+3,2).setFlags(Qt.ItemIsEnabled)
                if(self.jobList[cnt+18:cnt+19].mask == False):
                    self.jobTable.setItem(cnt+3,1, QTableWidgetItem(str(int(self.jobList[cnt+18])))) 
                self.jobTable.item(cnt+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.jobTable.item(cnt+3,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.jobTable.item(3,0).setToolTip('YES/NO :')
            self.jobTable.item(4,0).setToolTip('ON/OFF :Display ON:When running a job,if the actual<a>Weld-current fallas outside +/-10 % Tol</a>limits,then an error will be recognised and <a>ALARM raised.Display OFF:NO ALARM raised')
            self.jobTable.item(5,0).setToolTip('ON/OFF :IF REMOTE TRIM is ON-<a>Percentage HEAT2 value can be adjusted by</a> +/-12 HEAT value of set parameter from ready menu')
            self.jobTable.item(6,0).setToolTip('ON/OFF :NON BEAT MODE -If Foot switch is released <a>after the end of SQUZEE time Wels Seq. will be continue till end</a>.ie SEQ is latched at the end of SQUZEE time.<a>BEAT MODE - Wels seq is Stopped When foot switch</a>released, no mattaer where the seq is it.')
            self.jobTable.item(7,0).setToolTip('OFF/ON :2hand operation is OFF POSITION : <a>only foot switch can be used,2 hand operation</a>ON POSITION: Both FS1 & FS2 has to be press simultaneously within <a>second for weld sequence to happen</a>')
            self.jobTable.item(8,0).setToolTip('0=50Hz/1=60Hz')       
            
            self.jobTable.item(9,0).setFlags(Qt.ItemIsEnabled)            
            self.jobTable.item(9,1).setFlags(Qt.ItemIsEnabled)            
            self.jobTable.item(9,2).setFlags(Qt.ItemIsEnabled)            
            
            self.jobTable.setItem(10,0, QTableWidgetItem("Software Weld Control"))  
            if(self.jobList[24:25].mask == False):
                self.jobTable.setItem(10,1, QTableWidgetItem(str(int(self.jobList[24]))))
            self.jobTable.item(10,0).setToolTip('0=Weld Disable,1=Weld Enable :')
            self.jobTable.item(10,0).setFlags(Qt.ItemIsEnabled)
            self.jobTable.setItem(10,2, QTableWidgetItem("0=Weld Disable,1=Weld Enable"))
            self.jobTable.item(10,2).setFlags(Qt.ItemIsEnabled)
            self.jobTable.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.jobTable.item(10,2).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            for cnt in np.arange(11,16):
                self.jobTable.item(cnt,0).setFlags(Qt.ItemIsEnabled)
                self.jobTable.item(cnt,1).setFlags(Qt.ItemIsEnabled)
                self.jobTable.item(cnt,2).setFlags(Qt.ItemIsEnabled)
        self.userUpdate = 1
    
    def isFloat(self,s): 
        try: 
           s = float(s) 
        except: 
           return False 
        return True   
    
    def saveMenueventEng(self):
        if(str(self.selectMenuE.currentText()) == 'ScheduleJob' and  self.userUpdate == 1):
            #Shedule Menu            
            for sh in np.arange(16):
                item = self.jobTable.item(sh,1)
                if(item and self.isFloat(str(item.text()))==True): 
                    self.entry = 1
                    if(sh==0 and (float(item.text())>999 or float(item.text())<0)):
                        self.entry = 0                        
                    if(sh==2 and (float(item.text())>4999 or float(item.text())<0)):
                        self.entry = 0
                    if(sh==3 and (float(item.text())>99.9 or float(item.text())<0)):
                        self.entry = 0
                    if(sh==4 and (float(item.text())>15 or float(item.text())<5)):
                        self.entry = 0
                    if(sh==10 and (float(item.text())>99 or float(item.text())<0)):
                        self.entry = 0
                    if(sh==15 and (float(item.text())>1 or float(item.text())<0)):
                        self.entry = 0
#                    if((sh==0 or sh==1 or (sh > 3 and sh <10) or (sh>10 and sh<14)) and float(item.text())>99 or float(item.text())<0):
                    if((sh==1 or (sh > 4 and sh <10) or (sh>10 and sh<15)) and float(item.text())>99 or float(item.text())<0): 
                       self.entry = 0
                    
                    if(self.entry == 1):
                        self.jobList[sh]= float(item.text())
                    else:
                        self.result = QMessageBox.question(self, 'Error', "Error In Entry\t%s"%(self.shedule[sh]), QMessageBox.Close)
                        self.jobTable.setItem(sh,1, QTableWidgetItem(str('')))
                        self.jobList[sh:sh+1].mask = True
                        self.jobTable.item(sh,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                elif(str(item.text()) != "" and self.isFloat(str(item.text()))==False):
                    self.jobTable.setItem(sh,1, QTableWidgetItem(str('')))
                    self.result = QMessageBox.question(self, 'Error', "Error In Entry (Enter Only Digits)", QMessageBox.Close)
                    self.jobTable.item(sh,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                
        elif(self.userUpdate == 1):  #counter-config-weld
            #Counter Menu
            for sh in np.arange(2):
                item = self.jobTable.item(sh,1)
                if(item and str(item.text()).isdigit()):  
                    self.entry = 1
                    if(sh==0 and (float(item.text())>9999 or float(item.text())<0)):
                        self.entry = 0
                    if(sh==1 and (float(item.text())>1 or float(item.text())<0)):            
                        self.entry = 0
                    
                    if(self.entry == 1):
                        self.jobList[sh+16]= float(item.text())
                    else:
                        self.result = QMessageBox.question(self, 'Error', "Error In Entry\t%s"%(self.counter[sh]), QMessageBox.Close)
                        self.jobTable.setItem(sh,1, QTableWidgetItem(str('')))                        
                        self.jobList[sh+16:sh+17].mask = True
                        self.jobTable.item(sh,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                elif(str(item.text()) != "" and self.isFloat(str(item.text()))==False):
                    self.jobTable.setItem(sh,1, QTableWidgetItem(str('')))
                    self.result = QMessageBox.question(self, 'Error', "Error In Entry (Enter Only Digits)", QMessageBox.Close)
                    self.jobTable.item(sh,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                
            
            #Configure Menu            
            for sh in np.arange(6):
               item = self.jobTable.item(sh+3,1)
               if(item and str(item.text()).isdigit()):
                    self.entry = 1
                    if(float(item.text())>1 or float(item.text())<0):
                        self.entry = 0
                    if(self.entry == 1):
                        self.jobList[18+sh]= float(item.text())
                    else:    
                        self.result = QMessageBox.question(self, 'Error', "Error In Entry\t%s"%(self.Configure[sh]), QMessageBox.Close)
                        self.jobTable.setItem(sh+3,1, QTableWidgetItem(str('')))                        
                        self.jobList[sh+18:sh+19].mask = True
                        self.jobTable.item(sh+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
               elif(str(item.text()) != "" and self.isFloat(str(item.text()))==False):
                    self.jobTable.setItem(sh+3,1, QTableWidgetItem(str('')))
                    self.result = QMessageBox.question(self, 'Error', "Error In Entry (Enter Only Digits)", QMessageBox.Close)
                    self.jobTable.item(sh+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                           
            
            #weld Menu
            item = self.jobTable.item(10,1)
            if(item and str(item.text()).isdigit()): 
                    self.entry = 1
                    if(float(item.text())>1 or float(item.text())<0):
                        self.entry = 0
                    if(self.entry == 1):   
                        self.jobList[24]= float(item.text())
                    else:    
                        self.result = QMessageBox.question(self, 'Error', "Error In Entry\tSoftware Weld Control", QMessageBox.Close)
                        self.jobTable.setItem(10,1, QTableWidgetItem(str('')))
                        self.jobList[24:25].mask = True
                        self.jobTable.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)    
            elif(str(item.text()) != "" and self.isFloat(str(item.text()))==False):
                    self.jobTable.setItem(10,1, QTableWidgetItem(str('')))
                    self.result = QMessageBox.question(self, 'Error', "Error In Entry (Enter Only Digits)", QMessageBox.Close)
                    self.jobTable.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                           
    def loadFromeventEng(self):
        if(str(self.loadFromE.currentText()) == 'Computer'):
                self.selectJobE.clear()
                for f in os.listdir(self.cdir):
                    jobNumber = re.findall(r'\d+', f)
                    self.selectJobE.addItems(jobNumber)
        else:
             self.selectJobE.clear()
             for f in np.arange(1,9):
                 self.selectJobE.addItems(str(f))
    
    def displayJobeventEng(self):
           self.userUpdate = 0
           if(str(self.loadFromE.currentText()) == 'Computer'):
                 self.jobfile = self.cdir+'\job'+(str(self.selectJobE.currentText()))+'.npy'
                 if(os.path.isfile(self.jobfile)):                          
                      self.jobList[:] = np.load(self.jobfile)[:25]
                      self.docList[:] = np.load(self.jobfile)[25:25+12]
                      self.doc1_E.setText(self.docList[0])
                      self.doc2_E.setText(self.docList[1])
                      self.doc3_E.setText(self.docList[2])
                      self.doc4_E.setText(self.docList[3])
                      self.doc5_E.setText(self.docList[4])
                      self.doc6_E.setText(self.docList[5])
                      self.doc7_E.setText(self.docList[6])
                      self.doc8_E.setText(self.docList[7])
                      self.doc9_E.setText(self.docList[8])
                      self.doc10_E.setText(self.docList[9])
                      self.doc11_E.setText(self.docList[10]) 
                      self.doc12_E.setPlainText(self.docList[11])
                 else:    
                      self.jobList[:].mask = True
                 if(any(self.jobList.mask==1)):
                      self.message(3) # error in download  
           else:
                self.jobList[:].mask = True
                self.commandPacket[0] = self.headername
                self.commandPacket[1] = 0xF1
                self.commandPacket[2] = int(self.selectJobE.currentText())
                self.commandPacket[3] = 0x00
                self.commandPacket[4] = self.footername
                self.writeFtdi(0,self.commandPacket)              
                self.job = 1
                time.sleep(0.2)#wait 200ms assuming job is received in 200 ms   
                self.jobList[:2] = self.receiveJob[:2]
                self.jobList[2] = self.receiveJob[2] * 256 + self.receiveJob[3]
                if(all(self.receiveJob[4:6].mask == False)):                
                    self.jobList[3] = float(str(self.receiveJob[5])+"."+str(self.receiveJob[4]))
                self.jobList[4:16] = self.receiveJob[6:18]
                self.jobList[16] = self.receiveJob[18] * 256 + self.receiveJob[19]
                self.jobList[17:25] = self.receiveJob[20:28]
                self.message(99)
                self.doc1_E.setText("")
                self.doc2_E.setText("")
                self.doc3_E.setText("")
                self.doc4_E.setText("")
                self.doc5_E.setText("")
                self.doc6_E.setText("")
                self.doc7_E.setText("")
                self.doc8_E.setText("")
                self.doc9_E.setText("")
                self.doc10_E.setText("")
                self.doc11_E.setText("")
                self.doc12_E.setPlainText("")                 
                if(any(self.jobList.mask==1) and (self.com == 1)):
                   self.message(3) # error in download           
               
           if(str(self.selectMenuE.currentText()) == 'ScheduleJob'):
               for cnt in np.arange(16):
                   if(cnt == 3 and self.jobList[cnt:cnt+1].mask == False):         
                      self.jobTable.setItem(cnt,1, QTableWidgetItem(str(self.jobList[cnt])))
                   elif(self.jobList[cnt:cnt+1].mask == False):        
                      self.jobTable.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt]))))
                   self.jobTable.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
           else:            
               for cnt in np.arange(2):
                   if(self.jobList[cnt+16:cnt+17].mask == False):                   
                       self.jobTable.setItem(cnt,1, QTableWidgetItem(str(int(self.jobList[cnt+16]))))
                   self.jobTable.item(cnt,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
               for cnt in np.arange(6):
                   if(self.jobList[cnt+18:cnt+19].mask == False):                   
                       self.jobTable.setItem(cnt+3,1, QTableWidgetItem(str(int(self.jobList[cnt+18]))))
                   self.jobTable.item(cnt+3,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
               
               if(self.jobList[24:25].mask == False):                   
                   self.jobTable.setItem(10,1, QTableWidgetItem(str(int(self.jobList[24]))))
               self.jobTable.item(10,1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
           self.userUpdate = 1
    
    def deleteJobeventEng(self):
        if(str(self.loadFromE.currentText()) == 'Computer'):
            self.jobfile = self.cdir+'\job'+str(self.selectJobE.currentText())+'.npy' 
            self.printfile = self.printdir+'\printJob'+str(self.selectJobE.currentText())+'.doc'
            if(os.path.isfile(self.jobfile)):             
                 os.remove(self.jobfile)
                 self.jobList[:].mask = True
                 self.selectJobE.clear()
                 for f in os.listdir(self.cdir):
                     jobNumber = re.findall(r'\d+', f)
                     self.selectJobE.addItems(jobNumber)    
            
            if(os.path.isfile(self.printfile)):        
                 os.remove(self.printfile)
                 self.docList[:] = ''
    
    def SaveToComputereventEng(self):
        if(any(self.jobList.mask==1)):
            self.message(1) # error in save       
        elif(str(self.jobNo.text()).isdigit()):
            self.docList[0] = str(self.doc1_E.text())
            self.docList[1] = str(self.doc2_E.text())
            self.docList[2] = str(self.doc3_E.text())
            self.docList[3] = str(self.doc4_E.text())
            self.docList[4] = str(self.doc5_E.text())
            self.docList[5] = str(self.doc6_E.text())
            self.docList[6] = str(self.doc7_E.text())
            self.docList[7] = str(self.doc8_E.text())
            self.docList[8] = str(self.doc9_E.text())
            self.docList[9] = str(self.doc10_E.text())
            self.docList[10] = str(self.doc11_E.text())
            self.docList[11] = str(self.doc12_E.toPlainText())
            self.jobfile = self.cdir+'\job'+"%03d"%(int(self.jobNo.text()))+'.npy'   
            np.save(self.jobfile,np.append(np.asarray(self.jobList),self.docList))
            self.printDoc()
            self.result = QMessageBox.question(self, 'Message', "Job "+str(self.jobNo.text())+" Saved in Computer", QMessageBox.Close)
            jobNumber = "%03d"%(int(self.jobNo.text()))
            if(str(self.loadFromE.currentText()) == 'Computer'):
                val = self.selectJobE.currentText()
                self.selectJobE.clear()
                for f in os.listdir(self.cdir):
                    jobNumber = re.findall(r'\d+', f)
                    self.selectJobE.addItems(jobNumber)
                self.selectJobE.setCurrentIndex(self.selectJobE.findText(val))
        else:    
            self.message(1) # error in save
    
    def printDoc(self):
        self.printdoc = np.chararray(33,500)
        self.printdoc[0]   = "==========================================="
        self.printdoc[1]   = "     MECHELONIC WeldGuru Software"   
        self.printdoc[2]   = "==========================================="
        self.printdoc[3]   = "Job No:"+str(self.jobNo.text())+"\n"
        self.printdoc[4]   = "==========================================="
        self.printdoc[5]   = "DESCRIPTION"
        self.printdoc[6]   = "==========================================="
        self.printdoc[7]   = "Weld Title                    :"+str(self.docList[0])
        self.printdoc[8]   = "Top Sheet Material            :"+str(self.docList[2])
        self.printdoc[9]   = "Top Sheet Thickness, mm       :"+str(self.docList[3])
        self.printdoc[10]  = "Bottom Sheet Material         :"+str(self.docList[4])
        self.printdoc[11]  = "Bottom Sheet Thickness, mm    :"+str(self.docList[5])
        self.printdoc[12]  = "Upper Electrode Dwg No        :"+str(self.docList[6])
        self.printdoc[13]  = "Lower Electrode Dwg No        :"+str(self.docList[7])
        self.printdoc[14]  = "Force Mode(High or Low)       :"+str(self.docList[8])
        self.printdoc[15]  = "Air Pressure(Top)             :"+str(self.docList[9])
        self.printdoc[16]  = "Air Pressure(Bottom)          :"+str(self.docList[10])
        self.printdoc[17]  = "Remarks                       :"+str(self.docList[11].replace("\n"," "))+"\n"

        self.printdoc[18]  = "==========================================="
        self.printdoc[19]  = "WELD PARAMETERS"
        self.printdoc[20]  = "==========================================="
        self.printdoc[21]  = "Weld Force                    :"+str(self.docList[1])
        self.printdoc[22]  = "Squeeze, No of Cycles         :"+str(int(self.jobList[1]))
        self.printdoc[23]  = "Forge Delay, msec             :"+str(int(self.jobList[2]))
        self.printdoc[24]  = "Weld-1,No of Cycles           :"+str(int(self.jobList[5]))
        self.printdoc[25]  = "Weld-1, Heat %                :"+str(int(self.jobList[6]))
        self.printdoc[26]  = "Cool-1,No of Cycles           :"+str(int(self.jobList[7]))
        self.printdoc[27]  = "Weld-2,No of Cycles           :"+str(int(self.jobList[8]))
        self.printdoc[28]  = "Weld-2, Heat %                :"+str(int(self.jobList[9]))
        self.printdoc[29]  = "Cool-2,No of Cycles           :"+str(int(self.jobList[11]))
        self.printdoc[30]  = "Hold Time, No of Cycles       :"+str(int(self.jobList[12]))
        self.printdoc[31]  = "Off Time, No of Cycles        :"+str(int(self.jobList[13]))
        self.printdoc[32]  = "==========================================="
        self.printfile = self.printdir+'\printJob'+"%03d"%(int(self.jobNo.text()))+'.doc'  
        np.savetxt(self.printfile,self.printdoc,delimiter='\t', fmt="%s")        
        
    def sentJobeventEng(self):#downloadjobtotimer  
        if(any(self.jobList.mask==1) or str(self.selectJobE.currentText()).isdigit()==False):
            self.message(2) # error in job list/jobnumber              
        else:
            self.jobnumber  =  int(self.selectJobE.currentText())
            self.commandPacket[0] = self.headername
            self.commandPacket[1] = 0xF0
            self.commandPacket[2] = 0x00
            self.commandPacket[3] = 0x00
            self.commandPacket[4] = self.footername
            self.writeFtdi(0,self.commandPacket)              
            self.dataPacket[0]    = self.headername
            self.dataPacket[1]    = self.jobnumber
            self.dataPacket[2]    = (int(self.jobList[0]) & 0xFF00)>>8  #Sq delay msb
            self.dataPacket[3]    = (int(self.jobList[0]) & 0xFF)       #Sq delay lsb
            self.dataPacket[4]    = self.jobList[1]
            self.dataPacket[5]    = (int(self.jobList[2]) & 0xFF00)>>8  #forge lsb
            self.dataPacket[6]    = (int(self.jobList[2]) & 0xFF)       #forge Msb     
            self.dataPacket[7]    = str(self.jobList[3]).split(".")[1]  #current ref decimal
            self.dataPacket[8]    = str(self.jobList[3]).split(".")[0]  #current ref int
            self.dataPacket[9:21] = self.jobList[4:16]  
            self.dataPacket[21]   = (int(self.jobList[16]) & 0xFF00)>>8  #count upto lsb
            self.dataPacket[22]   = (int(self.jobList[16]) & 0xFF)       #count Msb
            self.dataPacket[23:31]= self.jobList[17:25]       #count Msb
            self.dataPacket[-1:]  = self.footername
            self.writeFtdi(1,self.dataPacket)           
            self.message(0)
#DATALOG EVENTS       
    
    def saveDatalogevent(self): 
        self.fileName = str(QFileDialog.getSaveFileName(self, 'Dialog Title', self.ddir, selectedFilter='*.txt'))
        if self.fileName:
            self.saveList =   np.c_[self.dat1,self.tim1,self.dataList]
            np.savetxt(self.fileName, self.saveList,delimiter='\t', fmt="%s") 
            self.result = QMessageBox.question(self, 'Message', "DatalogSaved", QMessageBox.Close)    
    
    def datalogComputerevent(self):
        self.clearDatalog()
        self.fileName = str(QFileDialog.getOpenFileName(self, 'Dialog Title', self.ddir, selectedFilter='*.txt'))        
        self.dataList = np.genfromtxt(self.fileName,dtype='str')
        self.dat1 = self.dataList[:,0]
        self.tim1 = self.dataList[:,1]
        self.dataList = np.asarray((self.dataList[:,2:]),dtype=np.uint8)
        for wno in np.arange(self.dataList.shape[0]):
            for sh in np.arange(0,self.packetLength):
                self.dataTable.setItem(wno,sh+2, QTableWidgetItem(str(self.dataList[wno,sh])))
            self.dataTable.setItem(wno,0, QTableWidgetItem(self.dat1[wno]))
            self.dataTable.setItem(wno,1, QTableWidgetItem(self.tim1[wno]))   
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_title("Title",fontsize=8)
        self.ax.set_xlabel('Read Points',fontsize=8)
        self.ax.set_ylabel(str(self.plotoption.currentText()),fontsize=8)
        poList = [2,5]  #weld current coloumn and force voltage column       
        po = poList[self.plotoption.currentIndex()]
        y = self.dataList[::-1,po]
        x = np.arange(len(y))
        if(self.xmin.text() != '' and self.xmax.text() != '' ):
            self.ax.set_xlim(int(self.xmin.text()),int(self.xmax.text()))
        if(self.ymin.text() != '' and self.ymax.text() != '' ):
            self.ax.set_ylim(int(self.ymin.text()),int(self.ymax.text()))
        self.fig.subplots_adjust(left=0.05, right=0.98, top=0.90, bottom=0.16)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.plot(x,y,'r-')
        self.datalog.addWidget(self.canvas,12,1,1,8)
    
    def startDatalogevent(self):
        self.globalPause = 0
        if(self.t2 == 0): #run thread if it is not running
            self.t2 = start_new_thread(self.liveUpdate,(1,))        
    
    def liveUpdate(self,arg):  
          while(1):
              if(self.globalPause == 0):
                  time.sleep(self.wait)                   
                  self.pausePlot = 1   # stop updating the plot while table filling
                  self.dataList= self.receiveLog[:self.packetCount,:] # select only filled length
                  self.dataList= self.dataList[::-1,:] # invert the arrya inorder to get the new data at the top of the table
                  self.tim1 = np.asarray(self.tim)[:self.packetCount][::-1]  # invert time and date list to get the new time at top                
                  self.dat1 = np.asarray(self.dat)[:self.packetCount][::-1]                  
                  for wno in np.arange(self.packetCount):
                      for sh in np.arange(0,self.packetLength):
                           if(self.globalPause == 0):
                               self.dataTable.setItem(wno,sh+2, QTableWidgetItem(str(self.dataList[wno,sh])))
                      if(self.globalPause == 0):                      
                          self.dataTable.setItem(wno,0, QTableWidgetItem(self.dat1[wno]))
                          self.dataTable.setItem(wno,1, QTableWidgetItem(self.tim1[wno]))
                  self.pausePlot = 0     # start updating the plot while table filling   
    def updatePlot(self,i):
        if(self.globalPause == 0 and self.pausePlot == 0):
            self.ax.clear()
            self.ax.grid(True)
            self.ax.set_title("Title",fontsize=8)
            self.ax.set_xlabel('Read Points',fontsize=8)
            self.ax.set_ylabel(str(self.plotoption.currentText()),fontsize=8)
            poList = [2,5]  #weld current coloumn and force voltage column       
            po = poList[self.plotoption.currentIndex()]
            y = self.dataList[::-1,po]
            x = np.arange(len(y))
            if(self.xmin.text() != '' and self.xmax.text() != '' ):
                self.ax.set_xlim(int(self.xmin.text()),int(self.xmax.text()))
            if(self.ymin.text() != '' and self.ymax.text() != '' ):
                self.ax.set_ylim(int(self.ymin.text()),int(self.ymax.text()))
            self.fig.subplots_adjust(left=0.05, right=0.98, top=0.90, bottom=0.16)
            self.ax.tick_params(axis='both', which='major', labelsize=8)
            self.ax.plot(x,y,'r-')
            self.datalog.addWidget(self.canvas,12,1,1,8)
    
    def pausePlotevent(self):
        self.globalPause = 1
    
    def clearDatalog(self):
        self.read = 0
        self.globalPause = 1
        self.dataTable.clear() 
        self.dataTable.setHorizontalHeaderLabels(("Date","Time","JobNumber","WeldNumber","WeldCurr","U-Limit","L-Limit","Forceval","U-Limit","L-limit","PASS/FAIL"))
        self.packetCount = 0    #reset 
        self.paramCount = 0     #reset
        self.validData =  0     #reset
        self.receiveLog= np.zeros((self.buffer,self.packetLength),dtype = np.uint8)
        self.dataList = np.zeros((self.buffer,self.packetLength),dtype = np.uint8)
        self.dat = ['']*self.buffer
        self.tim = ['']*self.buffer
        self.ax.clear()
        self.ax.grid(True)
        self.datalog.addWidget(self.canvas,12,1,1,8)
        self.read = 1
    
    def applyEvent(self):
        self.read = 0
        self.globalPause = 1
        self.dataTable.clear()        
        self.dataTable.setHorizontalHeaderLabels(("Date","Time","JobNumber","WeldNumber","WeldCurr","U-Limit","L-Limit","Forceval","U-Limit","L-limit","PASS/FAIL"))
        self.packetCount = 0 #counts number of pacjets received 1 packet = 9 bytes
        self.paramCount = 0 # counts number of bytes in a packet
        self.validData =  0 #reset
        self.buffer =  int(self.bufferSize.text())
        self.dataTable.setRowCount(self.buffer)
        self.receiveLog = np.zeros((self.buffer,self.packetLength),dtype=np.uint8)
        self.dataList = np.zeros((self.buffer,self.packetLength),dtype = np.uint8)
        self.dat = ['']*self.buffer
        self.tim = ['']*self.buffer
        self.ax.clear()
        self.ax.grid(True)
        self.datalog.addWidget(self.canvas,12,1,1,8)
        self.read = 1
    
    def applyIntervalevent(self):
        self.wait =  int(self.interval.text())
#Setting Tab Events
    
    def updatePasswordOpevent(self):
        if(str(self.passwordOp.text()) == str(self.repasswordOp.text())):
            self.result = QMessageBox.question(self, 'Error',"Update username and Password?",QMessageBox.Yes,QMessageBox.No) 
            if(self.result == QMessageBox.Yes):          
                f=open(self.pdir+"\AuthOpU","wb")
                f.write(bz2.compress(str(self.userNameOp.text()))+"\n")
                f.close()                
                f=open(self.pdir+"\AuthOpP","wb")
                f.write(bz2.compress(str(self.passwordOp.text()))+"\n")
                f.close()
        else:        
            self.result = QMessageBox.question(self, 'Error',"Password Mismatch", QMessageBox.Close) 
        
    def updatePasswordEgevent(self):     
        if(str(self.passwordEg.text()) == str(self.repasswordEg.text())):
            self.result = QMessageBox.question(self, 'Error',"Update username and Password?",QMessageBox.Yes,QMessageBox.No) 
            if(self.result == QMessageBox.Yes):          
                f=open(self.pdir+"\AuthEgU","wb")
                f.write(bz2.compress(str(self.userNameEg.text())))
                f.close()
                f=open(self.pdir+"\AuthEgP","wb")
                f.write(bz2.compress(str(self.passwordEg.text())))
                f.close()
        else:        
           self.result = QMessageBox.question(self, 'Error',"Password Mismatch", QMessageBox.Close) 
        
#FTDI routines    
    def readftdi(self,arg): 
        while(1):
            if(self.read):
                for line in self.ser.read():
                    val = ord(line)
                    if(self.job==0): # dataLogg
                        if(val == 170): #0xAA is the Header
                            self.validData =  1
                            self.paramCount = 0 
                        elif((val == 187) and(self.validData  == 1)and (self.packetCount < self.buffer)) : #0xBB is the footer
                            self.validData =  0
                            self.paramCount = 0
                            ltime = time.localtime()
                            self.dat[self.packetCount] = str(ltime[2])+'-'+str(ltime[1])+'-'+str(ltime[0])   
                            self.tim[self.packetCount] = str(ltime[3])+':'+str(ltime[4])+':'+str(ltime[5]) 
                            self.packetCount = self.packetCount + 1
                            if(self.packetCount == self.buffer):
                              self.packetCount = self.packetCount#packet count 1023
                        elif((val != '') and (self.validData == 1) and (self.packetCount < self.buffer)): # valid data  
                            if(self.paramCount < self.packetLength):
                                self.receiveLog[self.packetCount,self.paramCount] = val
                                self.paramCount = self.paramCount + 1
                    else:#reading Job          
                         if(val == 170): #0xAA is the Header
                             self.validJob =  1
                             self.jobCount = 0 
                             #self.receiveJob[:] = np.ma.masked
                         elif((val == 187) and(self.validJob == 1)) : #0xBB is the footer  
                             self.validJob =  0
                             self.jobCount = 0
                             self.job = 0               
                         elif((val != '') and (self.validJob == 1) ): # valid data                              
                            if(self.jobCount<27):                            
                                self.receiveJob[self.jobCount] = val
                                self.jobCount = self.jobCount + 1
                            #if(self.jobCount == 25) header/footer correction in data
                            #if(self.jobCount == 26)  
                            
    def writeFtdi(self,mode,packet = np.zeros([],dtype=np.uint16)):
        self.pack = ''        
        self.checksum = 0
        for c0,p in enumerate(packet):
            self.pack = self.pack+chr(p & 0xFF)
            self.checksum = self.checksum + (p & 0xFF)
        self.checksum = self.checksum%255         
        if(self.ser):        
            self.ser.write(self.pack)        
            self.com = 1
        else:
            self.com = 0
    
    def connectftdi(self):
        #self.ftdistatus.clear()
        ports = list(serial.tools.list_ports.comports())
        self.ftdistatus.setText("Not Detected")
        self.ftdistatusOp.setText("Not Detected")
        self.ftdistatus.setStyleSheet("QLabel {color : red; }")
        self.ftdistatusOp.setStyleSheet("QLabel {color : red; }")
        
        for line in ports: 
            if("VID_0403+PID_6001" in str(line)):
                comNumber =  str(line).split(',')[0].split('(')[1].strip("'")
                self.ser = serial.Serial(port=comNumber,baudrate=115200,timeout=0)   
                self.ftdistatus.setText("FT232 Detected")
                self.ftdistatusOp.setText("FT232 Detected")
                self.ftdistatus.setStyleSheet("QLabel {color : black; }")
                self.ftdistatusOp.setStyleSheet("QLabel {color : black; }")
            elif("VID:PID=1A86:7523"  in str(line)):
                comNumber =  str(line).split(',')[0].split('(')[1].strip("'")
                self.ser = serial.Serial(port=comNumber,baudrate=115200,timeout=0)   
                self.ftdistatus.setText("CH340 Detected")
                self.ftdistatusOp.setText("CH340 Detected")
                self.ftdistatus.setStyleSheet("QLabel {color : black; }")
                self.ftdistatusOp.setStyleSheet("QLabel {color : black; }")
                
                
    
    def message(self,m):
        if(self.com==0):
            self.result = QMessageBox.question(self, 'Error',"COM Port Error", QMessageBox.Close)                       
        elif(m==0):    
            self.result = QMessageBox.question(self, 'Message',"Job Sent to Timer", QMessageBox.Close)
        elif(m==1):
            self.result = QMessageBox.question(self, 'Error',"Job Not Saved,Error in JobList/JobNo", QMessageBox.Close)
        elif(m==2):
            self.result = QMessageBox.question(self, 'Error',"Job Not Send,Error in jobList/JobNo", QMessageBox.Close)
        elif(m==3):    
            self.result = QMessageBox.question(self, 'Error',"Error in Download", QMessageBox.Close)
            
    def verifyLicense(self):
        self.licensefile = os.getcwd()+"\license.txt"
        if(os.path.isfile(self.licensefile) == False):
                self.result = QMessageBox.question(self, 'Message', "No License File Found", QMessageBox.Close)           
                sys.exit()        
        self.getmac = subprocess.check_output(['getmac']).split('\n')
        self.macsplit = ''
        self.licenseStatus = 0
        for line in self.getmac:
            if(line.count('-')>=5):
                self.mac= str(line.split(' ')[0])
                self.macsplit = self.mac.split('-')
                keygen = ''        
                for i in np.arange(len(self.macsplit)):
                    keygen = keygen + key[i][int(self.macsplit[i],16)] + '-'    
                self.file = open(self.licensefile)
                self.keygiven = self.file.read().strip("\n")
                if(self.keygiven == keygen[:-1]):
                    self.licenseStatus = 1
        if(self.licenseStatus == 0):       
            self.result = QMessageBox.question(self, 'Message', "License Error", QMessageBox.Close)           
            sys.exit()
 
            
                    
                    
app=QApplication.instance() # checks if QApplication already exists 
if not app: # create QApplication if it doesnt exist 
    app = QApplication(sys.argv)
mw=MainWindow()
sys.exit(app.exec_())


