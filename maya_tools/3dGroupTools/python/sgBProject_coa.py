import maya.cmds as cmds




class WinA_Cmd:
    
    @staticmethod
    def cmdSelectSgWobbleCurve( *args ):
        sgWobbleCurves = []
        for hist in cmds.listHistory( cmds.ls( sl=1 ), pdo=1 ):
            if cmds.nodeType( hist ) != 'wire': continue
            targetCrv = cmds.listConnections( hist+'.deformedWire[0]' )
            crvHists = cmds.listHistory( targetCrv, pdo=1 )
            for crvHist in crvHists:
                if cmds.nodeType( crvHist ) != 'sgWobbleCurve2': continue
                sgWobbleCurves.append( crvHist )
        if sgWobbleCurves: cmds.select( sgWobbleCurves )
        
        
        
    @staticmethod
    def cmdSelectCurve( *args ):
        sgCurves = []
        for hist in cmds.listHistory( cmds.ls( sl=1 ), pdo=1 ):
            if cmds.nodeType( hist ) != 'wire': continue
            targetCrv = cmds.listConnections( hist+'.deformedWire[0]' )
            sgCurves.append( targetCrv[0] )
        if sgCurves: cmds.select( sgCurves )


    
    @staticmethod
    def cmdSelectUpObject( *args ):
        upObjects = []
        for hist in cmds.listHistory( cmds.ls( sl=1 ), pdo=1 ):
            if cmds.nodeType( hist ) != 'wire': continue
            targetCrv = cmds.listConnections( hist+'.deformedWire[0]' )
            crvHists = cmds.listHistory( targetCrv, pdo=1 )
            for crvHist in crvHists:
                if cmds.nodeType( crvHist ) != 'sgWobbleCurve2': continue
                mm = cmds.listConnections( crvHist+'.aimMatrix' )[0]
                upObj = cmds.listConnections( mm+'.matrixIn[0]' )[0]
                upObjects.append( upObj )
        if upObjects: cmds.select( upObjects )


    @staticmethod
    def cmdSelectFollicle( *args ):
        upObjects = []
        for hist in cmds.listHistory( cmds.ls( sl=1 ), pdo=1 ):
            if cmds.nodeType( hist ) != 'wire': continue
            targetCrv = cmds.listConnections( hist+'.deformedWire[0]' )
            crvHists = cmds.listHistory( targetCrv, pdo=1 )
            for crvHist in crvHists:
                if cmds.nodeType( crvHist ) != 'sgWobbleCurve2': continue
                mm = cmds.listConnections( crvHist+'.aimMatrix' )[0]
                upObj = cmds.listConnections( mm+'.matrixIn[0]' )[0]
                upObjects.append( upObj )
        if upObjects: cmds.select( upObjects )





class WinA:
    
    def __init__(self):
        
        self.winName = 'sgBProject_wobbleCurveEditor'
        self.title   = 'Wobble Curve Editor'
        
        self.width = 300
        self.height = 10
        
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw= [1,self.width] )
        cmds.button( l='Select Curve', h=25, bgc=[0.8,0.8,0.6], c=WinA_Cmd.cmdSelectCurve )
        cmds.button( l='Select SG Wobble Curve', h=25, bgc=[0.5,0.5,1.0], c=WinA_Cmd.cmdSelectSgWobbleCurve )
        cmds.button( l='Select UP Object', h=25, bgc=[0.5,0.7,0.5], c=WinA_Cmd.cmdSelectUpObject )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1, w= self.width, h= self.height, rtf=1 )
        cmds.showWindow( self.winName )