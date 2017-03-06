uiCmd_OpenConfirmUI = """import confirm.confirmUI.view
import maya.cmds as cmds

confirmUi = confirm.confirmUI.view.DateAndPath_ui()
cmds.scriptJob( e=['NewSceneOpened', confirmUi.update ], p=confirmUi.win )
cmds.scriptJob( e=['SceneOpened', confirmUi.update], p=confirmUi.win )"""