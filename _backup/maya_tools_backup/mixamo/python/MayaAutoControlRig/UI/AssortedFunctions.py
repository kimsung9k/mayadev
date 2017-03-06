'''
UI.AssortedFunctions
Handles:
    UI functions
'''
import maya.cmds as mayac
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import os


def goToWebpage(page):
    if page == "mixamo":
        mayac.showHelp( 'http://www.mixamo.com', absolute = True)
    elif page == "autoRigger":
        mayac.showHelp( 'http://www.mixamo.com/c/auto-rigger', absolute = True)
    elif page == "motions":
        mayac.showHelp( 'http://www.mixamo.com/motions', absolute = True)
    elif page == "autoControlRig":
        mayac.showHelp( 'http://www.mixamo.com/c/auto-control-rig-for-maya', absolute = True)
    elif page == "community":
        mayac.showHelp( 'https://community.mixamo.com', absolute = True)
    elif page == "tutorials":
        mayac.showHelp( 'https://community.mixamo.com/hc/en-us/sections/200559213-Maya', absolute = True)
    else:
        OpenMaya.MGlobal.displayError("Webpage Call Invalid")

def DJB_BrowserWindow(filter_ = None, caption_ = "Browse", fileMode_ = "directory"):
    multipleFilters = None
    filtersOld = None
    if filter_ == "Maya":
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
        filtersOld = None
    elif filter_ == "Maya_FBX":
        multipleFilters = "Valid Files (*.ma *.mb *.fbx);;FBX (*.fbx);;Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
    elif filter_ == "FBX":
        multipleFilters = "FBX (*.fbx);;All Files (*.*)"
    else:
        multipleFilters = ""
    window = None    
    version = mel.eval("float $ver = `getApplicationVersionAsFloat`;")
    if version <= 2011.0:
        if fileMode_ == "directory":
            window = mayac.fileBrowserDialog(dialogStyle = 2, windowTitle = caption_, fileType = "directory")
    else: #new style dialog window
        if fileMode_ == "directory":
            window = mayac.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, caption = caption_, fileMode = 3, okCaption = "Select")
        else:
            window = mayac.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, caption = caption_, fileMode = 4, okCaption = "Select")
    if window:
        return window[0]
    else:
        return window
    
def validateFolder(folder, create=False):
    if create and not os.path.isdir(folder):
        try: 
            os.makedirs(folder)
        except OSError:
            if not os.path.isdir(folder):
                raise
    if os.path.isdir(folder):
        return folder
    else:
        return None
    
def validateFile(file):
    if os.path.exists(file):
        return file
    else:
        return None