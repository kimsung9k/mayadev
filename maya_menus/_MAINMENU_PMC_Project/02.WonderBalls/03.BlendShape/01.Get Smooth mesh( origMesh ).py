import pymel.core
sels = pymel.core.ls( sl=1 )

for sel in sels:
    duSel = pymel.core.duplicate( sel )[0]
    selShape = sel.getShape()
    duSelShape = duSel.getShape()
    duSel.setParent( w=1 )
    selShape.outMesh >> duSelShape.inMesh
    pymel.core.polySmooth( duSelShape, mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=1, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1 )
