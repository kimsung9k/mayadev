import maya.cmds as cmds
import sgModelUI
import os
from functools import partial


class UIBakeTargets:
    
    def __init__(self, parentUi, *args ):
        
        self.textAreaWidth = parentUi.textAreaWidth
        self.bakeTargetField = sgModelUI.PopupFieldUI( 'Bake Targets  :  ', 'Load Selected', 'multi', textWidth = self.textAreaWidth,
                                                       addCommand = partial( Window_functions( parentUi ).loadReferenceList, parentUi.uiReference.textScroll ) )
    
    
    def create(self):

        form = cmds.formLayout()
        self.bakeTargetField.create()
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1,
                         attachForm =[ (self.bakeTargetField._form, 'top', 5),
                                       (self.bakeTargetField._form, 'left', 0),
                                       (self.bakeTargetField._form, 'right', 0),
                                       (self.bakeTargetField._form, 'bottom', 5) ] )

        self.form = form
        self.field = self.bakeTargetField._field

        return form




class UIPaths:
    
    def __init__(self, parentUi ):
        
        self.textAreaWidth = parentUi.textAreaWidth
        self.fieldHeight = 23


    def create(self):
        
        form = cmds.formLayout()
        
        tx_currentPath = cmds.text( l='Scene Path  :  ', al='right', w=self.textAreaWidth, h=self.fieldHeight )
        txf_currentPath = cmds.textField( en=1, h=self.fieldHeight )
        pu_currentPath = cmds.popupMenu()
        tx_exportPath = cmds.text( l='Export Path  :  ', al='right', w=self.textAreaWidth, h=self.fieldHeight )
        txf_exportPath = cmds.textField( en=1, h=self.fieldHeight )
        pu_exportPath = cmds.popupMenu()
        tx_cameraPath  = cmds.text( l='Camera Path  :  ', al='right', w=self.textAreaWidth, h=self.fieldHeight )
        txf_cameraPath = cmds.textField( en=1, h=self.fieldHeight )
        pu_cameraPath = cmds.popupMenu()
        tx_cachePath = cmds.text( l='Cache Path  :  ', al='right', w=self.textAreaWidth, h=self.fieldHeight )
        txf_cachePath = cmds.textField( en=1, h=self.fieldHeight )
        pu_cachePath = cmds.popupMenu()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         attachForm = [ ( tx_currentPath, 'top', 5), ( tx_currentPath, 'left', 0),
                                        ( txf_currentPath, 'top', 5), ( txf_currentPath, 'right', 0),
                                        ( tx_exportPath, 'left', 0),
                                        ( txf_exportPath, 'right', 0),
                                        ( tx_cameraPath, 'left', 0),
                                        ( txf_cameraPath, 'right', 0),
                                        ( tx_cachePath, 'bottom', 5), ( tx_cachePath, 'left', 0),
                                        ( txf_cachePath, 'bottom', 5), ( txf_cachePath, 'right', 0) ],
                         attachControl = [ ( tx_exportPath, 'top', 0, txf_currentPath ), ( txf_exportPath, 'top', 0, txf_currentPath ),
                                           ( tx_cameraPath, 'top', 0, txf_exportPath ),  ( txf_cameraPath, 'top', 0, txf_exportPath ),
                                           ( tx_cachePath, 'top', 0, txf_cameraPath ),  ( txf_cachePath, 'top', 0, txf_cameraPath ),
                                           
                                           
                                           ( txf_currentPath, 'left', 0, tx_currentPath ),
                                           ( txf_exportPath, 'left', 0, tx_exportPath ),
                                           ( txf_cameraPath, 'left', 0, tx_cameraPath ),
                                           ( txf_cachePath, 'left', 0, tx_cachePath ) ] )
        
        self.form = form
        self.txf_currentPath = txf_currentPath
        self.pu_currentPath = pu_currentPath
        self.txf_exportPath = txf_exportPath
        self.pu_exportPath = pu_exportPath
        self.txf_cameraPath = txf_cameraPath
        self.pu_cameraPath = pu_cameraPath
        self.txf_cachePath = txf_cachePath
        self.pu_cachePath = pu_cachePath
        
        return form




class UIReferences:
    
    def __init__(self, parentUi ):
        
        self.form = ''
        self.textScroll = 'txsl_sgSceneBakeUpdateCacheBody'


    def create(self):
        
        form = cmds.formLayout()
        
        frame = cmds.frameLayout( l='Target References' )
        textScroll = cmds.textScrollList( self.textScroll )
        popup = cmds.popupMenu()
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         attachForm = [( frame, 'top', 0 ), ( frame, 'bottom', 0 ), 
                                       ( frame, 'left', 0 ), ( frame, 'right', 0 )] )
        
        self.form = form
        self.textScroll = textScroll
        self.popup = popup
        
        return form



class UIFrames:
    
    def __init__(self, parentUi ):
        
        self.form = ''
        
    
    def create(self):
        
        form = cmds.formLayout()
        
        startFrame = cmds.intFieldGrp( numberOfFields=2, l='Start Frame', cw=[(1,120), (2,70), (3,70)] )
        endFrame   = cmds.intFieldGrp( numberOfFields=2, l='End frame'  , cw=[(1,120), (2,70), (3,70)]  )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         attachForm = [( startFrame, 'top', 0 ),( startFrame, 'bottom', 0 ),( startFrame, 'left', 0 ),
                                       ( endFrame, 'top', 0 ),( endFrame, 'bottom', 0 ),( endFrame, 'right', 0 )],
                         attachPosition = [(startFrame, 'right', 0, 50 ),
                                           (endFrame, 'left', 0, 50 )])
        
        self.form = form
        self.startFrame = startFrame
        self.endFrame   = endFrame
        
        return form



class UIButtons:
    
    def __init__(self, parentUi ):
        
        self.form = ''
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        buttonExportCam = cmds.button( l='Export Camera', h=30 )
        buttonExportTargets = cmds.button( l='Export Targets', h=30 )
        buttonReferenceCam = cmds.button( l='Reference Camera', h=30 )
        buttonImportCacheBodies = cmds.button( l='Import Cache Bodies', h=30 )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         attachForm = [ ( buttonExportCam, 'top', 0 ),( buttonExportCam, 'left', 0 ),
                                        ( buttonExportTargets, 'top', 0 ), ( buttonExportTargets, 'right', 0 ),
                                        ( buttonReferenceCam, 'bottom', 0 ), ( buttonReferenceCam, 'left', 0 ), 
                                        ( buttonImportCacheBodies, 'bottom', 0 ), ( buttonImportCacheBodies, 'right', 0 ) ],
                        attachPosition = [(buttonExportCam, 'right', 0, 50),(buttonExportCam, 'bottom', 0, 50),
                                          (buttonExportTargets, 'left', 0, 50), (buttonExportTargets, 'bottom', 0, 50),
                                          (buttonReferenceCam, 'right', 0, 50), (buttonReferenceCam, 'top', 0, 50),
                                          (buttonImportCacheBodies, 'left', 0, 50), (buttonImportCacheBodies, 'top', 0, 50),])
        
        self.buttonExportCam  = buttonExportCam
        self.buttonExportTargets  = buttonExportTargets
        self.buttonReferenceCam = buttonReferenceCam
        self.buttonImportCacheBodies = buttonImportCacheBodies

        self.form = form
        '''
        form  = cmds.formLayout()
        
        buttonBake              =  cmds.button( l = 'Bake', h=30 )
        buttonCreateBakedObject =  cmds.button( l = 'Create Baked Object', h=30 )
        buttonClose =  cmds.button( l = 'Close', h=30 )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         attachForm = [( buttonBake, 'top', 0 ),( buttonBake, 'left', 0 ),
                                       ( buttonCreateBakedObject, 'top', 0 ),( buttonCreateBakedObject, 'right', 0 ),
                                       ( buttonClose, 'bottom', 0 ),( buttonClose, 'left', 0 ),( buttonClose, 'right', 0 )],
                         attachPosition = [(buttonBake, 'bottom', 0, 50 ),(buttonBake, 'right', 0, 50 ),
                                           (buttonCreateBakedObject, 'bottom', 0, 50 ),(buttonCreateBakedObject, 'left', 0, 50 ),
                                           (buttonClose, 'top', 0, 50 )] )
        
        self.form = form
        self.buttonBake  = buttonBake
        self.buttonCreateBakedObject  = buttonCreateBakedObject
        self.buttonClose = buttonClose
        '''
        return form




class Window:
    
    def __init__(self):
        
        self.winName = 'sgUISceneBake'
        self.title   = 'SG Scene Bake UI'
        self.width   = 800
        self.height  = 600
    
        self.textAreaWidth = 150
        self.textAreaPercent = 30
        
        self.uiReference  = UIReferences( self )
        self.uiBakeTarget = UIBakeTargets( self )
        self.uiPaths      = UIPaths( self )
        self.uiFrames     = UIFrames( self )
        self.uiButtons    = UIButtons( self )
        self.windowFunction = Window_functions( self )



    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        form = cmds.formLayout()
        
        formPaths      = self.uiPaths.create()
        formBakeTarget = self.uiBakeTarget.create()
        formReferences = self.uiReference.create()
        formUIFrames   = self.uiFrames.create()
        formButtons    = self.uiButtons.create()
        
        cmds.setParent( '..' )
        '''
        cmds.formLayout( form, e=1,
                         attachForm = [ (formPaths, 'top', 5), ( formPaths, 'left', 0 ), ( formPaths, 'right', 0 ),
                                        (formBakeTarget, 'left', 0),     ( formBakeTarget, 'right', 0),
                                        (formReferences, 'left', 0), ( formReferences, 'right', 0),(formReferences, 'bottom', 0)],
                         attachControl = [ ( formBakeTarget, 'top', 0, formPaths ),
                                           ( formReferences, 'top', 0, formBakeTarget )] )
        
        '''
        cmds.formLayout( form, e=1,
                         attachForm = [ (formPaths, 'top', 5), ( formPaths, 'left', 0 ), ( formPaths, 'right', 0 ),
                                        (formBakeTarget, 'left', 0),     ( formBakeTarget, 'right', 0),
                                        (formReferences, 'left', 0), ( formReferences, 'right', 0),
                                        (formUIFrames, 'left', 0), ( formUIFrames, 'right', 0),
                                        (formButtons, 'left', 0), (formButtons, 'right', 0),(formButtons, 'bottom', 0) ],
                         attachControl = [ ( formBakeTarget, 'top', 0, formPaths ),
                                           ( formReferences, 'top', 0, formBakeTarget ),( formReferences, 'bottom', 0, formUIFrames ),
                                           ( formUIFrames, 'bottom', 0, formButtons )] )
        
        cmds.window( self.winName, e=1, w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.bakeTargetField  = self.uiBakeTarget.field
        self.currentPathField = self.uiPaths.txf_currentPath
        self.exportPathField  = self.uiPaths.txf_exportPath
        self.cameraPathField  = self.uiPaths.txf_cameraPath
        self.cachePathField   = self.uiPaths.txf_cachePath
        
        self.pu_currentPath = self.uiPaths.pu_currentPath
        self.pu_exportPath  = self.uiPaths.pu_exportPath
        self.pu_cameraPath  = self.uiPaths.pu_cameraPath
        self.pu_cachePath   = self.uiPaths.pu_cachePath
        self.pu_cacheBody   = self.uiReference.popup
        
        self.windowFunction.updateCurrentPath( self.currentPathField )
        self.windowFunction.updateExportPath( self.exportPathField )
        self.windowFunction.updateCameraPath( self.cameraPathField )
        self.windowFunction.updateCachePath( self.cachePathField )
        self.windowFunction.updateStartAndEndFrame( self.uiFrames.startFrame, self.uiFrames.endFrame )
        self.windowFunction.addButtonCmdExportCam( self.uiButtons.buttonExportCam )
        self.windowFunction.addButtonCmdExportTargets( self.uiButtons.buttonExportTargets )
        self.windowFunction.addButtonCmdReferenceCam( self.uiButtons.buttonReferenceCam )
        self.windowFunction.addButtonCmdImportCacheBodies( self.uiButtons.buttonImportCacheBodies )
        
        sgModelUI.updatePathPopupMenu( self.currentPathField, self.pu_currentPath, None )
        sgModelUI.updatePathPopupMenu( self.exportPathField,  self.pu_exportPath , None )
        sgModelUI.updatePathPopupMenu( self.cameraPathField,  self.pu_cameraPath , None )
        sgModelUI.updatePathPopupMenu( self.cachePathField ,  self.pu_cachePath  , None )
        cmds.textField( self.currentPathField, e=1, en=0 )
        
        cmds.textScrollList( self.uiReference.textScroll, e=1, 
                             sc = partial( sgModelUI.updatePathPopupMenu_forScrollList,
                                           self.uiReference.textScroll, self.pu_cacheBody, None ) )





class Window_functions:

    def __init__(self, ui ):

        self.ui = ui



    def updateCurrentPath( self, pathField ):
        
        currentPath = cmds.file( q=1, sceneName=1 )
        cmds.textField( pathField, e=1, tx=currentPath )


    def updateExportPath(self, cachePathField ):
        
        currentPath = cmds.file( q=1, sceneName=1 )
        if not currentPath: return None
        splits = currentPath.split( '/' )
        
        cutName = splits[-3]
        cachePath = '/'.join( splits[:-1] ) + '/export/%s_ani_export_r01.mb' % cutName
        cmds.textField( cachePathField, e=1, tx=cachePath )


    def updateCachePath(self, cachePathField ):
        
        currentPath = cmds.file( q=1, sceneName=1 )
        if not currentPath: return None
        splits = currentPath.split( '/' )
        
        cachePath = '/'.join( splits[:-2] ) + '/cache/master'
        cmds.textField( cachePathField, e=1, tx=cachePath )


    def updateCameraPath(self, cachePathField ):
        
        currentPath = cmds.file( q=1, sceneName=1 )
        if not currentPath: return None
        splits = currentPath.split( '/' )
        
        minTime = cmds.playbackOptions( q=1, minTime=1 )
        maxTime = cmds.playbackOptions( q=1, maxTime=1 )
        strMinTime = '%d' % minTime
        strMaxTime = '%d' % maxTime
        strMinTime = strMinTime.replace( '-', 'm' )
        strMaxTime = strMaxTime.replace( '-', 'm' )
        
        cachePath = '/'.join( splits[:-2] ) + '/reference/camera/anicam/anicam_%s_%s_bake.mb' %( strMinTime, strMaxTime )
        cmds.textField( cachePathField, e=1, tx=cachePath )
    
    
    def loadReferenceList(self, scrollList ):
        
        sels = cmds.listRelatives( cmds.ls( sl=1 ), c=1, ad=1, f=1 )

        cmds.textScrollList( scrollList, e=1, ra=1 )
        
        fileNames = []
        namespaces = []
        filePaths = []
        for sel in sels:
            if not cmds.reference( sel, q=1, inr=1 ): continue
            
            namespace = cmds.referenceQuery( sel, ns=1 )
            
            filePath = cmds.reference( sel, q=1, filename=1 )
            
            fileName = filePath.split( '/' )[-1]
            if not fileName in fileNames:
                fileNames.append( fileName )
                namespaces.append( namespace[1:] )
            else:
                continue
            
            filePaths.append( filePath )

        targetTxts = []
        for i in range( len( fileNames ) ):
            targetTxt = '%s --> %s' %( namespaces[i], filePaths[i] )
            targetTxts.append( targetTxt )
        
        cmds.textScrollList( scrollList, e=1, append=targetTxts )


    def updateStartAndEndFrame(self, startFrameField, endFrameField ):

        minTime = cmds.playbackOptions( q=1, minTime=1 )
        maxTime = cmds.playbackOptions( q=1, maxTime=1 )

        cmds.intFieldGrp( startFrameField, e=1, v1= -5, v2=minTime )
        cmds.intFieldGrp( endFrameField  , e=1, v1= maxTime, v2=5 )



    def addButtonCmdBake( self, uiButton ):
        
        def bake( *args ):
            
            import sgFunctionCache
            
            bakeTargets = cmds.textField( self.ui.bakeTargetField, q=1, tx=1 )
            cachePath   = cmds.textField( self.ui.cachePathField, q=1, tx=1 )
            
            startOffset, startFrame = cmds.intFieldGrp( self.ui.uiFrames.startFrame, q=1, v=1 )
            endFrame   , endOffset  = cmds.intFieldGrp( self.ui.uiFrames.endFrame, q=1, v=1 )
            
            sgFunctionCache.bake( bakeTargets, 
                                  startFrame = (startOffset + startFrame),
                                  endFrame   = (endOffset   + endFrame), 
                                  cachePath = cachePath, geometryBake=1, transformBake=1 )

        cmds.button( uiButton, e=1, c=bake )
        
        
    
    def addButtonCmdExportCam( self, uiButton ):
        
        def cameraBake( *args ):
            import hgCameraBake
            cameraPath   = cmds.textField( self.ui.cameraPathField, q=1, tx=1 )
            hgCameraBake.doBake( cameraPath )
        
        cmds.button( uiButton, e=1, c=cameraBake )
        


    def addButtonCmdExportTargets( self, uiButton ):
        
        def sceneBake( *args ):
            import sgFunctionSceneBake2
            
            bakeTargets = cmds.textField( self.ui.bakeTargetField, q=1, tx=1 ).split( ' ' )
            cachePath   = cmds.textField( self.ui.cachePathField, q=1, tx=1 )
            
            startOffset, startFrame = cmds.intFieldGrp( self.ui.uiFrames.startFrame, q=1, v=1 )
            endFrame   , endOffset  = cmds.intFieldGrp( self.ui.uiFrames.endFrame, q=1, v=1 )

            print "export target", bakeTargets, cachePath, startFrame, endFrame, startOffset, endOffset
            sgFunctionSceneBake2.exportBakedData(bakeTargets, cachePath, startFrame, endFrame, startOffset, endOffset)
            
        cmds.button( uiButton, e=1, c=sceneBake )



    def addButtonCmdReferenceCam( self, uiButton ):
        
        def referenceCam( *args ):
            camPath = cmds.textField( self.ui.cameraPathField, q=1, tx=1 )
            cmds.file( camPath, r=1, type="mayaBinary", gl=1, loadReferenceDepth="all",
                       mergeNamespacesOnClash=True, namespace= ":", options ="v=0;" )
        
        cmds.button( uiButton, e=1, c=referenceCam )



    def addButtonCmdImportCacheBodies( self, uiButton ):
        
        def importCacheBodys( *args ):
            
            import sgFunctionSceneBake2
            
            cachePath = cmds.textField( self.ui.cachePathField, q=1, tx=1 )
            sgFunctionSceneBake2.importBakeData( cachePath )
        
        cmds.button( uiButton, e=1, c=importCacheBodys )



    def addButtonCmdCreateBakedObject(self, uiButton ):
        
        def createBakedObject( *args ):
            
            import sgFunctionCache
            
            bakeTargets = cmds.textField( self.ui.bakeTargetField, q=1, tx=1 )
            cachePath   = cmds.textField( self.ui.cachePathField, q=1, tx=1 )
            
            sgFunctionCache.importCacheAndBake( bakeTargets, cachePath = cachePath )
        
        cmds.button( uiButton, e=1, c= createBakedObject )



    def addButtonCmdcloseWindow(self, uiButton ):
        
        def deleteWindow( *arsg ):
            cmds.deleteUI( self.ui.winName, wnd=1 )
        
        cmds.button( uiButton, e=1, c=deleteWindow )




def showWindow( *args ):
    Window().create()


mc_showWindow = '''import sgUISceneBake
sgUISceneBake.Window().create()'''