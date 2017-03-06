'''
Utils.ZV_Dynamics
    code by Paolo Dominici, edits by Dan Babcock to fit into the AutoControlRig system
'''
import maya.cmds as mayac

def particleMethod(obj, weight=0.5, conserve=1.0, transfShapes=False):
    return _particleDyn(obj, weight, conserve, transfShapes, False)

def nParticleMethod(obj, weight=0.5, conserve=1.0, transfShapes=False):
    return _particleDyn(obj, weight, conserve, transfShapes, True)

def _particleDyn(obj, weight, conserve, transfShapes, nucleus):
    "Metodo generico di dinamica basata sulla particella"
    c = obj
    
    cNoPath = c[c.rfind("|")+1:]
    dynName = cNoPath + "_DYN"
    partName = cNoPath + "_INIT"
    dynLocName = cNoPath + "_DYN_LOC"
    statLocName = cNoPath + "_STAT_LOC"
    revName = cNoPath + "_REV"
    exprName = cNoPath + "_Expression"
    octName = cNoPath + "Oct"
    
    # leggo la posizione dell'oggetto
    pos = mayac.xform(c, q=True, rp=True, ws=True)
    
    # creo la particella
    if nucleus:
        partic, partShape = mayac.nParticle(n=partName, p=pos)
    else:
        partic, partShape = mayac.particle(n=partName, p=pos)
    
    partShape = "%s|%s" % (partic, partShape)
    
    # sposto il pivot
    mayac.xform(partic, piv=pos, ws=True)
    # aggiungo uno shape alla particella
    octName = drawOct(octName, r=0.25, pos=pos)
    octShapeName = mayac.listRelatives(octName, s=True, pa=True)[0]
    
    mayac.setAttr(octShapeName + ".overrideEnabled", True)
    mayac.setAttr(octShapeName + ".overrideColor", 13)
    mayac.parent([octShapeName, partic], s=True, r=True)
    mayac.delete(octName)
    
    # creo i locator
    statLocGrp = mayac.group("|" + mayac.spaceLocator(n=statLocName)[0], n="g_" + statLocName)
    dynLocGrp = mayac.group("|" + mayac.spaceLocator(n=dynLocName)[0], n="g_" + dynLocName)
    mayac.setAttr("|%s|%s.overrideEnabled" % (dynLocGrp, dynLocName), True)
    mayac.setAttr("|%s|%s.overrideColor" % (dynLocGrp, dynLocName), 6)
    
    # se e' attivo transfer shapes uso un gruppo invece di creare il cubetto
    if transfShapes:
        dyn = mayac.group(n=dynName, em=True)
    else:
        # cubetto colorato di blu orientato secondo l'oggetto
        dyn = drawCube(dynName, l=0.5)
        cubeShape = mayac.listRelatives(dyn, s=True, pa=True)[0]
        mayac.setAttr(cubeShape + ".overrideEnabled", True)        # colore
        mayac.setAttr(cubeShape + ".overrideColor", 6)
    
    # ruoto il cubetto e i locator (molto + carino)
    mayac.xform(["|" + statLocGrp, "|" + dynLocGrp, dyn], ro=mayac.xform(c, q=True, ro=True, ws=True), ws=True)
    mayac.xform(["|" + statLocGrp, "|" + dynLocGrp, dyn], t=pos, ws=True)
    dyn = mayac.parent([dyn, c])[0]
    mayac.makeIdentity(dyn, apply=True)                        # in questo modo il cubo assume le coordinate dell'oggetto pur essendo posizionato nel suo pivot
    
    # parento dyn allo stesso parente dell'oggetto
    parentObj = mayac.listRelatives(c, p=True, pa=True)
    if parentObj:
        dyn = mayac.parent([dyn, parentObj[0]])[0]
    else:
        dyn = mayac.parent(dyn, w=True)[0]
    c = mayac.parent([c, dyn])[0]
    
    mayac.parent(["|" + statLocGrp, "|" + dynLocGrp, dyn])
    
    # aggiorna i nomi con i percorsi
    statLocGrp = "%s|%s" % (dyn, statLocGrp)
    dynLocGrp = "%s|%s" % (dyn, dynLocGrp)
    statLoc = "%s|%s" % (statLocGrp, statLocName)
    dynLoc = "%s|%s" % (dynLocGrp, dynLocName)
    
    # goal particella-loc statico
    mayac.goal(partic, g=statLoc, utr=True, w=weight)
    
    # nascondo locator
    mayac.hide([statLocGrp, dynLocGrp])
    
    # rendo template la particella
    mayac.setAttr(partShape + '.template', True)
    
    # aggiungo l'attributo di velocita'
    mayac.addAttr(c, ln="info", at="enum", en=" ", keyable=True)
    mayac.setAttr(c + ".info", l=True)
    mayac.addAttr(c, ln="velocity", at="double3")
    mayac.addAttr(c, ln="velocityX", at="double", p="velocity", k=True)
    mayac.addAttr(c, ln="velocityY", at="double", p="velocity", k=True)
    mayac.addAttr(c, ln="velocityZ", at="double", p="velocity", k=True)

    # point oggetto tra i locator statico e dinamico
    pc = mayac.pointConstraint(statLoc, dynLoc, c, n=cNoPath + "_PC")[0]
    mayac.addAttr(dyn, ln="settings", at="enum", en=" ", keyable=True)
    mayac.setAttr(dyn + ".settings", l=True)
    mayac.addAttr(dyn, ln="dynamicsBlend", at="double", min=0.0, max=1.0, dv=1.0, keyable=True)
    mayac.addAttr(dyn, ln="weight", at="double", min=0.0, max=1.0, dv=weight, keyable=True)
    mayac.addAttr(dyn, ln="conserve", at="double", min=0.0, max=1.0, dv=conserve, keyable=True)
    rev = mayac.createNode("reverse", n=revName)
    mayac.connectAttr(dyn + ".dynamicsBlend", pc + ".w1")
    mayac.connectAttr(dyn + ".dynamicsBlend", rev + ".inputX")
    mayac.connectAttr(rev + ".outputX", pc + ".w0")
    mayac.connectAttr(dyn + ".weight", partShape + ".goalWeight[0]")
    mayac.connectAttr(dyn + ".conserve", partShape + ".conserve")
    # locco il point constraint
    [mayac.setAttr("%s.%s" % (pc, s), l=True) for s in ["offsetX", "offsetY", "offsetZ", "w0", "w1", "nodeState"]]
    # locco il reverse
    [mayac.setAttr("%s.%s" % (revName, s), l=True) for s in ["inputX", "inputY", "inputZ"]]
    
    # nParticle
    if nucleus:
        nucleusNode = mayac.listConnections(partShape + ".currentState")[0]
        mayac.setAttr(nucleusNode + '.gravity', 0.0)
        
        expr = """// rename if needed
string $dynHandle = "%s";
string $particleObject = "%s";
string $dynLocator = "%s";

undoInfo -swf 0;
$ast = `playbackOptions -q -ast`;
if (`currentTime -q` - $ast < 2) {
//    %s.startFrame = $ast;                        // remove it if you don't want to change nucleus start time
    $destPiv = `xform -q -rp -ws $dynHandle`;
    $origPiv = `xform -q -rp -ws $particleObject`;
    xform -t ($destPiv[0]-$origPiv[0]) ($destPiv[1]-$origPiv[1]) ($destPiv[2]-$origPiv[2]) -r -ws $particleObject;
}

$zvPos = `getParticleAttr -at worldPosition ($particleObject + ".pt[0]")`;
$currUnit = `currentUnit -q -linear`;
if ($currUnit != "cm") {
    $zvPos[0] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[0])`;
    $zvPos[1] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[1])`;
    $zvPos[2] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[2])`;
}
xform -a -ws -t $zvPos[0] $zvPos[1] $zvPos[2] $dynLocator;
$zvVel = `getParticleAttr -at velocity ($particleObject + ".pt[0]")`;        // velocity relative to the particleObject
%s.velocityX = $zvVel[0];
%s.velocityY = $zvVel[1];
%s.velocityZ = $zvVel[2];
undoInfo -swf 1;""" % (dyn, partic, dynLocName, nucleusNode, c, c, c)
    
    # particella standard
    else:
        mayac.setAttr(partic + ".visibility", False)
        expr = """// rename if needed
string $dynHandle = "%s";
string $particleObject = "%s";
string $dynLocator = "%s";

undoInfo -swf 0;
$ast = `playbackOptions -q -ast`;
if (`currentTime -q` - $ast < 2) {
    %s.startFrame = $ast;
    $destPiv = `xform -q -rp -ws $dynHandle`;
    $origPiv = `xform -q -rp -ws $particleObject`;
    xform -t ($destPiv[0]-$origPiv[0]) ($destPiv[1]-$origPiv[1]) ($destPiv[2]-$origPiv[2]) -r -ws $particleObject;
}

$zvPos = `getParticleAttr -at worldPosition ($particleObject + ".pt[0]")`;
$currUnit = `currentUnit -q -linear`;
if ($currUnit != "cm") {
    $zvPos[0] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[0])`;
    $zvPos[1] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[1])`;
    $zvPos[2] = `convertUnit -f "cm" -t $currUnit ((string)$zvPos[2])`;
}
xform -a -ws -t $zvPos[0] $zvPos[1] $zvPos[2] $dynLocator;
$zvVel = `getParticleAttr -at velocity ($particleObject + ".pt[0]")`;        // velocity relative to the particleObject
%s.velocityX = $zvVel[0];
%s.velocityY = $zvVel[1];
%s.velocityZ = $zvVel[2];
undoInfo -swf 1;""" % (dyn, partic, dynLocName, partShape, c, c, c)
    
    # crea l'espressione
    mayac.expression(n=exprName, s=expr)
    
    # se il check e' attivo trasferisci le geometrie nel nodo dinamico
    if transfShapes:
        shapes = mayac.listRelatives(c, s=True, pa=True)
        if shapes:
            mayac.parent(shapes + [dyn], r=True, s=True)
    
    # locks
    [mayac.setAttr(partic + s, k=False, cb=True) for s in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v", ".startFrame"]]
    
    return dyn

def drawOct(name, r=1.0, pos=(0.0, 0.0, 0.0)):
    p = [(s[0]+pos[0], s[1]+pos[1], s[2]+pos[2]) for s in [(0, 0, r), (r, 0, 0), (0, 0, -r), (-r, 0, 0), (0, -r, 0), (r, 0, 0), (0, r, 0), (-r, 0, 0), (0, 0, r), (0, r, 0), (0, 0, -r), (0, -r, 0), (0, 0, r)]]
    return mayac.rename(mayac.curve(d=1, p=p), name)

def drawCube(name, l=1.0, pos=(0.0, 0.0, 0.0)):
    r = l*0.5
    p = [(s[0]+pos[0], s[1]+pos[1], s[2]+pos[2]) for s in [(-r, r, r,), (r, r, r,), (r, r, -r,), (-r, r, -r,), (-r, -r, -r,), (r, -r, -r,), (r, -r, r,), (-r, -r, r,), (-r, r, r,), (-r, r, -r,), (-r, -r, -r,), (-r, -r, r,), (r, -r, r,), (r, r, r,), (r, r, -r,), (r, -r, -r,)]]
    return mayac.rename(mayac.curve(d=1, p=p), name)