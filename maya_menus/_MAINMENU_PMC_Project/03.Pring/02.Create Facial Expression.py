import maya.cmds as cmds

exString = '''int $xValue = %CTL%.translateX+.49999; 
int $yValue = %CTL%.translateY+.49999;

int $allValue = $xValue + $yValue * 6;
if( $allValue > %CTL%.maxIndex )
{
$allValue = %CTL%.maxIndex;
}

%TEXTURE%.frameExtension = $allValue;'''

eyeLCol= []
eyeLAlp= []
eyeRCol= []
eyeRAlp= []
mouthCol= []
mouthAlp= []

for fNode in cmds.ls( type='file' ):
    filePath = cmds.getAttr( fNode + '.fileTextureName' )
    fileName = filePath.split( '/' )[-1]
    if fileName.lower().find( 'eyel_col' ) != -1:
        eyeLCol.append( fNode )
    if fileName.lower().find( 'eyel_alp' ) != -1:
        eyeLAlp.append( fNode )
    if fileName.lower().find( 'eyer_col' ) != -1:
        eyeRCol.append( fNode )
    if fileName.lower().find( 'eyer_alp' ) != -1:
        eyeRAlp.append( fNode )
    if fileName.lower().find( 'mouth_col' ) != -1:
        mouthCol.append( fNode )
    if fileName.lower().find( 'mouth_alp' ) != -1:
        mouthAlp.append( fNode )

for ctl, colorTextures, alphaTextures in [ ['Ctl_Eye_L_',eyeLCol,eyeLAlp],['Ctl_Eye_R_',eyeRCol,eyeRAlp],['Ctl_Mouth',mouthCol,mouthAlp] ]:
    if not cmds.attributeQuery( 'maxIndex', node=ctl, ex=1 ):
        cmds.addAttr( ctl, ln='maxIndex', min=0, at='long' )
        cmds.setAttr( ctl + '.maxIndex', e=1, cb=1 )
        cmds.setAttr( ctl + '.maxIndex', 100 )
     
    allTextures = []
    allTextures += colorTextures
    allTextures += alphaTextures
    
    for texture in colorTextures:
        print texture
    	if not cmds.objExists( texture ): 
    		cmds.waning( "'%s' is not exists" % texture )
    		continue
        cmds.setAttr( texture + '.useFrameExtension', 1 )
        newString = exString.replace( '%CTL%', ctl ).replace( '%TEXTURE%', texture )
        expressionName= cmds.expression( s=newString,  o="", ae=1, uc='all', n= 'ex_' + ctl )
        try:
            cmds.connectAttr( expressionName + '.output[0]', texture + '.frameExtension', f=1 )
        except:
            print texture, expressionName