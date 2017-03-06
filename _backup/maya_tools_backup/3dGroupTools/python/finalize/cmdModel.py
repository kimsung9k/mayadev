

uiCmd_OpenCreateBakeCamera = """import finalize.createBakeCamera.view
bakeCamUI = finalize.createBakeCamera.view.Window()
bakeCamUI.create()"""
    


uiCmd_OpenImportCacheUI ="""import finalize.importCache.cmdModel
finalize.importCache.cmdModel.openImportCacheUI()"""

    
    
uiCmd_OpenBuildCacheUI = """import finalize.buildCache.view
buildCacheUI = finalize.buildCache.view.Window()
buildCacheUI.create()"""
    
    

uiCmd_makeSelectedCacheSet ="""import maya.cmds as cmds
cmds.sets( n='cache_set' )"""