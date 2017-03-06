'''
Created on Aug 11, 2014

@author: Dan
'''
import os, sys
import pymel.core as pm
import SimpleCurves



class ControlUI():
    def __init__(self, iconPath):
        self.name = "Control_Creation_UI"
        self.title = "Create Controls"
        
        if (pm.window(self.name, q=1, exists=1)): pm.deleteUI(self.name)
        self.window = pm.window(self.title, widthHeight=(300, 300),
                         resizeToFitChildren=1, menuBar=True)
        self.iconPath = iconPath
        icons = [f for f in os.listdir(self.iconPath) if f.endswith('.png')]
        
        #menu
        pm.menu( label='UI', helpMenu=True )
        pm.menuItem( label='Create Icons', command = pm.Callback(self.createIcons))
        
        form = pm.formLayout()
        tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        pm.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))
        
        child1 = pm.rowColumnLayout(numberOfColumns=3)
        for style in SimpleCurves.STYLES:
            if icons and "%s.png"%(style) in icons:
                iPath = os.path.join(self.iconPath, "%s.png"%(style))
                pm.iconTextButton(label=style, style='iconAndTextVertical', image1=iPath, command = pm.Callback(self.simpleCurve, style))
            else:
                pm.button(label=style, command = pm.Callback(self.simpleCurve, style))
        pm.setParent( '..' )
        
        child2 = pm.rowColumnLayout(numberOfColumns=2)
        pm.button()
        pm.setParent( '..' )
        
        child3 = pm.rowColumnLayout(numberOfColumns=2)
        pm.button()
        pm.button()
        pm.button()
        pm.setParent( '..' )
        
        pm.tabLayout( tabs, edit=True, tabLabel=((child1, 'Simple Curves'), (child2, 'Combo Controls'), (child3, 'Facial Controls')) )
        pm.showWindow(self.window)
        
    def simpleCurve(self, style):
        newCurve = SimpleCurves.Curve(style, name = "Control")
        return newCurve
    
    def createIcons(self):
        print "CREATE ICONS"
        formatOrig = pm.getAttr("defaultRenderGlobals.imageFormat")
        
        for style in SimpleCurves.STYLES:
            iPath = os.path.join(self.iconPath, "%s.png"%(style))
            pm.setAttr("defaultRenderGlobals.imageFormat", 32)
            newCurve = self.simpleCurve(style)
            pm.viewFit(all=True)
            pm.playblast(frame=1, format = "image", cf = iPath, wh = (100,100), p=100)
            newCurve.delete()
        
        pm.setAttr("defaultRenderGlobals.imageFormat", formatOrig)   
        ControlUI(self.iconPath)
   



def create():
    iconPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'icons'))
    print iconPath
    ControlUI(iconPath)