from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
for sel in sels:
    if sel.nodeType() != 'joint': continue
    try:sel.jo.set( 0,0,0 )
    except:pass