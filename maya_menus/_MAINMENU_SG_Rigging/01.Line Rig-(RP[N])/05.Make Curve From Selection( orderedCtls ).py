from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
lenSels = len( sels )
sgCmds.makeCurveFromSelection( *sels, d=min( [lenSels-1,3] ) )