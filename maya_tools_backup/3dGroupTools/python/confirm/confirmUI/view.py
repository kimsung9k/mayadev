#!/usr/bin/python
#-*- coding: utf-8 -*-
#-*- encoding: cp949 -*-

import maya.cmds as cmds
import datetime
import platform
from functools import partial


def setClipboardData( text ):
    pass


class DateAndPath_ui():
    def __init__(self, *args):
        self.repairString = ''
        
        if cmds.window( 'dateAndPath_ui', ex=1 ):
            cmds.deleteUI( 'dateAndPath_ui', wnd=1 )
        self.win = cmds.window( 'dateAndPath_ui', title='Confirm Text UI')
        
        if not cmds.uiTemplate( 'checkBoxTemp', ex=1 ):
            cmds.uiTemplate( 'checkBoxTemp' )
        
        cmds.checkBox( dt='checkBoxTemp', h=20, onc=self.update, ofc=self.update )
        cmds.setUITemplate( 'checkBoxTemp', pushTemplate=1 ) 
        
        form = cmds.formLayout()
        assetCheck = cmds.frameLayout( l='Asset' )
        self.assetCheck = cmds.rowColumnLayout( nc=5, co=(1,'left',10), cw=[(1,100),(2,100),(3,100),(4,100),(5,100)] )
        cmds.checkBox( l='Modeling' )
        cmds.checkBox( l='Blend Shape' )
        cmds.checkBox( l='Scale' )
        cmds.checkBox( l='Texture' )
        cmds.text( l='' )
        cmds.checkBox( l='Shader' )
        cmds.checkBox( l='UV' )
        cmds.checkBox( l='Cloth' )
        cmds.checkBox( l='Hair' )
        cmds.checkBox( l='Rigging' )
        cmds.setParent( form )
        
        layoutCheck = cmds.frameLayout( l='Layout' )
        self.layoutCheck = cmds.rowColumnLayout( nc=5, co=(1,'left',10), cw=[(1,130),(2,140),(3,100),(4,100),(5,30)] )
        cmds.checkBox( l='Camera' )
        cmds.checkBox( l='Matte Camera' )
        cmds.checkBox( l='BG' )
        cmds.checkBox( l='Frame Length' )
        cmds.text( l='' )
        cmds.checkBox( l='Matte Painting' )
        cmds.checkBox( l='Position' )
        cmds.setParent( form )
        
        productionCheck = cmds.frameLayout( l='Production' )
        self.productionCheck = cmds.rowColumnLayout( nc=5, co=(1,'left',10), cw=[(1,130),(2,140),(3,100),(4,100),(5,30)] )
        cmds.checkBox( l='Animation' )
        cmds.checkBox( l='Facial Ani' )
        cmds.checkBox( l='Hair Sim' )
        cmds.checkBox( l='Cloth Sim' )
        cmds.text( l='' )
        cmds.checkBox( l='Cache' )
        cmds.checkBox( l='Lighting' )
        cmds.checkBox( l='FX' )
        cmds.setParent( form )
        
        scrollField = cmds.scrollField( editable=True, wordWrap=False, h=80 )
        
        closeBt =cmds.button( l='Close', c= self.closeWindow, h=30 )
        
        cmds.formLayout( form, e=1, 
                         af=[ (assetCheck,'left',5 ),(assetCheck,'top',5 ),(assetCheck,'right',5 ),
                              (layoutCheck,'left',5 ),(layoutCheck,'top',75 ),(layoutCheck,'right',5 ),
                              (productionCheck,'left',5 ),(productionCheck,'top',145 ),(productionCheck,'right',5 ),
                              (scrollField, 'left', 5), (scrollField, 'right', 5),
                              (scrollField, 'top', 215), (scrollField, 'bottom', 40 ),
                              (closeBt, 'left', 5 ),(closeBt, 'right', 5 ),(closeBt, 'bottom', 5 )] )

        cmds.window( self.win, e=1, wh=[515,357 ] )
        cmds.showWindow( self.win )

        self.scrollField = scrollField

        self.editFieldString()
        
        self.checkBoxs = cmds.lsUI( type='checkBox' )
        
    def addRepairString( self, name ):
        if not self.repairString:
            self.repairString = name
        elif self.repairString.rstrip()[-1] == '\n':
            self.repairString = name
        elif self.repairString.rstrip()[-1] == ':':
            self.repairString += name
        else:
            self.repairString += ', '+name
    
    def update(self, *args ):
        self.repairString = ''
        
        cmds.scrollField( self.scrollField, e=1, text='' )
        
        checkUIs = []
        checkUIs.append( cmds.rowColumnLayout( self.assetCheck, q=1, ca=1 ) )
        checkUIs.append( cmds.rowColumnLayout( self.layoutCheck, q=1, ca=1 ) )
        checkUIs.append( cmds.rowColumnLayout( self.productionCheck, q=1, ca=1 ) )
        
        for cuCheckUIs in checkUIs:
            repairTitle = cmds.frameLayout( cmds.rowColumnLayout( cmds.checkBox( cuCheckUIs[0], q=1, p=1 ), q=1, p=1 ), q=1, l=1 )
            
            onCheckBoxEx = False
            for checkBox in cuCheckUIs:
                if not checkBox in self.checkBoxs:
                    continue
                if cmds.checkBox( checkBox, q=1, v=1 ):
                    if not onCheckBoxEx:
                        self.repairString += repairTitle+' : '
                        onCheckBoxEx = True
                    self.addRepairString( cmds.checkBox( checkBox, q=1, l=1 ) )
            if onCheckBoxEx:
                self.repairString += u' 수정\n'
                        
        self.editFieldString()

    def editFieldString( self, *args ):
        fpsDict = { 'game':15, 'film':24, 'pal':25, 'ntsc':30, 'show':48, 'palf':50, 'ntscf':60 }
        
        timeString = ':'.join( str( datetime.datetime.now() ).split( '.' )[0].split(':')[:-1] )
        comName = platform.node()
        playRange = '%d-%d' %( cmds.playbackOptions( q=1, min=1 ), cmds.playbackOptions( q=1, max=1 ) ) 
        frameRate = '%dp'  % fpsDict[ cmds.currentUnit( q=1, t=1 ) ]
        pathString = cmds.file( q=1, l=1 )[0].replace( '/', '\\' )

        cmds.scrollField( self.scrollField, e=1, text=timeString+' '+comName+' '+ playRange +' '+ frameRate +' \n'+pathString+'\n'+self.repairString )
        
    def setClipboard(self, *args ):
        pastStr = cmds.scrollField( self.scrollField, q=1, text=1 )
        setClipboardData( pastStr )

    def closeWindow(self, *args ):
        cmds.deleteUI( 'dateAndPath_ui', wnd=1 )