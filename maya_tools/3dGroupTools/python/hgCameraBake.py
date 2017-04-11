import maya.cmds as cmds
import os, time, socket


def setClipboardData( text ):
    pass

def tearOffPanel():
    r = cmds.modelPanel(toc="modelPanel1")
    cmds.modelEditor(r, e=1, allObjects=0)

def doBake(maya=True, fbx=True):
    ##_ex_Atts = ["renderable"]
    _attrs = ["horizontalFilmAperture", "verticalFilmAperture", "focalLength", "lensSqueezeRatio", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "nearClipPlane", "farClipPlane",
    "filmFit", "filmFitOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "horizontalShake", "verticalShake", "shakeOverscanEnabled", "shakeOverscan", "preScale",
    "filmTranslateH", "filmTranslateV", "horizontalRollPivot", "verticalRollPivot", "filmRollValue", "filmRollOrder", "postScale", "depthOfField", "focusRegionScale"]

    if not (maya or fbx):
        return
    if not cmds.ls(sl=1):
        return
    src = cmds.ls(sl=1)[0]
    src_sh = cmds.listRelatives(src, s=True, f=True)[0]
    if not (cmds.objectType(src_sh) == "camera"):
        return
    trg = cmds.camera()[0]
    trg = cmds.rename(trg, src.split("|")[-1]+"_Bake")
    trg_sh = cmds.listRelatives(trg, s=True, f=True)[0]
    
    ##for at in cmds.listAttr(src_sh):
    for at in _attrs:
    ##if at in _ex_Atts: continue
        try:
            ##cmds.setAttr("%s.%s" % (src_sh, at), k=1)
            cmds.setAttr("%s.%s" % (trg_sh, at), k=1)
            cmds.setAttr("%s.%s" % (trg_sh, at), cmds.getAttr("%s.%s" % (src_sh, at)))
            cmds.connectAttr("%s.%s" % (src_sh, at), "%s.%s" % (trg_sh, at), f=1)
        except:
            pass
    
    cmds.pointConstraint(src, trg, offset=[0,0,0], weight=1)
    cmds.orientConstraint(src, trg, offset=[0,0,0], weight=1)
    cmds.setAttr(trg + ".rotateAxisX", cmds.getAttr(src + ".rotateAxisX"))
    cmds.setAttr(trg + ".rotateAxisY", cmds.getAttr(src + ".rotateAxisY"))
    cmds.setAttr(trg + ".rotateAxisZ", cmds.getAttr(src + ".rotateAxisZ"))
    
    _min, _max = cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)
    cmds.refresh(suspend=True)
    try:
        cmds.bakeResults(trg, sm=True, t=(_min, _max), sb=1, dic=True, pok=True, sac=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, cp=False, s=True)
    finally:
        cmds.refresh(suspend=False)
        cmds.refresh()
        cmds.delete(trg, constraints=1)
    try:
        a = cmds.listConnections(src_sh, s=0, d=1, c=1, p=1, scn=1, sh=1)[::2]
        b = cmds.listConnections(src_sh, s=0, d=1, c=1, p=1, scn=1, sh=1)[1::2]
        for i in range(len(a)):
            cmds.disconnectAttr(a[i], b[i])
    except:
        pass
    
    fpsDict = { 'game':"15p", 'film':"24p", 'pal':"25p", 'ntsc':"30p", 'show':"48p", 'palf':"50p", 'ntscf':"60p" }
    rnt = time.strftime('%Y-%m-%d %H:%M') + " " + socket.gethostname() + " " + "%d-%d" % (int(_min), int(_max)) + " " + fpsDict[cmds.currentUnit(q=1, t=1)] + "\n"
    curPath = cmds.file( q=1, sn=1 )
    fn = os.path.basename(os.path.splitext(curPath)[0])
    out = curPath.split("/ani/")[0]+"/reference/camera/anicam/"
    outFN = out+trg
    if not os.path.exists(out):
        os.makedirs(out)
    rntN = cmds.fileDialog2(fm=0, dir=outFN)
    if not rntN:
        return
    rntFN = os.path.splitext(rntN[0])[0]
    if maya: 
        cmds.file(rntFN, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1)
        rnt += rntFN+".mb\n"
    if fbx:
        cmds.file(rntFN, force=1, options="v=0;", typ="FBX export", pr=1, es=1)
        rnt += rntFN+".fbx\n"
    
    #print rnt
    ##setClipboardData(rnt)
    
    def showExportCamera():
        if cmds.window("exportCamera", ex=1):
            cmds.deleteUI("exportCamera")
            cmds.window("exportCamera")
            cmds.columnLayout( adjustableColumn=True )
            cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 100), (2, 100)] )
            mayaCB = cmds.checkBox(l="Maya", v=True)
            fbxCB = cmds.checkBox(l="FBX", v=True)
            cmds.setParent("..")
            #cmds.button(l="Tear off", c=lambda x:tearOffPanel())
            cmds.button(l="Export", c=lambda x:doBake(cmds.checkBox(mayaCB, q=1, v=1), cmds.checkBox(fbxCB, q=1, v=1)))
            cmds.showWindow()

    showExportCamera()


def bake( *args ):
    
    doBake()