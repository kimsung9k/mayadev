import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

src = sels[0]
dst = sels[1]

attrNames = pymel.core.channelBox( 'mainChannelBox', q=1, sma=1 )

for attrName in attrNames:
    sgCmds.copyAttribute( dst, src, attrName )
    src.attr( attrName ) >> dst.attr( attrName )