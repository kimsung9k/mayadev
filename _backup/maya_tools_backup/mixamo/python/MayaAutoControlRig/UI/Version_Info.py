'''
UI.Version_Info
Contains all of the info text
'''


VERSION = "1.6.0"


ABOUT_TEXT = """
MIXAMO Maya Auto Control Rig      
www.mixamo.com/c/maya-auto-control-rig   
Copyright Mixamo www.mixamo.com 2012-2015 Created by Dan Babcock
    Additional code by Paolo Dominici: Thanks for letting us integrate ZV Dynamics!

This script automatically creates a no-bake-necessary control rig for 
    editing MIXAMO motions and/or keyframing animation

    
Notes:
    Autodesk Maya 2009 or higher is required.
    Requires a character Autorigged by Mixamo

To Use:
    1) Save the MayaAutoControlRig folder into your maya scripts directory.
    2) Load up MayaShelfButton.py into the script editor and run (useful as a shelf button)

Noted Features:
    FK/IK legs and arms that follow animation data with no baking
    Keyable AnimDataMult attributes that exaggerate or ignore animation data
    The ability to bake animation to controls at any point in time
    The ability to clear controls at any point in time, preserving animation
    IK legs and arms can follow body motion
    Hands and Feet custom attributes
    Export baked FK skeleton
    Dynamic Joints / Joint Chains
"""

CHANGELOG_TEXT = """
Changes in 1.6.0:
    Automatic Creation of Facial Controls on FacePlus-compatible characters
        -Osipa style controls with sync/etc
        -Eye rotation and aim control
        -Transfer of any existing facial animation data to the control rig on "Import Animation to Control Rig"
        -Export of facial blendShape animation (must have export with mesh checked)
            *works only on non-referenced rigs
    Script Refactor: Part 1
        -Separated sections of the script for easier upkeep
        -Script must now be installed instead of just loaded into script editor
    Exported Meshes now go back to bind pose before being created
    Simplified Import Animation to Rig process
    Separate Batcher sub-tabs for importing and exporting
Changes in 1.5.0:
    Fixed bug with mesh export
    Blendshape animation now exports with "Export with Mesh" 
        *Only works on non-referenced rigs - needs to disconnect and reconnect attributes
    Fixed bug in IK creation
    Removed extraneous code
    Added option to remove end joints on export
Changes in 1.04d:
    Fix for no finger joints at all
Changes in 1.04c:
    Added support for characters with only one spine joint
    Fixed some namespace issues
    Extra Joints exports now have translates unlocked
Changes in 1.04b:
    Added handling of meshes (usually blendShapes) where 
      the shape node had the same name as the transform
Changes in 1.04a:
    Added support for dynamic joints and joint chains! 
      (integrated ZV Dynamics by Paolo Dominici)
    Added utilities for recreating infonodes 
    Fixed application of namespace on export joints when 
      namespace is not present in the scene
    Reworked UI
    Batching functionality
"""