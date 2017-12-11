from maya import cmds
import maya.mel as mel

class cList:

    @staticmethod
    def selCtrl(self):
        sel=cmds.ls(sl=True)
        cmds.textScrollList( Win.TSL , e=True, ra=True)
        cmds.textScrollList( Win.TSL , e=True, numberOfRows=10 , allowMultiSelection=True, append=sel)
        
    @staticmethod
    def selPrint():
        selTSL = cmds.textScrollList( Win.TSL, q=1, si=1)
        print selTSL

class createImagineCtrl:
    
    @staticmethod
    def ctrlCreate(self):
        print "ctrlCreate"
        selTSL = cmds.textScrollList( Win.TSL, q=1, si=1)
        selTSLsize = len(selTSL)
        for x in range(0, selTSLsize):
            #print selTSL[x]
            cmds.curve( p=[(0, 0, 0), (0, 6, 0), (0, 7, 1), (0, 8, 0), (0, 7, -1), (0, 6, 0)], d=1, k=[0,1,2,3,4,5])
            circlename=cmds.ls(sl=True)
            cmds.rename(circlename[0], '%s_simul_Con'%selTSL[x]) 
            cmds.circle(n='%s_animkey_Con'%selTSL[x])
            selCircle=cmds.ls(sl=True)
            cmds.setAttr( '%s.rotateY'%selCircle[0], 90)
            cmds.setAttr( '%s.scaleX'%selCircle[0], 5)
            cmds.setAttr( '%s.scaleY'%selCircle[0], 5)
            cmds.setAttr( '%s.scaleZ'%selCircle[0], 5)
            cmds.FreezeTransformations()
            cmds.ResetTransformations()
            #cmds.DeleteAllHistory()
            cmds.group('%s_animkey_Con'%selTSL[x], n='%s_animkey_Con_xform'%selTSL[x])
            cmds.select( clear=True )
            cmds.Group()
            doGroupA = cmds.ls(sl=1)
            cmds.rename(doGroupA[0], '%s_simul_Con_xform'%selTSL[x])
            cmds.parent('%s_simul_Con'%selTSL[x], '%s_simul_Con_xform'%selTSL[x])
            cmds.parent('%s_simul_Con_xform'%selTSL[x], '%s_animkey_Con'%selTSL[x])
            cmds.delete(cmds.parentConstraint( selTSL[x], '%s_animkey_Con_xform'%selTSL[x], w=.1 ))
            cmds.setAttr( '%s_simul_ConShape.overrideEnabled'%selTSL[x], 1)
            cmds.setAttr( '%s_simul_ConShape.overrideColor'%selTSL[x], 17)
            cmds.setAttr( '%s_animkey_ConShape.overrideEnabled'%selTSL[x], 1)
            cmds.setAttr( '%s_animkey_ConShape.overrideColor'%selTSL[x], 20)
            sizeX = selTSLsize-1
        for y in range(0, sizeX):
            if (y != sizeX):
                cmds.parent('%s_animkey_Con_xform'%selTSL[y+1], '%s_animkey_Con'%selTSL[y])
            else:
                pass
        for yy in range(0, selTSLsize):
            if(yy==0):
                po = cmds.listRelatives('%s'%selTSL[yy], p=1)
                selA = ( po[0], '%s_animkey_Con_xform'%selTSL[yy])
                srcCons = selA[1::2]
                consSize = len(srcCons)
                for i in range( consSize):
                    j= consSize+i
                    #k=yy-1
                    selTest = cmds.ls('MM_%s'%selA[i])
                    if (len(selTest) == 0):
                        cmds.createNode( 'multMatrix', n='MM_%s'%selA[i] )
                        cmds.createNode( 'decomposeMatrix', n='DM_%s'%selA[i] )
                        cmds.select( clear=True )
                        cmds.connectAttr( '%s.worldMatrix[0]'%po[i], 'MM_%s.matrixIn[0]'%selA[i] )
                        cmds.connectAttr( 'MM_%s.matrixSum'%selA[i], 'DM_%s.inputMatrix'%selA[i] )
                        cmds.connectAttr( 'DM_%s.outputTranslate'%selA[i], '%s.translate'%selA[j])
                        cmds.connectAttr( 'DM_%s.outputRotate'%selA[i], '%s.rotate'%selA[j])
                        cmds.connectAttr( '%s.parentInverseMatrix[0]'%selA[j], 'MM_%s.matrixIn[1]'%selA[i] )
                    else:
                        cmds.connectAttr( 'DM_%s.outputTranslate'%selA[i], '%s.translate'%selA[j])
                        cmds.connectAttr( 'DM_%s.outputRotate'%selA[i], '%s.rotate'%selA[j])
                atrList = cmds.listConnections( selTSL[yy], s=1, d=0, p=1, c=1 )
                if(atrList == None):
                    print 'None == %s'%selTSL[yy]
                else:
                    beforeList = atrList[1::2]
                    afterList = atrList[::2]
                    for ii in range(len(beforeList)):
                        tokenA = afterList[ii].split('.')
                        cmds.connectAttr( beforeList[ii], '%s_animkey_Con.%s'%(selTSL[yy], tokenA[1]))
            else:
                po = cmds.listRelatives('%s'%selTSL[yy], p=1)
                selA = ( po[0], '%s_animkey_Con_xform'%selTSL[yy])
                srcCons = selA[1::2]
                consSize = len(srcCons)
                for i in range( consSize):
                    j= consSize+i
                    k=yy-1
                    selTest = cmds.ls('MM_%s'%selA[i])
                    if (len(selTest) == 0):
                        cmds.createNode( 'multMatrix', n='MM_%s'%selA[i] )
                        cmds.createNode( 'decomposeMatrix', n='DM_%s'%selA[i] )
                        cmds.select( clear=True )
                        cmds.connectAttr( '%s.worldMatrix[0]'%selA[i], 'MM_%s.matrixIn[0]'%selA[i] )
                        cmds.connectAttr( '%s.worldInverseMatrix[0]'%selTSL[k], 'MM_%s.matrixIn[1]'%selA[i] )
                        cmds.connectAttr( 'MM_%s.matrixSum'%selA[i], 'DM_%s.inputMatrix'%selA[i] )
                        cmds.connectAttr( 'DM_%s.outputTranslate'%selA[i], '%s.translate'%selA[j])
                        cmds.connectAttr( 'DM_%s.outputRotate'%selA[i], '%s.rotate'%selA[j])
                    else:
                        cmds.connectAttr( 'DM_%s.outputTranslate'%selA[i], '%s.translate'%selA[j])
                        cmds.connectAttr( 'DM_%s.outputRotate'%selA[i], '%s.rotate'%selA[j])
                atrList = cmds.listConnections( selTSL[yy], s=1, d=0, p=1, c=1 )
                if(atrList == None):
                    print 'None == %s'%selTSL[yy]
                else:
                    beforeList = atrList[1::2]
                    afterList = atrList[::2]
                    for ii in range(len(beforeList)):
                        tokenA = afterList[ii].split('.')
                        cmds.connectAttr( beforeList[ii], '%s_animkey_Con.%s'%(selTSL[yy], tokenA[1]))

    @staticmethod
    def ctrlBake(self):
        selTSL = cmds.textScrollList( Win.TSL, q=1, si=1)
        selTSLsize = len(selTSL)
        selA = cmds.ls(sl=1)
        
        import maya.cmds as cmds
        endF = cmds.playbackOptions( q=1, max=1 )
        staF = cmds.playbackOptions( q=1, min=1 )
        samby = 1
        simyl = 0
        for y in  range(0, selTSLsize):
            print 'aa'
            cmds.bakeResults( '%s_animkey_Con_xform'%selTSL[y], t=(staF,endF), sb='%s'%samby, simulation=simyl)
            cmds.delete('%s_animkey_Con_xform_parentConstraint1'%selTSL[y])
            #print 'Start Frame = %s'%staF
            #print 'End Frame = %s'%endF
            #print 'Sample By = %s'%staF
            #if(simyl == 1):
            #    print "Simulation = True"
            #else:
            #    print "Simulation = False"
        
class Win:
    
    name = "ui_basic"
    title = "UI - Basic"
    width = 80
    height = 200
    TSL = 'TSL'
    
    def __init__(self):
        pass
    
    def create( self ):
        
        if cmds.window( Win.name, ex=1 ):
            cmds.deleteUI( Win.name, wnd=1 )
        cmds.window( Win.name, title=Win.title )
        cmds.window( Win.name, e=1, width= Win.width, height= Win.height )
        
        form = cmds.formLayout()
        b1 = cmds.button(l='CONTROLLER\nLIST', w=100, command=cList.selCtrl )
        b2 = cmds.button(l='SET', w=315, command=createImagineCtrl.ctrlCreate)
        b3 = cmds.button(l='BAKE', w=315, command=createImagineCtrl.ctrlBake)
        RCY = cmds.rowColumnLayout(numberOfColumns=1)
        Win.TSL = cmds.textScrollList( w=150, h=100, dcc=cList.selPrint )
        cmds.formLayout( form, edit=True,
        attachForm=[(b1, 'top', 15), (b1, 'left', 15), 
                    (b2, 'left', 15), (b2, 'right', 15),
                    (b3, 'left', 15), (b3, 'bottom', 15), (b3, 'right', 15),
                    (RCY, 'top', 15), (RCY, 'right', 15)], 
        attachControl=[(b1, 'bottom', 15, b2), (b2, 'bottom', 15, b3), (b2, 'top', 30, RCY), (b1, 'right', 15, RCY)], 
        attachPosition=[(b2, 'top', 0, 65), (b3, 'top', 25, 70), (RCY, 'left', 40, 40), (RCY, 'bottom', 0, 50)])
        
        cmds.showWindow( Win.name )
        
def show():
    Win().create()






#cmds.autoKeyframe(st=True)
#cmds.autoKeyframe(st=False)

#cmds.playbackOptions( loop='once' )























