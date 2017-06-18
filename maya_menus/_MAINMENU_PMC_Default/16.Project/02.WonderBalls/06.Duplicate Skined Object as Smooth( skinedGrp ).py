from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

firstGrp = sels[0]
secondGrp = pymel.core.duplicate( sels[0] )[0]

firstChildren = firstGrp.listRelatives( c=1, ad=1, type='transform' )
secondChildren = secondGrp.listRelatives( c=1, ad=1, type='transform' )

for i in range( len( firstChildren ) ):
    if not firstChildren[i].getShape(): continue
    pymel.core.polySmooth( secondChildren[i], mth=0, sdt=2, ovb=1, ofb=3, ofc=0, 
                           ost=1, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=0 )
    try:sgCmds.copyWeightToSmoothedMesh( firstChildren[i], secondChildren[i] )
    except:pass