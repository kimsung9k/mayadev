import pymel.core
from sgMaya import sgCmds, sgModel
import cPickle

selAttrs = pymel.core.channelBox( 'mainChannelBox', q=1, sma=1 )
sels = pymel.core.ls( sl=1 )

attrInfos = []
for attr in selAttrs:
    targetAttr = sels[-1].attr( attr )
    
    attrInfo = sgCmds.getAttrInfo( targetAttr )
    attrInfos.append( attrInfo )

pdr = cmds.about( pd=1 )

f = open( pdr + '/sgFileClipboard.txt', 'w' )
cPickle.dump( attrInfos, f )
f.close()