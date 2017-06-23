import json
dataPath = 'A:/@@DEV@@/maya_tools/sg/datas/modifiedGpuObjs.txt'

f = open( dataPath, 'r' )
datas = json.load( f )
f.close()

for target, transform in datas:
    splits = target.split( ':' )
    name = splits[-1]
    trs = cmds.ls( tr=1 )
    targets = []
    for tr in trs:
        if tr.split( ':' )[-1] == name:
            targets.append( tr )
    for tr in targets:
        if tr.find( '_gpu' ) != -1: continue
        if name in ['sky1', 'sea', 'ground1', 'g']:
            cmds.setAttr( tr + '.t', *transform[:3] )
            cmds.setAttr( tr + '.r', *transform[3:6] )
            cmds.setAttr( tr + '.s', *transform[6:9] )
        else:
            cmds.move( transform[0], transform[1], transform[2], tr, r=1, ws=1 )
            cmds.rotate( transform[3], transform[4], transform[5], tr, r=1, ws=1 )
            cmds.scale( transform[6], transform[7], transform[8], tr, r=1, ws=1 ) 