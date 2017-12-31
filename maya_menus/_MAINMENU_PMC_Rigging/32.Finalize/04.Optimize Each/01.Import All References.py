import pymel.core
references = pymel.core.ls( type='reference' )
for refNode in references:
    try:cmds.file( importReference=1, referenceNode=refNode.name() )
    except:pass