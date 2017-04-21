import maya.cmds as cmds
sels = cmds.ls( sl=1 )
joints = sels[:-1]
mesh = sels[-1]

def getNodeFromHistory( node, typ='skinCluster' ):
	hists = cmds.listHistory( node, pdo=1 )
	
	targetNodes = []
	for hist in hists:
		if cmds.nodeType( hist ) != typ: continue
		targetNodes.append( hist )
	return targetNodes

for jnt in joints:
    try:cmds.skinCluster(  getNodeFromHistory( mesh )[0], e=1, dr=10, lw=True, wt=0, ai=jnt )
    except:pass