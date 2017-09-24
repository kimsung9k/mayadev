from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

src = sels[0]
trg = sels[1]

trg.rename( sgCmds.getOtherSideStr( src.shortName() ) )