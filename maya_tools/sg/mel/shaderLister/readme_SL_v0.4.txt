Shader List v0.4, 25 feb 2006
=============================


Description
===========
It makes possible to quick connect or manage shaders within the Attribute Editor
by the ShaderList, DraggNDrop or Clipboard features.


Notes
=====
This script's UI may not work wery well on other OS than Windows or on other versions of
Maya (I use 7.0, but it should work on 6.x).
The problem is that the script uses colors, so parts of the UI may not be visible on these OS's (?).

If you have other maya version than 7 / 6.x, some AE*.mel files may cause errors (incompatibility issues).
I think the AEnew*.mel and AEreplace*.mel shouldn't cause errors (since they were not changed for ages :p),
so you could try copying only these files, to show SL and dragNDrop on most controls of AtributeEditor.

New to ShaderList 0.4
-rewrote the copy/paste feature
-removed the bookmarking feature (become obsolete because of the new copy/pase feature)
-code optimisations and rewrote some procs


Limitations
===========
* Drag and drop doesn't work if an AE control was dimmed and then undimmed.
* If you delete the destination shader in SL (the UI will modify)
and then undo, you can't do any connections and you either need to reopen SL or you can
simpy drag one attribute to the SL window. This can be simply fixed with a scriptJob, but
I don't think it worth consuming memory for this...


Quick Help
==========
To use, open the AE window and then you can do one of the following :
   <+> drag controls to copy data (colors, floats...), copy plugs or break connections
   <+> right click over controls (preferably near Hot Spot, see image included)
       and choose Scene Shaders to open the main SL window to make connections with
       any shader in your scene or to rename, select, delete shaders
   <+> right click on Hot Spot and use Copy/Paste to copy/paste data (colors, floats)
       to/from different buffers (with customizable number). Also you can paste the pluged
       node of your copied attributes (if you enable the Paste-Pluged option from the Copy/Paste
       settings window).
PS. Take a look at the image in the "_help_img" directory for better understanding :)

Features
========
   <+> you can make connections with the help of a filtered list of shaders
   <+> you can make connections by drag'n'dropping between AE controls
   <+> you can make connections with the Copy&Paste feature with Paste-Pluged mode Enabled
   <+> you can copy colors, floats etc. between attributes with dragNDrop
       or with the Copy/Paste features.
   <+> you can also quick rename, delete, select shaders from the scene within SL window
   <+> you can disconnect by dragging
   <+> SL has 6 filters : Materials, Textures, Utilities, Lights, SG+Cameras, All
   <+> these filters can also be turned to show mental ray shaders instead of maya's
   <+> nicer UI with integrated help frame and the UI space is well covered
   <+> you can now change the destination attr by dragging an attribute to the SL window


Install
=======
# copy |1| AE*.mel (from AEtemplates_mayaxx) in your scripts dir
       |2| ya_shaderList.mel and ya_dragNDrop to user scripts dir
# add "source ya_shaderList;source ya_dragNDrop.mel;" to userSetup.mel

# PS. There are 3 directories in the zip for maya 6.0, 6.5 and 7.0 containing
      AETemplates for maya 6, 6.5 and 7.0. Copy them accordly.
      Also, the scripts dir is tipicaly in My Documents\maya\x.x\scripts.


Uninstall
=========
If you have other maya version than 6.x or 7 and the script doesn't work, simply delete
the AE*.mel files and the two ya_*.mel from your scripts dir then remove-it from userSetup.


Me
==
To contact me use alayashu@yahoo.com
Please tell me your opinions about SL and what would you want in a future release

---------------------------------------------------------------------------------
For a detailed help, click on the help bar (gray) or right click over the list
in main Shader List window and choose Help. You should also read script header.
---------------------------------------------------------------------------------
