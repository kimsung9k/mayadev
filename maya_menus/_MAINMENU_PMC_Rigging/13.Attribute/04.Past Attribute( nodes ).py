import pymel.core
from sgMaya import sgCmds, sgModel
import cPickle

sels = pymel.core.ls( sl=1 )

pdr = cmds.about( pd=1 )
f = open( pdr + '/sgFileClipboard.txt', 'r' )
data = cPickle.load( f )
f.close()

for sel in sels:
    for attrInfo in data:
        sgCmds.createAttrByAttrInfo( attrInfo, sel )