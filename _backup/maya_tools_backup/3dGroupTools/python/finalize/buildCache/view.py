import maya.cmds as cmds
import uiModel
import cmdModel
from functools import partial
import os



class Window:
    
    def __init__(self):
        
        self._winName = uiModel.winName
        self._title = uiModel.title
        self._width = uiModel.width
        self._height= uiModel.height



    def getInfomation(self):
        
        animPath, cachePath = cmdModel.getPathFromFile()
        geoNames = cmdModel.getGeoSetAndGeometryFromFile()
        cmdModel.getTimeUnitFromFile()
        
        self._animPath  = animPath
        self._cachePath = cachePath
        #self._setNames = setNames
        self._geoNames = geoNames
        
        cmds.textFieldGrp( self._tf_animPath, e=1, tx=self._animPath )
        cmds.textFieldGrp( self._tf_cachePath, e=1, tx=self._cachePath )
        #cmds.textFieldGrp( self._tf_setNames, e=1, tx=self._setNames )
        cmds.textField( self._tf_geoNames, e=1, tx=self._geoNames )
        
    
    
    def setInfomation(self):
        
        self._animPath  = cmds.textFieldGrp( self._tf_animPath,  q=1, tx=1 )
        self._cachePath = cmds.textFieldGrp( self._tf_cachePath, q=1, tx=1 )
        #self._setNames  = cmds.textFieldGrp( self._tf_setNames,  q=1, tx=1 )
        if cmds.textField( self._tf_geoNames,  q=1, en=1 ):
            self._geoNames = cmds.textField( self._tf_geoNames,  q=1, tx=1 )
        else:
            self._geoNames = '' 
        
        cmdModel.setPathToFile(self._animPath, self._cachePath)
        cmdModel.setGeometryToFile(self._geoNames)

    
    
    def cmdBuildCache(self, *args ):
        
        self.setInfomation()
        path = cmds.textFieldGrp( self._tf_cachePath, q=1, tx=1 )
        cmdModel.buildCacheStandalone( path )
        
        
    def cmdImportCacheFile(self, *args ):
        
        path = cmds.textFieldGrp( self._tf_cachePath, q=1, tx=1 )
        selItems = cmds.textScrollList( self._sl_cachedGeos, q=1, si=1 )
        cmdModel.buildCacheScene( selItems, path )
    
    
    def cmdCheckCacheList(self, *args ):
        
        path = cmds.textFieldGrp( self._tf_cachePath, q=1, tx=1 )
        cachedShapeNames = []
        for root, dirs, names in os.walk( path ):
            for name in names:
                if name[-3:] == '.mc':
                    cachedShapeNames.append( name[:-3] )
            break
        cachedShapeNames.sort()
        cmds.textScrollList( self._sl_cachedGeos, e=1, ra=1, append=cachedShapeNames, 
                             h=len(cachedShapeNames)*13+4, vis=1 )
        
        
    def popupOpenFileBrowser(self, textFieldGrp, *args ):
        
        text = cmds.textFieldGrp( textFieldGrp, q=1, tx=1 )
        cmdModel.openFileBrowser( text )
        
        
    
    def cmdEnableGeoNames( self, *args ):
        
        if cmds.checkBox( self._ck_geoName, q=1, v=1 ):
            cmds.textField( self._tf_geoNames, e=1, en=1 )
        else:
            cmds.textField( self._tf_geoNames, e=1, en=0 )
    
    
    def create(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        cmds.window( self._winName, title=self._title )
        
        cmds.columnLayout()
        layoutWidth = self._width-2
        fieldWidth  = layoutWidth -2
        
        firstWidth  = fieldWidth *.3
        secondWidth = fieldWidth - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[ (1,layoutWidth)] )
        animPath  = cmds.textFieldGrp( l='Animation Path : ', cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.popupMenu()
        cmds.menuItem( l='Open File browser', c=partial( self.popupOpenFileBrowser, animPath ) )
        cachePath = cmds.textFieldGrp( l='  Cache Path   : ', cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.popupMenu()
        cmds.menuItem( l='Open File browser', c=partial( self.popupOpenFileBrowser, cachePath ) )
        cmds.text( l='', h=3 )
        #setNames = cmds.textFieldGrp( l='     Set Names : ', cw=[(1,firstWidth),(2,secondWidth)], tx='model_cache_set' )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=2, co=[(1,'left', 9)], cw=[(1,firstWidth+3),(2,secondWidth)] )
        geoNameCheck = cmds.checkBox( l='Geometry Names :  ', cc=self.cmdEnableGeoNames )
        geoNames = cmds.textField( en=0 )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[ (1,layoutWidth)] )
        cmds.text( l='', h=3 )
        cmds.button( l='Create Cache', c=self.cmdBuildCache )
        cmds.text( l='', h=1 )
        cmds.button( l='Check Cache List', c=self.cmdCheckCacheList )
        scrollList = cmds.textScrollList( h=1, ams=1, vis=0 )
        cmds.button( l='Import Cache Files', c=self.cmdImportCacheFile )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, title=self._title,
                     w=self._width, h=self._height )
        cmds.showWindow( self._winName )
        
        self._tf_animPath  = animPath
        self._tf_cachePath = cachePath
        #self._tf_setNames  = setNames
        self._tf_geoNames  = geoNames
        self._sl_cachedGeos = scrollList
        self._ck_geoName = geoNameCheck
        
        self.getInfomation()