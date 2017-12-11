import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

ctl = sels[0]
meshs = sels[1:]

sgCmds.addAttr( ctl, ln='smooth', min=0, max=2, cb=1, at='long' )

for mesh in meshs:
    meshShape = mesh.getShape()
    smoothNode = pymel.core.polySmooth( mesh, mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=1, ocr=0, 
                            dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, 
                            suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1 )[0]
    ctl.smooth >> smoothNode.divisions