from maya import cmds
from sgModules import sgHumanRigCommands
import os, json



def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName



class Win_Global:
    
    winName = 'sgui_getDotWeight'
    title   = 'UI - Get Dot Weight'
    width = 300
    height = 10
    
    infoPath = cmds.about( pd=1 ) + '/sg/sgui_getDotWeight_info.txt'
    makeFolder( os.path.dirname( infoPath ) )
    

    @staticmethod
    def saveInfo():
        pass


    @staticmethod
    def loadInfo():
        pass





class Win_Cmd:
    
    @staticmethod
    def loadBase( *args ):
        
        sels = cmds.ls( sl=1 )
        cmds.textField( Win_Global.fieldBase, e=1, tx= sels[-1] )

    
    
    @staticmethod
    def loadTarget( *args ):
        
        sels = cmds.ls( sl=1 )
        cmds.textField( Win_Global.fieldTarget, e=1, tx= sels[-1] )
    
    
    @staticmethod
    def create( *args ):
        
        from sgModules import sgcommands
        
        baseObj = cmds.textField( Win_Global.fieldBase, q=1, tx=1 )
        targetObj = cmds.textField( Win_Global.fieldTarget, q=1, tx=1 )
        
        valuesBase = cmds.floatFieldGrp( Win_Global.valueGrpBase, q=1, v=1 )
        valuesTarget = cmds.floatFieldGrp( Win_Global.valueGrpTarget, q=1, v=1 )
        
        newObj = cmds.createNode( 'transform', n='dotObj_%s' % targetObj.split( '|' )[-1] )
        newObj = cmds.parent( newObj, baseObj )[0]
        
        cmds.addAttr( newObj , ln='dotValue', min=-1, max=1, dv=0 )
        cmds.setAttr( newObj +'.dotValue', e=1, cb=1 )
        
        vectorNode = sgcommands.getDotWeight( baseObj, targetObj, valuesBase, valuesTarget )
        cmds.connectAttr( vectorNode + '.outputX', newObj + '.dotValue' )
        
        cmds.setAttr( newObj + '.t', 0,0,0 )
        cmds.setAttr( newObj + '.r', 0,0,0 )
        cmds.setAttr( newObj + '.s', 1,1,1 )
        cmds.select( newObj )
        




class UI_vectorObject:
    
    def __init__(self):
        pass
    
    def create(self, label, vector ):
        
        form = cmds.formLayout()
        btLoad = cmds.button( l= 'Load %s' % label, h=25, w=100 )
        field = cmds.textField( h=25, w=150 )
        floatfield = cmds.floatFieldGrp( l='vector : ', numberOfFields=3, value1=vector[0], value2=vector[1], value3=vector[2], cw=[1,70] )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(btLoad, 'left', 0), (btLoad, 'top', 0),
                               (field, 'top', 0),
                               (floatfield, 'top', 0),(floatfield, 'right', 0) ], 
                         ac = [(field, 'left', 0, btLoad ), (field, 'right', 0, floatfield )])
        
        self.btLoad = btLoad
        self.field  = field
        self.valueGrp = floatfield
        return form
        
        cmds.setParent( '..' )

    
        

class Win:
    
    def __init__(self ):
        
        self.ui_vectorBase    = UI_vectorObject()
        self.ui_vectorTarget    = UI_vectorObject()
    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        formOuter = cmds.formLayout()
        formVectorBase   = self.ui_vectorBase.create( 'Base' , [0,1,0])
        formVectorTarget = self.ui_vectorTarget.create( 'Target', [1,0,0] )
        bt_set = cmds.button( l='CREATE', c=Win_Cmd.create )
        cmds.setParent( '..' )

        cmds.formLayout( formOuter, e=1, 
                         af=[( formVectorBase, 'top', 5 ), ( formVectorBase, 'left', 5 ), ( formVectorBase, 'right', 5 ),
                             ( formVectorTarget, 'left', 5 ), ( formVectorTarget, 'right', 5 ),
                             ( bt_set, 'left', 5 ), ( bt_set, 'right', 5 ), ( bt_set, 'bottom', 5 ) ],
                         ac=[( formVectorTarget, 'top', 5, formVectorBase ),
                             ( bt_set, 'top', 5, formVectorTarget )] )
        
        cmds.window( Win_Global.winName, e=1, width = Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.loadInfo()
        
        Win_Global.fieldBase   = self.ui_vectorBase.field
        Win_Global.fieldTarget = self.ui_vectorTarget.field
        Win_Global.valueGrpBase = self.ui_vectorBase.valueGrp
        Win_Global.valueGrpTarget = self.ui_vectorTarget.valueGrp
        
        cmds.button( self.ui_vectorBase.btLoad, e=1, c= Win_Cmd.loadBase )
        cmds.button( self.ui_vectorTarget.btLoad, e=1, c= Win_Cmd.loadTarget )
        
        
        
        
    