import maya.cmds as cmds



class WindowInfo:
    
    _winName = 'createJointOnCurve_ui'
    _title   = 'Create Joint On Curve'
    
    _width = 350
    _height = 50


class CreateJointOnCurveSet:
    
    def __init__( self ):
        
        self._curveShape = ''
        self._minParam   = 0.0
        self._maxParam   = 1.0
        self._infoNum    = 5
        self._numSpans   = 5
        
        
    def setJointNum( self, num ):
        
        self._infoNum = num
        
        
    def setCurve( self, curveShape ):
        
        self._curveShape = curveShape
        self._minParam = cmds.getAttr( self._curveShape+'.minValue' )
        self._maxParam = cmds.getAttr( self._curveShape+'.maxValue' )
        self._numSpans = cmds.getAttr( self._curveShape+'.spans' )
    
    
    def create(self, distanceNode ):
        
        eachParam = ( self._maxParam - self._minParam )/( self._infoNum - 1 )
        
        eachInfos = []
        
        for i in range( self._infoNum ):
            info = cmds.createNode( 'pointOnCurveInfo', n= self._curveShape+'_info%d' % i )
            cmds.connectAttr( self._curveShape+'.local', info+'.inputCurve' )
            cmds.setAttr( info+'.parameter', eachParam*i + self._minParam )
            eachInfos.append( info )
            
        cmds.select( d=1 )
        
        joints = []
        for i in range( self._infoNum ):
            joints.append( cmds.joint(p=[i,0,0]) )
            
        handle, effector = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self._curveShape )
        
        distNodes = []
        for i in range( self._infoNum -1 ):
            
            firstInfo = eachInfos[i]
            secondInfo = eachInfos[i+1]
            targetJoint = joints[i+1]
            
            distNode = cmds.createNode( 'distanceBetween' )
            distNodes.append( distNode )
            
            cmds.connectAttr( firstInfo+'.position', distNode+'.point1' )
            cmds.connectAttr( secondInfo+'.position', distNode+'.point2')
            
            if distanceNode:
                cmds.connectAttr( distNode+'.distance', targetJoint+'.tx' )
            else:
                cmds.setAttr( targetJoint+'.tx', cmds.getAttr( distNode+'.distance' ) )
        
        if not distanceNode:
            cmds.delete( distNodes )
        
        return handle, joints
            
            
            
            

def createJointOnCurve( numJoint, distanceNode = True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1, f=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets
        
        


def createJointOnCurveByNumSpans( distanceNode = True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        curveSetInst.setJointNum( curveSetInst._numSpans+1 )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets



def createJointOnCurveByLength( multRate, distNode=True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    curveInfo = cmds.createNode( 'curveInfo' )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        cmds.connectAttr( selCurve+'.local', curveInfo+'.inputCurve', f=1 )
        length = cmds.getAttr( curveInfo+'.arcLength' )
        curveSetInst.setJointNum( int( length * multRate ) )
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distNode )
        
        returnTargets.append( joints )

    return returnTargets




class Window:
    
    def __init__(self):
        
        self._winName = WindowInfo._winName
        self._title   = WindowInfo._title
        self._width   = WindowInfo._width
        self._height  = WindowInfo._height
        
        
        
    def cmdCreate( self, *args ):
        
        checkValue = cmds.checkBox( self._check, q=1, v=1 )
        
        if cmds.radioButton( self._radio1, q=1, sl=1 ):
            numJoint = cmds.intSliderGrp( self._slider1, q=1, v=1 )
            createJointOnCurve( numJoint, checkValue )
        else:
            multRate = cmds.floatSliderGrp( self._slider2, q=1, v=1 )
            createJointOnCurveByLength( multRate, checkValue )
    
    
    
    def cmdOn(self , *args ):
        
        cmds.intSliderGrp( self._slider1, e=1, en=1 )
        cmds.floatSliderGrp( self._slider2, e=1, en=0 )


    def cmdOff(self, *args ):
        
        cmds.intSliderGrp( self._slider1, e=1, en=0 )
        cmds.floatSliderGrp( self._slider2, e=1, en=1 )
    
        
    
    def show(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title= self._title )
        
        columnWidth = self._width - 2
        sliderFirstWidth = columnWidth * 0.4
        sliderSecondWidth = 50
        sliderThirdWidth = columnWidth - sliderFirstWidth - sliderSecondWidth
        
        firstWidth = ( columnWidth -2 )/ 2
        secondWidth = ( columnWidth - 2 ) - firstWidth
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=2, co=[(1, 'left',30)], cw=[(1,firstWidth),(2,secondWidth)])
        cmds.radioCollection()
        radio1 = cmds.radioButton( l='By Number', sl=1, onc = self.cmdOn, ofc = self.cmdOff )
        radio2 = cmds.radioButton( l='By Length' )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        cmds.separator()
        slider1 = cmds.intSliderGrp( l='Num of Joint : ', f=1, 
                                    cw=[(1,sliderFirstWidth),(2,sliderSecondWidth),(3,sliderThirdWidth)],
                                    min=1, max=20, fmn=1, fmx=1000, v=5 )
        slider2 = cmds.floatSliderGrp( l='Mult Rate : ', f=1, 
                                    cw=[(1,sliderFirstWidth),(2,sliderSecondWidth),(3,sliderThirdWidth)],
                                    min=0.01, max=10, fmn=0.01, fmx=100, v=1.0, pre=2, en=0 )
        cmds.separator()
        cmds.rowColumnLayout( nc=2, cw=[( 1, 50 ), (2,columnWidth-52)])
        cmds.text( l='' )
        check = cmds.checkBox( l='Connect Distance Node', value =1 )
        cmds.setParent( '..' )
        cmds.text( l='', h=5 )
        cmds.button( l='Create', c=self.cmdCreate )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1,
                     w = self._width, h= self._height )
        cmds.showWindow( self._winName )
        
        self._slider1 = slider1
        self._slider2 = slider2
        self._radio1 = radio1
        self._radio2 = radio2
        self._check = check
    
    
def show():
    
    Window.show()



if __name__ == '__main__':
    show()
