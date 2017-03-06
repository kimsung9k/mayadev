'''
DJB_Character.FacePlus
Handles
    -Plotting of FacePlus data to a maya facial rig
'''
import maya.cmds as mayac
import maya.OpenMaya
import sys

def DJB_findBeforeSeparator(object, separatedWith):
    latestSeparator = object.rfind(separatedWith)
    return object[0:latestSeparator]

def identifyBestBlendshapeNode(group):
    bestBlendshapeNode = None
    bestNumShapes = 0
    blendShapeNodes = set()
    children = mayac.listRelatives(group, children=True, type="transform", fullPath=True)
    if children:
        for child in children:
            shapes = mayac.listRelatives(child, children=True, shapes=True, fullPath=True)
            if shapes:
                for shape in shapes:
                    cons = mayac.listConnections(shape, s=True, type="blendShape")
                    if cons:
                        for con in cons:
                            blendShapeNodes.add(con)
    if blendShapeNodes:
        blendShapeNodes = list(blendShapeNodes)
        for node in blendShapeNodes:
            node=str(node)
            aliases = mayac.aliasAttr(node, q=True)[::2]
            numAttrs = len(aliases)
            if numAttrs > bestNumShapes:
                hasAnim = False
                for attr in aliases:
                    cons = mayac.listConnections("%s.%s"%(node,attr))
                    if cons:
                        hasAnim=True
                        break
                if hasAnim:
                    bestNumShapes = numAttrs
                    bestBlendshapeNode = node
    return bestBlendshapeNode
    

class FacePlus:
    def __init__(self, Facial_CTRLs_Mover, incomingBlendShapes):
        self.FacialControlsMover = Facial_CTRLs_Mover
        self.incomingBlendShapes = incomingBlendShapes
        blendshapeNames = mayac.listAttr(self.incomingBlendShapes, r=True, w=True, u=True, k=True, v=True, m=True, s=True)
        self.iMouthOpen = None
        self.iMouthUp = None
        self.iMouthDown = None
        self.iSmileLeft = None
        self.iSmileRight = None
        self.iFrownLeft = None
        self.iFrownRight = None
        self.iUpperLipUp_Left = None
        self.iUpperLipUp_Right = None
        self.iLowerLipDown_Left = None
        self.iLowerLipDown_Right = None
        self.iMouthNarrow_Left = None
        self.iMouthNarrow_Right = None
        self.iMouthWhistle_Left = None
        self.iMouthWhistle_Right = None
        self.iSquint_Left = None
        self.iSquint_Right = None
        self.iEyesWide_Left = None
        self.iEyesWide_Right = None
        self.iBlink_Left = None
        self.iBlink_Right = None
        self.iScrunch_Left = None
        self.iScrunch_Right = None
        self.iBrowsDown_Left = None
        self.iBrowsDown_Right = None
        self.iBrowsUp_Left = None
        self.iBrowsUp_Right = None
        self.iBrowsIn_Left = None
        self.iBrowsIn_Right = None
        self.iBrowsOuter_Left = None
        self.iBrowsOuter_Right = None
        self.iMouth_Left = None
        self.iMouth_Right = None
        self.iEyesUp_Left = None
        self.iEyesUp_Right = None
        self.iEyesDown_Left = None
        self.iEyesDown_Right = None
        self.iEyesLeft_Left = None
        self.iEyesLeft_Right = None
        self.iEyesRight_Left = None
        self.iEyesRight_Right = None
        
        for bs in blendshapeNames:
            if "MouthOpen" in bs:
                self.iMouthOpen = bs
            elif "MouthUp" in bs:
                self.iMouthUp = bs
            elif "MouthDown" in bs:
                self.iMouthDown = bs
            elif "Smile_Left" in bs:
                self.iSmileLeft = bs
            elif "Smile_Right" in bs:
                self.iSmileRight = bs
            elif "Frown_Left" in bs:
                self.iFrownLeft = bs
            elif "Frown_Right" in bs:
                self.iFrownRight = bs
            elif "UpperLipUp_Left" in bs:
                self.iUpperLipUp_Left = bs
            elif "UpperLipUp_Right" in bs:
                self.iUpperLipUp_Right = bs
            elif "LowerLipDown_Left" in bs:
                self.iLowerLipDown_Left = bs
            elif "LowerLipDown_Right" in bs:
                self.iLowerLipDown_Right = bs
            elif "MouthNarrow_Left" in bs:
                self.iMouthNarrow_Left = bs
            elif "MouthNarrow_Right" in bs:
                self.iMouthNarrow_Right = bs
            elif "Whistle_NarrowAdjust_Left" in bs:
                self.iMouthWhistle_Left = bs
            elif "Whistle_NarrowAdjust_Right" in bs:
                self.iMouthWhistle_Right = bs
            elif "Squint_Left" in bs:
                self.iSquint_Left = bs
            elif "Squint_Right" in bs:
                self.iSquint_Right = bs
            elif "EyesWide_Left" in bs:
                self.iEyesWide_Left = bs
            elif "EyesWide_Right" in bs:
                self.iEyesWide_Right = bs
            elif "Blink_Left" in bs:
                self.iBlink_Left = bs
            elif "Blink_Right" in bs:
                self.iBlink_Right = bs
            elif "NoseScrunch_Left" in bs:
                self.iScrunch_Left = bs
            elif "NoseScrunch_Right" in bs:
                self.iScrunch_Right = bs
            elif "BrowsDown_Left" in bs:
                self.iBrowsDown_Left = bs
            elif "BrowsDown_Right" in bs:
                self.iBrowsDown_Right = bs
            elif "BrowsUp_Left" in bs:
                self.iBrowsUp_Left = bs
            elif "BrowsUp_Right" in bs:
                self.iBrowsUp_Right = bs
            elif "BrowsIn_Left" in bs:
                self.iBrowsIn_Left = bs
            elif "BrowsIn_Right" in bs:
                self.iBrowsIn_Right = bs
            elif "BrowsOuterLower_Left" in bs:
                self.iBrowsOuter_Left = bs
            elif "BrowsOuterLower_Right" in bs:
                self.iBrowsOuter_Right = bs
            elif "Midmouth_Left" in bs:
                self.iMouth_Left = bs
            elif "Midmouth_Right" in bs:
                self.iMouth_Right = bs
            elif "EyesUp_Left" in bs:
                self.iEyesUp_Left = bs
            elif "EyesUp_Right" in bs:
                self.iEyesUp_Right = bs
            elif "EyesDown_Left" in bs:
                self.iEyesDown_Left = bs
            elif "EyesDown_Right" in bs:
                self.iEyesDown_Right = bs
            elif "EyesLeft_Left" in bs:
                self.iEyesLeft_Left = bs
            elif "EyesLeft_Right" in bs:
                self.iEyesLeft_Right = bs
            elif "EyesRight_Left" in bs:
                self.iEyesRight_Left = bs
            elif "EyesRight_Right" in bs:
                self.iEyesRight_Right = bs
        prefix = DJB_findBeforeSeparator(self.FacialControlsMover, "Facial_CTRLs_Mover")
        self.Sync_CTRL = prefix + "Sync_CTRL"
        self.Smile_CTRL = prefix + "Smile_CTRL"
        self.MouthPosition_CTRL = prefix + "MouthPosition_CTRL"
        self.MouthNarrow_CTRL = prefix + "MouthNarrow_CTRL"
        self.Frown_CTRL = prefix + "Frown_CTRL"
        self.LowerLipDown_CTRL = prefix + "LowerLipDown_CTRL"
        self.UpperLipUp_CTRL = prefix + "UpperLipUp_CTRL"
        self.Whistle_CTRL = prefix + "Whistle_CTRL"
        self.NoseScrunch_CTRL = prefix + "NoseScrunch_CTRL"
        self.Squint_CTRL = prefix + "Squint_CTRL"
        self.Smile_CTRL1 = prefix + "Smile_CTRL1"
        self.LeftEye_CTRL = prefix + "LeftEye_CTRL"
        self.RightEye_CTRL = prefix + "RightEye_CTRL"
        self.LeftEyeBlink_CTRL = prefix + "LeftEyeBlink_CTRL"
        self.RightEyeBlink_CTRL = prefix + "RightEyeBlink_CTRL"
        self.LeftBrow_CTRL = prefix + "LeftBrow_CTRL"
        self.RightBrow_CTRL = prefix + "RightBrow_CTRL"
        self.LeftBrowOuterLower_CTRL = prefix + "LeftBrowOuterLower_CTRL"
        self.RightBrowOuterLower_CTRL = prefix + "RightBrowOuterLower_CTRL"
    
    def bake(self, iStartFrame, iEndFrame, startFrame):
        curIFrame = iStartFrame
        curFrame = startFrame
        while curFrame-startFrame <= iEndFrame-iStartFrame:
            #open and mouth up
            curOpen = mayac.getAttr(self.incomingBlendShapes + "." + self.iMouthOpen, t=curIFrame)
            curMouthUp = mayac.getAttr(self.incomingBlendShapes + "." + self.iMouthUp, t=curIFrame)
            curMouthDown = mayac.getAttr(self.incomingBlendShapes + "." + self.iMouthDown, t=curIFrame)
            curMouthPos = curMouthUp-curMouthDown
            if curOpen >= 0:
                mayac.setKeyframe(self.Sync_CTRL, at = "ty", t=[curFrame], v=curOpen*-1)
                mayac.setKeyframe(self.MouthPosition_CTRL, at = "ty", t=[curFrame], v=curMouthPos)
            else:
                if curMouthPos >= 0:
                    mayac.setKeyframe(self.Sync_CTRL, at = "ty", t=[curFrame], v=curMouthPos)
                    mayac.setKeyframe(self.MouthPosition_CTRL, at = "ty", t=[curFrame], v=0)
                else:
                    mayac.setKeyframe(self.Sync_CTRL, at = "ty", t=[curFrame], v=0)
                    mayac.setKeyframe(self.MouthPosition_CTRL, at = "ty", t=[curFrame], v=curMouthPos)
            #smile and narrow
            curSmileL = mayac.getAttr(self.incomingBlendShapes + "." + self.iSmileLeft, t=curIFrame)
            curSmileR = mayac.getAttr(self.incomingBlendShapes + "." + self.iSmileRight, t=curIFrame)
            curSmileLowest = curSmileL if curSmileL < curSmileR else curSmileR
            curNarrowL = mayac.getAttr(self.incomingBlendShapes + "." + self.iMouthNarrow_Left, t=curIFrame)
            curNarrowR = mayac.getAttr(self.incomingBlendShapes + "." + self.iMouthNarrow_Right, t=curIFrame)
            curNarrowLowest = curNarrowL if curNarrowL < curNarrowR else curNarrowR
            curSyncX = curSmileLowest-curNarrowLowest
            mayac.setKeyframe(self.Sync_CTRL, at = "tx", t=[curFrame], v=curSyncX)
            if curSyncX >= 0:
                #some smile taken away
                setKeyLR(self.incomingBlendShapes, curSmileL-curSyncX, curSmileR-curSyncX, curIFrame, curFrame, self.Smile_CTRL)
                setKeyLR(self.incomingBlendShapes, curNarrowL, curNarrowR, curIFrame, curFrame, self.MouthNarrow_CTRL)
            else:
                #some narrow taken away
                setKeyLR(self.incomingBlendShapes, curSmileL, curSmileR, curIFrame, curFrame, self.Smile_CTRL)
                setKeyLR(self.incomingBlendShapes, curNarrowL+curSyncX, curNarrowR+curSyncX, curIFrame, curFrame, self.MouthNarrow_CTRL)
            
            setKeyOpposites(self.incomingBlendShapes , self.iEyesWide_Left, self.iBlink_Left, curIFrame, curFrame, self.LeftEyeBlink_CTRL, "ty")
            setKeyOpposites(self.incomingBlendShapes , self.iEyesWide_Right, self.iBlink_Right, curIFrame, curFrame, self.RightEyeBlink_CTRL, "ty")
            
            
            #Brows
            setKeyOpposites(self.incomingBlendShapes , self.iBrowsUp_Left, self.iBrowsDown_Left, curIFrame, curFrame, self.LeftBrow_CTRL, "ty")
            setKeyOpposites(self.incomingBlendShapes , self.iBrowsUp_Right, self.iBrowsDown_Right, curIFrame, curFrame, self.RightBrow_CTRL, "ty")
            setKey(self.incomingBlendShapes , self.iBrowsIn_Left, curIFrame, curFrame, self.LeftBrow_CTRL, "tx", neg = -1)
            setKey(self.incomingBlendShapes , self.iBrowsIn_Right, curIFrame, curFrame, self.RightBrow_CTRL, "tx")
            setKey(self.incomingBlendShapes , self.iBrowsOuter_Left, curIFrame, curFrame, self.LeftBrowOuterLower_CTRL, "ty")
            setKey(self.incomingBlendShapes , self.iBrowsOuter_Right, curIFrame, curFrame, self.RightBrowOuterLower_CTRL, "ty")
            
            
            #Opposites
            setKeyOpposites(self.incomingBlendShapes , self.iMouth_Left, self.iMouth_Right, curIFrame, curFrame, self.MouthPosition_CTRL, "tx")
            
            #Basic LR Split Controls
            setKeyLR(self.incomingBlendShapes, self.iFrownRight, self.iFrownLeft, curIFrame, curFrame, self.Frown_CTRL, negative=True)
            setKeyLR(self.incomingBlendShapes, self.iLowerLipDown_Right, self.iLowerLipDown_Left, curIFrame, curFrame, self.LowerLipDown_CTRL, negative=True)
            setKeyLR(self.incomingBlendShapes, self.iUpperLipUp_Left, self.iUpperLipUp_Right, curIFrame, curFrame, self.UpperLipUp_CTRL)
            setKeyLR(self.incomingBlendShapes, self.iMouthWhistle_Left, self.iMouthWhistle_Right, curIFrame, curFrame, self.Whistle_CTRL)
            setKeyLR(self.incomingBlendShapes, self.iScrunch_Left, self.iScrunch_Right, curIFrame, curFrame, self.NoseScrunch_CTRL)
            setKeyLR(self.incomingBlendShapes, self.iSquint_Left, self.iSquint_Right, curIFrame, curFrame, self.Squint_CTRL)
            

            
            
            curFrame += 1
            curIFrame += 1
            
def setKey(ibs, iA, iFrame, curFrame, CTRL, att, neg = 1):
    cur = mayac.getAttr(ibs + "." + iA, t=iFrame)
    mayac.setKeyframe(CTRL, at = att , t=[curFrame], v=cur*neg)
       
def setKeyOpposites(ibs, iA, iB, iFrame, curFrame, CTRL, att):
    try:
        curA = mayac.getAttr(ibs + "." + iA, t=iFrame)
    except:
        print ibs
        print iA
        print iFrame
    curB = mayac.getAttr(ibs + "." + iB, t=iFrame)
    mayac.setKeyframe(CTRL, at = att , t=[curFrame], v=curA-curB)
    
def setKeyLR(ibs, iL, iR, iFrame, curFrame, CTRL, negative=False):
    curL = 0
    curR = 0
    try:
        curL = mayac.getAttr(ibs + "." + iL, t=iFrame)
        curR = mayac.getAttr(ibs + "." + iR, t=iFrame)
    except:
        curL = iL
        curR = iR
    if not negative:
        mayac.setKeyframe(CTRL, at = "tx", t=[curFrame], v=curL)
        mayac.setKeyframe(CTRL, at = "ty", t=[curFrame], v=curR)
    else:
        mayac.setKeyframe(CTRL, at = "tx", t=[curFrame], v=curL*-1)
        mayac.setKeyframe(CTRL, at = "ty", t=[curFrame], v=curR*-1)

     
    
class DJB_FacePlus_UI:
    def __init__(self):
        self.file1Dir = None
        self.name = "FacePlus_Hookup"
        self.title = "FacePlus_Hookup"

        # Begin creating the UI
        if (mayac.window(self.name, q=1, exists=1)): 
            mayac.deleteUI(self.name)
        self.window = mayac.window(self.name, title=self.title, menuBar=True)
        
        #forms
        mayac.columnLayout(adj=True)
        mayac.button(label = "Import Facial Animation File", c=self.importPressed)
        mayac.text( label='', align='left' )
        self.MoverTextField = mayac.textFieldButtonGrp( label='Facial Control Mover', text='Facial_CTRLs_Mover', buttonLabel='Load from selection', bc = self.MoverPressed, cw3=[200,200,100])
        self.incomingBlendshapeNode = mayac.textFieldButtonGrp( label='Incoming Animated BlendShape Node', text='Take_001:FBXASC000_ncl1_18', buttonLabel='Load from selection', bc = self.BSPressed,cw3=[200,200,100])
        mayac.text( label='', align='left' )
        mayac.text( label='', align='left' )
        self.AnimatedBSFrameRange = mayac.intFieldGrp( numberOfFields=2, label='Frames of Blendshapes to copy', value1=0, value2=1, cw3=[200,100,100])
        self.startFrameIntField = mayac.intFieldGrp( numberOfFields=1, label='Start Frame to copy to', value1=0, cw2=[200,100])
        mayac.text( label='', align='left' )
        mayac.text( label='', align='left' )
        self.bakeButton = mayac.button(label = "Copy To Rig", c=self.copyToRigPressed)
        mayac.text( label='', align='left' )
        
        mayac.window(self.window, e=1, w=500, h=200, sizeable = 1)
        mayac.showWindow(self.window)
        
    def importPressed(self, arg=None):
        mayac.Import()
        
    def MoverPressed(self):
        sel = mayac.ls(sl=True)
        if sel:
            if sel[0]:
                mayac.textFieldButtonGrp(self.MoverTextField, edit = True, text = sel[0])
            else:
                mayac.textFieldButtonGrp(self.MoverTextField, edit = True, text = "")
        else:
            mayac.textFieldButtonGrp(self.MoverTextField, edit = True, text = "")
            
    def BSPressed(self):
        sel = mayac.ls(sl=True)
        if sel:
            if sel[0]:
                mayac.textFieldButtonGrp(self.incomingBlendshapeNode, edit = True, text = sel[0])
            else:
                mayac.textFieldButtonGrp(self.incomingBlendshapeNode, edit = True, text = "")
        else:
            mayac.textFieldButtonGrp(self.incomingBlendshapeNode, edit = True, text = "")
            
    def copyToRigPressed(self, arg=None):
        mover = mayac.textFieldButtonGrp(self.MoverTextField, query = True, text = True)
        bsNode = mayac.textFieldButtonGrp(self.incomingBlendshapeNode, query = True, text = True)
        bsStart = mayac.intFieldGrp(self.AnimatedBSFrameRange, query=True, value1=True)
        bsEnd = mayac.intFieldGrp(self.AnimatedBSFrameRange, query=True, value2=True)
        copyToStart = mayac.intFieldGrp(self.startFrameIntField, query=True, value1=True)
        
        FacePlusInstance = FacePlus(mover, bsNode)
        FacePlusInstance.bake(bsStart,bsEnd,copyToStart)
        sys.stdout.write("Animation Copied.  \nYou may now delete imported facial animation file.")
        
def copyBlendshapeAnimationToRig(origAnimGrp, FacialMoverNode, startTime, endTime):
    blendShapeNode = identifyBestBlendshapeNode(origAnimGrp)
    if blendShapeNode:
        FacePlusInstance = FacePlus(FacialMoverNode, blendShapeNode)
        FacePlusInstance.bake(startTime,endTime,startTime)

if __name__ == "__main__":
    DJB_FacePlus_UI_Instance = DJB_FacePlus_UI()