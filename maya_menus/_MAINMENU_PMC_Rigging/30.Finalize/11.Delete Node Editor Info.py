import pymel.core
targets = pymel.core.ls( type='nodeGraphEditorInfo' )
pymel.core.delete( targets )