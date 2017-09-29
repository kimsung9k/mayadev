#coding=utf8

import maya.cmds as cmds
from maya import OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
import model
import ntpath


class ControlBase:
    
    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    
    mainui = QtGui.QMainWindow()
    manageui = QtGui.QMainWindow()
    uiTreeWidget = QtGui.QWidget()
    
    infoBaseDir = cmds.about( pd=1 ) + "/pingowms"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    projectListPath = infoBaseDir + '/projectList.json'
    defaultInfoPath = infoBaseDir + '/defaultInfo.json'
    
    labelServerPath = 'serverPath'
    labelLocalPath = 'localPath'
    labelCurrentProject = 'currentProject'
    labelDefaultLocalPath = "defaultLocalFolder"
    labelDefaultServerPath = 'defaultServerPath'
    labelDefaultTaskFolder = 'defaultTaskFolder'
    labelDefaultTaskType = 'defaultTaskType'
    labelTasks    = 'tasks'
    labelTaskType = 'type'
    labelTaskPath = 'path'
    
    fileInfoExtension = 'pingowmsFileInfo'