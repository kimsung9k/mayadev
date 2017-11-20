from sgcommands import *
import pymel.core


class HumanRig:
    
    bodyColor = 18
    bodyRotColor = 23
    rootColor = 6
    worldColor = 22
    leftColor = 17
    rightColor = 13
    leftHandColor = 22
    rightHandColor = 20



        
        
def makeAimConstrainChild( lookTarget, pRotTarget, **options ):

    name = 'transform'
    if options.has_key( 'n' ):
        name = options.pop( 'n' )
        
    transform = pymel.core.createNode( 'transform', n=name )
    pymel.core.parent( transform, pRotTarget )
    pymel.core.setAttr( transform + '.t', 0,0,0 )
    pymel.core.aimConstraint( lookTarget, transform, **options )
    return transform.name()



class StdInfo:
    
    def __init__(self, name, position, rotation=[0,0,0] ):
        
        self.name   = name
        self.position = position
        self.rotation = rotation





class HumanStdInfo:
    
    Std_World = StdInfo( 'Std_World', [0.000, 0.000, 0.000] )
    Std_Root = StdInfo( 'Std_Root', [0.000, 9.458, 0.117] )
    Std_Back01 = StdInfo( 'Std_Back01', [0.000, 10.522, 0.198], [0.366, 0.000, 0.000] )
    Std_Back02 = StdInfo( 'Std_Back02', [0.000, 11.876, 0.201], [0.366, 0.000, 0.000] )
    Std_Chest = StdInfo( 'Std_Chest', [0.000, 13.073, 0.112] )
    Std_Neck = StdInfo( 'Std_Neck', [0.000, 15.225, -0.204] )
    Std_Head = StdInfo( 'Std_Head', [0.000, 16.339, 0.161] )
    Std_HeadEnd = StdInfo( 'Std_HeadEnd', [0.000, 18.255, 0.169] )
    
    Std_clavicle_L_ = StdInfo( 'Std_clavicle_L_', [0.221, 14.550, -0.148] )
    Std_Arm_L_00 = StdInfo( 'Std_Arm_L_00', [1.806, 14.458, -0.158] )
    Std_Arm_L_01 = StdInfo( 'Std_Arm_L_01', [3.298, 11.717, -0.040], [1.165, -4.865, -63.861] )
    Std_Arm_L_02 = StdInfo( 'Std_Arm_L_02', [4.219, 9.541, 0.309], [-0.409, -14.111, -71.342] )
    Std_Arm_L_PoleV = StdInfo( 'Std_Arm_L_PoleV', [3.303, 11.586, -3.773], [3.033, -4.865, -63.861] )
    Std_Leg_L_00 = StdInfo( 'Std_Leg_L_00', [0.983, 9.293, 0.136] )
    Std_Leg_L_01 = StdInfo( 'Std_Leg_L_01', [1.408, 5.002, -0.133], [-3.446, 4.294, -86.538] )
    Std_Leg_L_02 = StdInfo( 'Std_Leg_L_02', [1.491, 0.902, -0.495], [-10.139, 0.040, -89.776] )
    Std_Leg_L_PoleV = StdInfo( 'Std_Leg_L_PoleV', [1.508, 4.793, 3.989] )

    Std_Thumb_L_00 = StdInfo( 'Std_Thumb_L_00', [4.183, 9.285, 0.684], [16.574, -37.211, -102.483] )
    Std_Thumb_L_01 = StdInfo( 'Std_Thumb_L_01', [4.114, 8.973, 0.926], [13.699, -35.257, -101.244] )
    Std_Thumb_L_02 = StdInfo( 'Std_Thumb_L_02', [4.046, 8.647, 1.082], [13.775, -23.955, -101.397] )
    Std_Thumb_L_03 = StdInfo( 'Std_Thumb_L_03', [3.981, 8.314, 1.225], [1.178, -14.069, -77.854] )
    Std_Index_L_00 = StdInfo( 'Std_Index_L_00', [4.438, 9.203, 0.560], [-72.329, -20.859, -79.776] )
    Std_Index_L_01 = StdInfo( 'Std_Index_L_01', [4.567, 8.486, 0.837], [-75.189, -16.214, -93.073] )
    Std_Index_L_02 = StdInfo( 'Std_Index_L_02', [4.587, 8.211, 0.952], [-73.256, -19.404, -99.387] )
    Std_Index_L_03 = StdInfo( 'Std_Index_L_03', [4.542, 7.941, 1.049], [-73.256, -19.404, -99.387] )
    Std_Index_L_04 = StdInfo( 'Std_Index_L_04', [4.433, 7.674, 1.127], [0.000, -0.000, -0.000] )
    Std_Middle_L_00 = StdInfo( 'Std_Middle_L_00', [4.442, 9.148, 0.420], [-93.029, -11.415, -77.864] )
    Std_Middle_L_01 = StdInfo( 'Std_Middle_L_01', [4.607, 8.381, 0.578], [-92.849, -10.804, -91.487] )
    Std_Middle_L_02 = StdInfo( 'Std_Middle_L_02', [4.624, 8.059, 0.670], [-91.075, -16.488, -98.986] )
    Std_Middle_L_03 = StdInfo( 'Std_Middle_L_03', [4.575, 7.748, 0.763], [-91.075, -16.488, -98.986] )
    Std_Middle_L_04 = StdInfo( 'Std_Middle_L_04', [4.459, 7.448, 0.858], [0.000, -0.000, -0.000] )
    Std_Ring_L_00 = StdInfo( 'Std_Ring_L_00', [4.430, 9.122, 0.280], [-111.989, -3.644, -81.659] )
    Std_Ring_L_01 = StdInfo( 'Std_Ring_L_01', [4.545, 8.334, 0.331], [-111.133, -5.730, -88.911] )
    Std_Ring_L_02 = StdInfo( 'Std_Ring_L_02', [4.542, 8.012, 0.398], [-108.672, -15.761, -102.007] )
    Std_Ring_L_03 = StdInfo( 'Std_Ring_L_03', [4.477, 7.709, 0.485], [-108.672, -15.761, -102.007] )
    Std_Ring_L_04 = StdInfo( 'Std_Ring_L_04', [4.352, 7.425, 0.593], [0.000, -0.000, -0.000] )
    Std_Pinky_L_00 = StdInfo( 'Std_Pinky_L_00', [4.375, 9.097, 0.133], [-114.756, 3.501, -84.680] )
    Std_Pinky_L_01 = StdInfo( 'Std_Pinky_L_01', [4.441, 8.385, 0.089], [-128.173, 6.550, -98.649] )
    Std_Pinky_L_02 = StdInfo( 'Std_Pinky_L_02', [4.409, 8.105, 0.091], [-127.995, -8.866, -107.321] )
    Std_Pinky_L_03 = StdInfo( 'Std_Pinky_L_03', [4.329, 7.847, 0.133], [-127.995, -8.866, -107.321] )
    Std_Pinky_L_04 = StdInfo( 'Std_Pinky_L_04', [4.199, 7.610, 0.216], [0.000, -0.000, -0.000] )
    
    Std_clavicle_R_ = StdInfo( 'Std_clavicle_R_', [-0.221, 14.550, -0.148] )
    Std_FootPiv_L_ = StdInfo( 'Std_FootPiv_L_', [1.391, 0.045, -0.942], [0.000, 10.139, -0.000] )
    Std_FootIn_L_ = StdInfo( 'Std_FootIn_L_', [1.253, 0.018, 1.009], [0.000, 11.571, 0.000] )
    Std_FootOut_L_ = StdInfo( 'Std_FootOut_L_', [2.227, 0.018, 0.625], [0.000, 11.571, 0.000] )
    Std_Toe_L_End = StdInfo( 'Std_Toe_L_End', [1.925, 0.134, 1.567], [0.000, 11.571, 0.000] )
    Std_Toe_L_ = StdInfo( 'Std_Toe_L_', [1.765, 0.202, 0.860], [0.000, 11.571, 0.000] )
    
    Std_Arm_R_00 = StdInfo( 'Std_Arm_R_00', [-1.806, 14.458, -0.158] )
    Std_Arm_R_01 = StdInfo( 'Std_Arm_R_01', [-3.221, 11.576, -0.209], [-177.733, 4.865, 63.271] )
    Std_Arm_R_02 = StdInfo( 'Std_Arm_R_02', [-4.276, 9.553, 0.310], [186.034, 14.069, 77.854] )
    Std_Arm_R_PoleV = StdInfo( 'Std_Arm_R_PoleV', [-3.461, 11.497, -3.588], [3.033, 4.865, 63.861] )
    Std_Leg_R_00 = StdInfo( 'Std_Leg_R_00', [-0.975, 9.274, 0.136] )
    Std_Leg_R_01 = StdInfo( 'Std_Leg_R_01', [-1.451, 4.969, -0.151], [-177.578, -4.303, 86.477] )
    Std_Leg_R_02 = StdInfo( 'Std_Leg_R_02', [-1.491, 0.902, -0.495], [-190.076, 0.063, 87.698] )
    Std_Leg_R_PoleV = StdInfo( 'Std_Leg_R_PoleV', [-1.074, 4.793, 3.989] )
    
    Std_Thumb_R_00 = StdInfo( 'Std_Thumb_R_00', [-4.183, 9.285, 0.684], [-166.839, 37.211, 102.483] )
    Std_Thumb_R_01 = StdInfo( 'Std_Thumb_R_01', [-4.114, 8.973, 0.926], [-160.839, 35.257, 101.244] )
    Std_Thumb_R_02 = StdInfo( 'Std_Thumb_R_02', [-4.047, 8.643, 1.076], [-160.763, 23.955, 101.397] )
    Std_Thumb_R_03 = StdInfo( 'Std_Thumb_R_03', [-3.981, 8.314, 1.225], [-261.336, 17.208, 91.440] )
    Std_Index_R_00 = StdInfo( 'Std_Index_R_00', [-4.438, 9.203, 0.560], [-247.956, 20.859, 79.776] )
    Std_Index_R_01 = StdInfo( 'Std_Index_R_01', [-4.567, 8.486, 0.837], [-259.027, 20.763, 86.459] )
    Std_Index_R_02 = StdInfo( 'Std_Index_R_02', [-4.583, 8.200, 0.954], [105.430, 19.404, 99.387] )
    Std_Index_R_03 = StdInfo( 'Std_Index_R_03', [-4.536, 7.945, 1.044], [105.430, 19.404, 99.387] )
    Std_Index_R_04 = StdInfo( 'Std_Index_R_04', [-4.433, 7.674, 1.127], [-360.000, -0.000, 0.000] )
    Std_Middle_R_00 = StdInfo( 'Std_Middle_R_00', [-4.442, 9.148, 0.420], [82.930, 11.415, 77.864] )
    Std_Middle_R_01 = StdInfo( 'Std_Middle_R_01', [-4.607, 8.381, 0.578], [-272.224, 14.694, 84.617] )
    Std_Middle_R_02 = StdInfo( 'Std_Middle_R_02', [-4.617, 8.017, 0.686], [91.658, 16.488, 98.986] )
    Std_Middle_R_03 = StdInfo( 'Std_Middle_R_03', [-4.583, 7.748, 0.766], [91.658, 16.488, 98.986] )
    Std_Middle_R_04 = StdInfo( 'Std_Middle_R_04', [-4.459, 7.448, 0.858], [-360.000, -0.000, 0.000] )
    Std_Ring_R_00 = StdInfo( 'Std_Ring_R_00', [-4.430, 9.122, 0.280], [79.631, 3.644, 81.659] )
    Std_Ring_R_01 = StdInfo( 'Std_Ring_R_01', [-4.545, 8.334, 0.331], [-287.337, 7.024, 81.225] )
    Std_Ring_R_02 = StdInfo( 'Std_Ring_R_02', [-4.529, 8.018, 0.407], [76.824, 15.761, 102.007] )
    Std_Ring_R_03 = StdInfo( 'Std_Ring_R_03', [-4.464, 7.715, 0.495], [76.824, 15.761, 102.007] )
    Std_Ring_R_04 = StdInfo( 'Std_Ring_R_04', [-4.352, 7.425, 0.593], [-360.000, -0.000, 0.000] )
    Std_Pinky_R_00 = StdInfo( 'Std_Pinky_R_00', [-4.375, 9.097, 0.133], [72.311, -3.501, 84.680] )
    Std_Pinky_R_01 = StdInfo( 'Std_Pinky_R_01', [-4.441, 8.385, 0.089], [-311.012, -5.816, 90.892] )
    Std_Pinky_R_02 = StdInfo( 'Std_Pinky_R_02', [-4.405, 8.096, 0.089], [49.432, 8.866, 107.321] )
    Std_Pinky_R_03 = StdInfo( 'Std_Pinky_R_03', [-4.317, 7.853, 0.139], [49.432, 8.866, 107.321] )
    Std_Pinky_R_04 = StdInfo( 'Std_Pinky_R_04', [-4.199, 7.610, 0.216], [-360.000, -0.000, 0.000] )
    
    Std_FootPiv_R_ = StdInfo( 'Std_FootPiv_R_', [-1.393, 0.045, -0.943], [-0.000, -7.844, 0.000] )
    Std_FootIn_R_ = StdInfo( 'Std_FootIn_R_', [-1.247, 0.018, 1.017], [-0.000, -7.844, 0.000] )
    Std_FootOut_R_ = StdInfo( 'Std_FootOut_R_', [-2.222, 0.018, 0.622], [-0.000, -7.844, 0.000] )
    Std_Toe_R_End = StdInfo( 'Std_Toe_R_End', [-1.925, 0.043, 1.567], [-0.000, -7.844, 0.000] )
    Std_Toe_R_ = StdInfo( 'Std_Toe_R_', [-1.765, 0.202, 0.860], [-0.000, -7.844, 0.000] )




class HumanStdRig:
    
    def __init__(self):
        
        self.createStds()
        self.rigStds()
        self.rigStdJnts()
    
    
    
    def createStds(self):
        
        self.Std_Root = self.createStdElementFromInfo( HumanStdInfo.Std_Root )
        self.Std_Back01 = self.createStdElementFromInfo( HumanStdInfo.Std_Back01 )
        self.Std_Back02 = self.createStdElementFromInfo( HumanStdInfo.Std_Back02 )
        self.Std_Chest = self.createStdElementFromInfo( HumanStdInfo.Std_Chest )
        self.Std_Neck = self.createStdElementFromInfo( HumanStdInfo.Std_Neck )
        self.Std_Head = self.createStdElementFromInfo( HumanStdInfo.Std_Head )
        self.Std_HeadEnd = self.createStdElementFromInfo( HumanStdInfo.Std_HeadEnd )
        
        self.Std_clavicle_L_ = self.createStdElementFromInfo( HumanStdInfo.Std_clavicle_L_ )
        self.Std_Arm_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_L_00 )
        self.Std_Arm_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_L_01 )
        self.Std_Arm_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_L_02 )
        self.Std_Arm_L_PoleV = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_L_PoleV )
        
        self.Std_Leg_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_L_00 )
        self.Std_Leg_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_L_01 )
        self.Std_Leg_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_L_02 )
        self.Std_Leg_L_PoleV = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_L_PoleV )
        
        self.Std_Thumb_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_L_00 )
        self.Std_Thumb_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_L_01 )
        self.Std_Thumb_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_L_02 )
        self.Std_Thumb_L_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_L_03 )
        self.Std_Index_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_L_00 )
        self.Std_Index_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_L_01 )
        self.Std_Index_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_L_02 )
        self.Std_Index_L_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_L_03 )
        self.Std_Index_L_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_L_04 )
        self.Std_Middle_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_L_00 )
        self.Std_Middle_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_L_01 )
        self.Std_Middle_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_L_02 )
        self.Std_Middle_L_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_L_03 )
        self.Std_Middle_L_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_L_04 )
        self.Std_Ring_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_L_00 )
        self.Std_Ring_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_L_01 )
        self.Std_Ring_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_L_02 )
        self.Std_Ring_L_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_L_03 )
        self.Std_Ring_L_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_L_04 )
        self.Std_Pinky_L_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_L_00 )
        self.Std_Pinky_L_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_L_01 )
        self.Std_Pinky_L_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_L_02 )
        self.Std_Pinky_L_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_L_03 )
        self.Std_Pinky_L_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_L_04 )
        
        self.Std_FootPiv_L_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootPiv_L_ )
        self.Std_FootIn_L_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootIn_L_ )
        self.Std_FootOut_L_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootOut_L_ )
        self.Std_Toe_L_End = self.createStdElementFromInfo( HumanStdInfo.Std_Toe_L_End )
        self.Std_Toe_L_ = self.createStdElementFromInfo( HumanStdInfo.Std_Toe_L_ )
        
        self.Std_clavicle_R_ = self.createStdElementFromInfo( HumanStdInfo.Std_clavicle_R_ )
        self.Std_Arm_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_R_00 )
        self.Std_Arm_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_R_01 )
        self.Std_Arm_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_R_02 )
        self.Std_Arm_R_PoleV = self.createStdElementFromInfo( HumanStdInfo.Std_Arm_R_PoleV )
        
        self.Std_Leg_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_R_00 )
        self.Std_Leg_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_R_01 )
        self.Std_Leg_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_R_02 )
        self.Std_Leg_R_PoleV = self.createStdElementFromInfo( HumanStdInfo.Std_Leg_R_PoleV )
        
        self.Std_Thumb_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_R_00 )
        self.Std_Thumb_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_R_01 )
        self.Std_Thumb_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_R_02 )
        self.Std_Thumb_R_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Thumb_R_03 )
        self.Std_Index_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_R_00 )
        self.Std_Index_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_R_01 )
        self.Std_Index_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_R_02 )
        self.Std_Index_R_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_R_03 )
        self.Std_Index_R_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Index_R_04 )
        self.Std_Middle_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_R_00 )
        self.Std_Middle_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_R_01 )
        self.Std_Middle_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_R_02 )
        self.Std_Middle_R_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_R_03 )
        self.Std_Middle_R_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Middle_R_04 )
        self.Std_Ring_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_R_00 )
        self.Std_Ring_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_R_01 )
        self.Std_Ring_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_R_02 )
        self.Std_Ring_R_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_R_03 )
        self.Std_Ring_R_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Ring_R_04 )
        self.Std_Pinky_R_00 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_R_00 )
        self.Std_Pinky_R_01 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_R_01 )
        self.Std_Pinky_R_02 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_R_02 )
        self.Std_Pinky_R_03 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_R_03 )
        self.Std_Pinky_R_04 = self.createStdElementFromInfo( HumanStdInfo.Std_Pinky_R_04 )
        
        self.Std_FootPiv_R_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootPiv_R_ )
        self.Std_FootIn_R_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootIn_R_ )
        self.Std_FootOut_R_ = self.createStdElementFromInfo( HumanStdInfo.Std_FootOut_R_ )
        self.Std_Toe_R_End = self.createStdElementFromInfo( HumanStdInfo.Std_Toe_R_End )
        self.Std_Toe_R_ = self.createStdElementFromInfo( HumanStdInfo.Std_Toe_R_ )
    
    
    
    def rigStds(self):
        
        #chest rig
        self.LookAtStd_Root = pymel.core.ls( makeLookAtChild( self.Std_Chest, self.Std_Root, direction=[0,1,0] ) )[0]
        self.LookAtStd_Root.rename( 'LookAtStd_Root' )
        pymel.core.parent( self.Std_Back01, self.Std_Back02, self.LookAtStd_Root )
        
        self.PStd_Back01 = pymel.core.ls( makeParent( self.Std_Back01 ) )[0]
        self.PStd_Back02 = pymel.core.ls( makeParent( self.Std_Back02 ) )[0]
        
        stdBack00Pos = self.Std_Back01.wm.get()
        stdBack01Pos = self.Std_Back02.wm.get()
        
        dcmp = pymel.core.ls( getLocalDecomposeMatrix( self.Std_Chest, self.LookAtStd_Root ).name() )[0]
        multiplyNode1 = pymel.core.createNode( 'multiplyDivide' )
        multiplyNode2 = pymel.core.createNode( 'multiplyDivide' )
        dcmp.ot >> multiplyNode1.input1
        dcmp.ot >> multiplyNode2.input1
        multiplyNode1.input2.set( *[ 0.3333 for i in range( 3 ) ] )
        multiplyNode2.input2.set( *[ 0.6666 for i in range( 3 ) ] )
        
        multiplyNode1.output >> self.PStd_Back01.t
        multiplyNode2.output >> self.PStd_Back02.t
        
        pymel.core.xform( self.Std_Back01, ws=1, matrix= stdBack00Pos )
        pymel.core.xform( self.Std_Back02, ws=1, matrix= stdBack01Pos )
        
        
        #arm rig_L_
        self.LookAtStd_Arm_L_00 = pymel.core.ls( makeAimConstrainChild( self.Std_Arm_L_02, self.Std_Arm_L_00, aim=[1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Arm_L_PoleV ) )[0]
        self.LookAtStd_Root.rename( 'LookAtStd_Arm_L_00' )
        self.PStd_Arm_L_01 = pymel.core.createNode( 'transform', n='PStd_Arm_L_01' )
        self.Std_Arm_L_01_Moved = pymel.core.createNode( 'transform', n='Std_Arm_L_01_Moved' )
        self.Std_Arm_L_01_Moved.ty.setLocked(1)
        self.Std_Arm_L_01.tx >> self.Std_Arm_L_01_Moved.tx
        self.Std_Arm_L_01.tz >> self.Std_Arm_L_01_Moved.tz
        pymel.core.parent( self.Std_Arm_L_01_Moved, self.PStd_Arm_L_01 )
        pymel.core.parent( self.PStd_Arm_L_01, self.LookAtStd_Arm_L_00 )
        dcmp = pymel.core.ls( getLocalDecomposeMatrix( self.Std_Arm_L_02, self.LookAtStd_Arm_L_00 ).name() )[0]
        multiplyNode = pymel.core.createNode( 'multiplyDivide' )
        dcmp.ot >> multiplyNode.input1
        multiplyNode.input2.set( .5, .5, .5 )
        multiplyNode.output >> self.PStd_Arm_L_01.t
        self.PStd_Arm_L_01.r.set( 0,0,0 )
        pymel.core.parent( self.Std_Arm_L_01, self.PStd_Arm_L_01 )
        pymel.core.parent( self.Std_Arm_L_PoleV, self.Std_Arm_L_00 )
        
        
        #arm rig_R_
        self.LookAtStd_Arm_R_00 = pymel.core.ls( makeAimConstrainChild( self.Std_Arm_R_02, self.Std_Arm_R_00, aim=[-1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Arm_R_PoleV ) )[0]
        self.LookAtStd_Root.rename( 'LookAtStd_Arm_R_00' )
        self.PStd_Arm_R_01 = pymel.core.createNode( 'transform', n='PStd_Arm_R_01' )
        self.Std_Arm_R_01_Moved = pymel.core.createNode( 'transform', n='Std_Arm_R_01_Moved' )
        self.Std_Arm_R_01_Moved.ty.setLocked(1)
        self.Std_Arm_R_01.tx >> self.Std_Arm_R_01_Moved.tx
        self.Std_Arm_R_01.tz >> self.Std_Arm_R_01_Moved.tz
        pymel.core.parent( self.Std_Arm_R_01_Moved, self.PStd_Arm_R_01 )
        pymel.core.parent( self.PStd_Arm_R_01, self.LookAtStd_Arm_R_00 )
        dcmp = pymel.core.ls( getLocalDecomposeMatrix( self.Std_Arm_R_02, self.LookAtStd_Arm_R_00 ).name() )[0]
        multiplyNode = pymel.core.createNode( 'multiplyDivide' )
        dcmp.ot >> multiplyNode.input1
        multiplyNode.input2.set( .5, .5, .5 )
        multiplyNode.output >> self.PStd_Arm_R_01.t
        self.PStd_Arm_R_01.r.set( 0,0,0 )
        pymel.core.parent( self.Std_Arm_R_01, self.PStd_Arm_R_01 )
        pymel.core.parent( self.Std_Arm_R_PoleV, self.Std_Arm_R_00 )
        
        
        #leg rig_L_
        self.LookAtStd_Leg_L_00 = pymel.core.ls( makeAimConstrainChild( self.Std_Leg_L_02, self.Std_Leg_L_00, aim=[1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Leg_L_PoleV ) )[0]
        self.LookAtStd_Root.rename( 'LookAtStd_Leg_L_00' )
        self.PStd_Leg_L_01 = pymel.core.createNode( 'transform', n='PStd_Leg_L_01' )
        self.Std_Leg_L_01_Moved = pymel.core.createNode( 'transform', n='Std_Leg_L_01_Moved' )
        self.Std_Leg_L_01_Moved.ty.setLocked(1)
        self.Std_Leg_L_01.tx >> self.Std_Leg_L_01_Moved.tx
        self.Std_Leg_L_01.tz >> self.Std_Leg_L_01_Moved.tz
        pymel.core.parent( self.Std_Leg_L_01_Moved, self.PStd_Leg_L_01 )
        pymel.core.parent( self.PStd_Leg_L_01, self.LookAtStd_Leg_L_00 )
        dcmp = pymel.core.ls( getLocalDecomposeMatrix( self.Std_Leg_L_02, self.LookAtStd_Leg_L_00 ).name() )[0]
        multiplyNode = pymel.core.createNode( 'multiplyDivide' )
        dcmp.ot >> multiplyNode.input1
        multiplyNode.input2.set( .5, .5, .5 )
        multiplyNode.output >> self.PStd_Leg_L_01.t
        self.PStd_Leg_L_01.r.set( 0,0,0 )
        pymel.core.parent( self.Std_Leg_L_01, self.PStd_Leg_L_01 )
        pymel.core.parent( self.Std_Leg_L_PoleV, self.Std_Leg_L_00 )
        
        
        #leg rig_R_
        self.LookAtStd_Leg_R_00 = pymel.core.ls( makeAimConstrainChild( self.Std_Leg_R_02, self.Std_Leg_R_00, aim=[-1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Leg_R_PoleV ) )[0]
        self.LookAtStd_Root.rename( 'LookAtStd_Leg_R_00' )
        self.PStd_Leg_R_01 = pymel.core.createNode( 'transform', n='PStd_Leg_R_01' )
        self.Std_Leg_R_01_Moved = pymel.core.createNode( 'transform', n='Std_Leg_R_01_Moved' )
        self.Std_Leg_R_01_Moved.ty.setLocked(1)
        self.Std_Leg_R_01.tx >> self.Std_Leg_R_01_Moved.tx
        self.Std_Leg_R_01.tz >> self.Std_Leg_R_01_Moved.tz
        pymel.core.parent( self.Std_Leg_R_01_Moved, self.PStd_Leg_R_01 )
        pymel.core.parent( self.PStd_Leg_R_01, self.LookAtStd_Leg_R_00 )
        dcmp = pymel.core.ls( getLocalDecomposeMatrix( self.Std_Leg_R_02, self.LookAtStd_Leg_R_00 ).name() )[0]
        multiplyNode = pymel.core.createNode( 'multiplyDivide' )
        dcmp.ot >> multiplyNode.input1
        multiplyNode.input2.set( .5, .5, .5 )
        multiplyNode.output >> self.PStd_Leg_R_01.t
        self.PStd_Leg_R_01.r.set( 0,0,0 )
        pymel.core.parent( self.Std_Leg_R_01, self.PStd_Leg_R_01 )
        pymel.core.parent( self.Std_Leg_R_PoleV, self.Std_Leg_R_00 )
        
        #foot rig_L_
        pymel.core.parent( self.Std_FootPiv_L_, self.Std_FootIn_L_, self.Std_FootOut_L_, self.Std_Toe_L_, self.Std_Toe_L_End, self.Std_Leg_L_02 )
        
        #foot rig_R_
        pymel.core.parent( self.Std_FootPiv_R_, self.Std_FootIn_R_, self.Std_FootOut_R_, self.Std_Toe_R_, self.Std_Toe_R_End, self.Std_Leg_R_02 )
        
        #hand rig
        thumbList_L_ = [ self.Std_Thumb_L_00, self.Std_Thumb_L_01, self.Std_Thumb_L_02, self.Std_Thumb_L_03, self.Std_Arm_L_02 ]
        thumbList_R_ = [ self.Std_Thumb_R_00, self.Std_Thumb_R_01, self.Std_Thumb_R_02, self.Std_Thumb_R_03, self.Std_Arm_R_02 ]
        
        for Std_Thumb_00, Std_Thumb_01, Std_Thumb_02, Std_Thumb_03, Std_Arm_02 in [ thumbList_L_, thumbList_R_ ]:
            side = '_L_'
            direction = [1,0,0]
            if Std_Thumb_00.find( '_R_' ) != -1: 
                side = '_R_'
                direction = [-1,0,0]
            pymel.core.parent( Std_Thumb_00, Std_Thumb_01, Std_Thumb_03, Std_Arm_02 )
            LookAtStd_Thumb_01 = pymel.core.ls( makeLookAtChild( Std_Thumb_03, Std_Thumb_01, direction=direction ) )[0]
            LookAtStd_Thumb_01.rename( 'LookAtStd_Thumb%s01' % side )
            PStd_Thumb_02 = pymel.core.createNode( 'transform', n='P' + Std_Thumb_02.name() )
            pymel.core.parent( PStd_Thumb_02, LookAtStd_Thumb_01 )
            dcmp = pymel.core.ls( getLocalDecomposeMatrix( Std_Thumb_03, LookAtStd_Thumb_01 ).name() )[0]
            multiplyNode = pymel.core.createNode( 'multiplyDivide' )
            dcmp.ot >> multiplyNode.input1
            multiplyNode.input2.set( .5, .5, .5 )
            multiplyNode.output >> PStd_Thumb_02.t
            PStd_Thumb_02.r.set( 0,0,0 )
            pymel.core.parent( Std_Thumb_02, PStd_Thumb_02 )
            
            exec( 'self.LookAtStd_Thumb%s01 = LookAtStd_Thumb_01' % side )
        
        fingerStrList = [ 'Std_Index_SIDE_NUM', 'Std_Middle_SIDE_NUM', 'Std_Ring_SIDE_NUM', 'Std_Pinky_SIDE_NUM' ]
        
        for side in [ '_L_', '_R_' ]:
            
            baseStd = self.Std_Arm_L_02
            direction = [1,0,0]
            if side == '_R_':
                baseStd = self.Std_Arm_R_02
                direction = [-1,0,0]
            
            for fingerStr in fingerStrList:
                targetStr = fingerStr.replace( '_SIDE_', side )
                exec( 'target00 = self.%s' % (targetStr.replace( 'NUM', '00' ) ) )
                exec( 'target01 = self.%s' % (targetStr.replace( 'NUM', '01' ) ) )
                exec( 'target02 = self.%s' % (targetStr.replace( 'NUM', '02' ) ) )
                exec( 'target03 = self.%s' % (targetStr.replace( 'NUM', '03' ) ) )
                exec( 'target04 = self.%s' % (targetStr.replace( 'NUM', '04' ) ) )
                #print target00, target01, target02, target03, target04
                
                pymel.core.parent( target00, target01, target04, baseStd )
                LookAtStd = pymel.core.ls( makeLookAtChild( target04, target01, direction=direction ) )[0]
                LookAtStd.rename( 'LookAt' + target01.name() )
                
                pTarget02 = pymel.core.createNode( 'transform', n='P' + target02.name() )
                pymel.core.parent( pTarget02, LookAtStd )
                pTarget03 = pymel.core.createNode( 'transform', n='P' + target03.name() )
                pymel.core.parent( pTarget03, LookAtStd )
                
                dcmp = pymel.core.ls( getLocalDecomposeMatrix( target04, LookAtStd ).name() )[0]
                
                multiplyNode = pymel.core.createNode( 'multiplyDivide' )
                dcmp.ot >> multiplyNode.input1
                multiplyNode.input2.set( .3333, .3333, .3333 )
                multiplyNode.output >> pTarget02.t
                pTarget02.r.set( 0,0,0 )
                pymel.core.parent( target02, pTarget02 )
                
                multiplyNode = pymel.core.createNode( 'multiplyDivide' )
                dcmp.ot >> multiplyNode.input1
                multiplyNode.input2.set( .666, .666, .666 )
                multiplyNode.output >> pTarget03.t
                pTarget03.r.set( 0,0,0 )
                pymel.core.parent( target03, pTarget03 )
        
        self.Std_World = pymel.core.group( self.Std_Root, self.Std_Chest, self.Std_Neck, self.Std_Head, self.Std_HeadEnd, 
                          self.Std_clavicle_L_, self.Std_Arm_L_00, self.Std_Arm_L_02, self.Std_Leg_L_00, self.Std_Leg_L_02, 
                          self.Std_clavicle_R_, self.Std_Arm_R_00, self.Std_Arm_R_02, self.Std_Leg_R_00, self.Std_Leg_R_02 )
        
        self.Std_World.rename( 'Std_World' )
    
    

    def rigStdJnts(self):
        
        #root_rig
        self.StdJnt_Base = pymel.core.createNode( 'transform', n='StdJnt_Base' )
        self.StdJnt_Root = pymel.core.createNode( 'joint', n='StdJnt_Root' )
        pymel.core.parent( self.StdJnt_Root, self.StdJnt_Base )
        constrain_parent( self.Std_Root, self.StdJnt_Root )


        #body_rig
        pymel.core.select( self.StdJnt_Root )
        self.StdJnt_Back01 = pymel.core.joint( n='StdJnt_Back01' )
        self.StdJnt_Back02 = pymel.core.joint( n='StdJnt_Back02' )
        self.StdJnt_Chest  = pymel.core.joint( n='StdJnt_Chest' )
        self.StdJnt_Neck   = pymel.core.joint( n='StdJnt_Neck' )
        self.StdJnt_Head   = pymel.core.joint( n='StdJnt_Head' )
        self.StdJnt_HeadEnd = pymel.core.joint( n='StdJnt_HeadEnd' )
        constrain_point( self.Std_Back01, self.StdJnt_Back01 )
        constrain_point( self.Std_Back02, self.StdJnt_Back02 )
        constrain_parent( self.Std_Chest, self.StdJnt_Chest )
        constrain_point( self.Std_Neck, self.StdJnt_Neck )
        constrain_parent( self.Std_Head, self.StdJnt_Head )
        constrain_point( self.Std_HeadEnd, self.StdJnt_HeadEnd )
        lookAtConnect( self.Std_Back02, self.StdJnt_Back01 )
        lookAtConnect( self.Std_Chest, self.StdJnt_Back02 )
        lookAtConnect( self.Std_Head, self.StdJnt_Neck )
        
        
        #arm_L_rig
        pymel.core.select( self.StdJnt_Chest )
        self.StdJnt_clavicle_L_ = pymel.core.joint( n='StdJnt_clavicle_L_')
        self.StdJnt_Arm_L_00 = pymel.core.joint( n='StdJnt_Arm_L_00')
        self.StdJnt_Arm_L_01 = pymel.core.joint( n='StdJnt_Arm_L_01')
        self.StdJnt_Arm_L_02 = pymel.core.joint( n='StdJnt_Arm_L_02')
        pymel.core.select( self.StdJnt_Arm_L_00 )
        self.StdJnt_Arm_L_PoleV = pymel.core.joint( n='StdJnt_Arm_L_PoleV')
        pymel.core.select( self.StdJnt_Arm_L_01 )
        self.StdJnt_Arm_L_01_offset = pymel.core.joint( n='StdJnt_Arm_L_01_Offset')
        lookAtConnect( self.Std_Arm_L_00, self.StdJnt_clavicle_L_, cr=1 )
        
        constrain_point( self.Std_clavicle_L_, self.StdJnt_clavicle_L_ )
        constrain_point( self.Std_Arm_L_00, self.StdJnt_Arm_L_00 )
        constrain_point( self.Std_Arm_L_01_Moved, self.StdJnt_Arm_L_01 )
        constrain_parent( self.Std_Arm_L_02, self.StdJnt_Arm_L_02 )
        constrain_point( self.Std_Arm_L_PoleV, self.StdJnt_Arm_L_PoleV )
        constrain_point( self.Std_Arm_L_01, self.StdJnt_Arm_L_01_offset )
        
        pymel.core.select( self.StdJnt_Arm_L_00 )
        self.LookAtStdJnt_Arm_L_00 = pymel.core.joint( n='LookAtStdJnt_Arm_L_00' )
        pymel.core.aimConstraint( self.Std_Arm_L_02, self.LookAtStdJnt_Arm_L_00, aim=[1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Arm_L_PoleV )
        pymel.core.aimConstraint( self.Std_Arm_L_01_Moved, self.StdJnt_Arm_L_00, aim=[1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Arm_L_PoleV )
        pymel.core.aimConstraint( self.Std_Arm_L_02, self.StdJnt_Arm_L_01, aim=[1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Arm_L_PoleV )
        
        
        #arm_R_rig
        pymel.core.select( self.StdJnt_Chest )
        self.StdJnt_clavicle_R_ = pymel.core.joint( n='StdJnt_clavicle_R_')
        self.StdJnt_Arm_R_00 = pymel.core.joint( n='StdJnt_Arm_R_00')
        self.StdJnt_Arm_R_01 = pymel.core.joint( n='StdJnt_Arm_R_01')
        self.StdJnt_Arm_R_02 = pymel.core.joint( n='StdJnt_Arm_R_02')
        pymel.core.select( self.StdJnt_Arm_R_00 )
        self.StdJnt_Arm_R_PoleV = pymel.core.joint( n='StdJnt_Arm_R_PoleV')
        pymel.core.select( self.StdJnt_Arm_R_01 )
        self.StdJnt_Arm_R_01_offset = pymel.core.joint( n='StdJnt_Arm_R_01_Offset')
        lookAtConnect( self.Std_Arm_R_00, self.StdJnt_clavicle_R_, cr=1 )
        
        constrain_point( self.Std_clavicle_R_, self.StdJnt_clavicle_R_ )
        constrain_point( self.Std_Arm_R_00, self.StdJnt_Arm_R_00 )
        constrain_point( self.Std_Arm_R_01_Moved, self.StdJnt_Arm_R_01 )
        constrain_parent( self.Std_Arm_R_02, self.StdJnt_Arm_R_02 )
        constrain_point( self.Std_Arm_R_PoleV, self.StdJnt_Arm_R_PoleV )
        constrain_point( self.Std_Arm_R_01, self.StdJnt_Arm_R_01_offset )
        
        pymel.core.select( self.StdJnt_Arm_R_00 )
        self.LookAtStdJnt_Arm_R_00 = pymel.core.joint( n='LookAtStdJnt_Arm_R_00' )
        pymel.core.aimConstraint( self.Std_Arm_R_02, self.LookAtStdJnt_Arm_R_00, aim=[-1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Arm_R_PoleV )
        pymel.core.aimConstraint( self.Std_Arm_R_01_Moved, self.StdJnt_Arm_R_00, aim=[-1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Arm_R_PoleV )
        pymel.core.aimConstraint( self.Std_Arm_R_02, self.StdJnt_Arm_R_01, aim=[-1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Arm_R_PoleV )
        
        #leg_L_rig
        pymel.core.select( self.StdJnt_Root )
        self.StdJnt_Leg_L_00 = pymel.core.joint( n='StdJnt_Leg_L_00' )
        self.StdJnt_Leg_L_01 = pymel.core.joint( n='StdJnt_Leg_L_01' )
        self.StdJnt_Leg_L_02 = pymel.core.joint( n='StdJnt_Leg_L_02' )
        
        constrain_point( self.Std_Leg_L_00, self.StdJnt_Leg_L_00 )
        pymel.core.aimConstraint( self.Std_Leg_L_01_Moved, self.StdJnt_Leg_L_00, aim=[1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Leg_L_PoleV )
        constrain_point( self.Std_Leg_L_01_Moved, self.StdJnt_Leg_L_01 )
        pymel.core.aimConstraint( self.Std_Leg_L_02, self.StdJnt_Leg_L_01, aim=[1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Leg_L_PoleV )
        constrain_parent( self.Std_Leg_L_02, self.StdJnt_Leg_L_02 )
        
        pymel.core.select( self.StdJnt_Leg_L_01 )
        self.StdJnt_Leg_L_01_Offset = pymel.core.joint( n='StdJnt_Leg_L_01_Offset')
        constrain_point( self.Std_Leg_L_01, self.StdJnt_Leg_L_01_Offset )
        
        pymel.core.select( self.StdJnt_Leg_L_00 )
        self.StdJnt_Leg_L_PoleV = pymel.core.joint( n='StdJnt_Leg_L_PoleV')
        constrain_point( self.Std_Leg_L_PoleV, self.StdJnt_Leg_L_PoleV )
        
        pymel.core.select( self.StdJnt_Leg_L_00 )
        self.LookAtStdJnt_Leg_L_00 = pymel.core.joint( n='LookAtStdJnt_Leg_L_00' )
        pymel.core.aimConstraint( self.Std_Leg_L_02, self.LookAtStdJnt_Leg_L_00, aim=[1,0,0], u=[0,0,1], wut='object', wuo= self.Std_Leg_L_PoleV )


        #leg_R_rig
        pymel.core.select( self.StdJnt_Root )
        self.StdJnt_Leg_R_00 = pymel.core.joint( n='StdJnt_Leg_R_00' )
        self.StdJnt_Leg_R_01 = pymel.core.joint( n='StdJnt_Leg_R_01' )
        self.StdJnt_Leg_R_02 = pymel.core.joint( n='StdJnt_Leg_R_02' )
        
        constrain_point( self.Std_Leg_R_00, self.StdJnt_Leg_R_00 )
        pymel.core.aimConstraint( self.Std_Leg_R_01_Moved, self.StdJnt_Leg_R_00, aim=[-1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Leg_R_PoleV )
        constrain_point( self.Std_Leg_R_01_Moved, self.StdJnt_Leg_R_01 )
        pymel.core.aimConstraint( self.Std_Leg_R_02, self.StdJnt_Leg_R_01, aim=[-1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Leg_R_PoleV )
        constrain_parent( self.Std_Leg_R_02, self.StdJnt_Leg_R_02 )
        
        pymel.core.select( self.StdJnt_Leg_R_01 )
        self.StdJnt_Leg_R_01_Offset = pymel.core.joint( n='StdJnt_Leg_R_01_Offset')
        constrain_point( self.Std_Leg_R_01, self.StdJnt_Leg_R_01_Offset )
        
        pymel.core.select( self.StdJnt_Leg_R_00 )
        self.StdJnt_Leg_R_PoleV = pymel.core.joint( n='StdJnt_Leg_R_PoleV')
        constrain_point( self.Std_Leg_R_PoleV, self.StdJnt_Leg_R_PoleV )
        
        pymel.core.select( self.StdJnt_Leg_R_00 )
        self.LookAtStdJnt_Leg_R_00 = pymel.core.joint( n='LookAtStdJnt_Leg_R_00' )
        pymel.core.aimConstraint( self.Std_Leg_R_02, self.LookAtStdJnt_Leg_R_00, aim=[-1,0,0], u=[0,0,-1], wut='object', wuo= self.Std_Leg_R_PoleV )
        
        
        #foot_L_rig
        pymel.core.select( self.StdJnt_Leg_L_02 )
        self.StdJnt_FootPiv_L_ = pymel.core.joint( n= 'StdJnt_FootPiv_L_' )
        self.StdJnt_FootToePiv_L_ = pymel.core.joint( n= 'StdJnt_FootToePiv_L_' )
        self.StdJnt_FootIn_L_ = pymel.core.joint( n= 'StdJnt_FootIn_L_' )
        self.StdJnt_FootOut_L_ = pymel.core.joint( n= 'StdJnt_FootOut_L_' )
        self.StdJnt_FootEnd_L_ = pymel.core.joint( n= 'StdJnt_FootEnd_L_' )
        pymel.core.select( self.StdJnt_Leg_L_02 )
        self.StdJnt_Toe_L_ = pymel.core.joint( n= 'StdJnt_Toe_L_' )
        self.StdJnt_Toe_L_End = pymel.core.joint( n= 'StdJnt_Toe_L_End' )
        constrain_point( self.Std_FootPiv_L_, self.StdJnt_FootPiv_L_ )
        constrain_point( self.Std_FootIn_L_, self.StdJnt_FootIn_L_ )
        constrain_point( self.Std_FootOut_L_, self.StdJnt_FootOut_L_ )
        constrain_point( self.Std_Toe_L_, self.StdJnt_Toe_L_ )
        constrain_point( self.Std_Toe_L_End, self.StdJnt_Toe_L_End )
        constrain_point( self.Std_Toe_L_End, self.StdJnt_FootEnd_L_ )
        connectBlendTwoMatrix( self.Std_FootIn_L_, self.Std_FootOut_L_, self.StdJnt_FootToePiv_L_, ct=1 )
        
        #foot_R_rig
        pymel.core.select( self.StdJnt_Leg_R_02 )
        self.StdJnt_FootPiv_R_ = pymel.core.joint( n= 'StdJnt_FootPiv_R_' )
        self.StdJnt_FootToePiv_R_ = pymel.core.joint( n= 'StdJnt_FootToePiv_R_' )
        self.StdJnt_FootIn_R_ = pymel.core.joint( n= 'StdJnt_FootIn_R_' )
        self.StdJnt_FootOut_R_ = pymel.core.joint( n= 'StdJnt_FootOut_R_' )
        self.StdJnt_FootEnd_R_ = pymel.core.joint( n= 'StdJnt_FootEnd_R_' )
        pymel.core.select( self.StdJnt_Leg_R_02 )
        self.StdJnt_Toe_R_ = pymel.core.joint( n= 'StdJnt_Toe_R_' )
        self.StdJnt_Toe_R_End = pymel.core.joint( n= 'StdJnt_Toe_R_End' )
        constrain_point( self.Std_FootPiv_R_, self.StdJnt_FootPiv_R_ )
        constrain_point( self.Std_FootIn_R_, self.StdJnt_FootIn_R_ )
        constrain_point( self.Std_FootOut_R_, self.StdJnt_FootOut_R_ )
        constrain_point( self.Std_Toe_R_, self.StdJnt_Toe_R_ )
        constrain_point( self.Std_Toe_R_End, self.StdJnt_Toe_R_End )
        constrain_point( self.Std_Toe_R_End, self.StdJnt_FootEnd_R_ )
        connectBlendTwoMatrix( self.Std_FootIn_R_, self.Std_FootOut_R_, self.StdJnt_FootToePiv_R_, ct=1 )
        
        #hand_rig
        finterStdStrs = ['Std_Thumb_SIDE_NUM', 'Std_Index_SIDE_NUM', 'Std_Middle_SIDE_NUM', 'Std_Ring_SIDE_NUM', 'Std_Pinky_SIDE_NUM' ]
        
        for fingerStdStr in finterStdStrs:
            for side in ['_L_', '_R_' ]:
                cuFinterStdStr = fingerStdStr.replace( '_SIDE_', side )
                baseStdJnt = self.StdJnt_Arm_L_02
                aimDirection = [1,0,0]
                if side == '_R_':
                    baseStdJnt = self.StdJnt_Arm_R_02
                    aimDirection = [-1,0,0]
                pymel.core.select( baseStdJnt )
                
                stds = []
                newJnts = []
                for i in range( 10 ):
                    numStr = '%02d' % i
                    cuFingerNumStdStr = cuFinterStdStr.replace( 'NUM', numStr )
                    if not cmds.objExists( cuFingerNumStdStr ): break
                    newJnt = cmds.joint( n= cuFingerNumStdStr.replace( 'Std_', 'StdJnt_' ) )
                    constrain_point( cuFingerNumStdStr, newJnt )
                    stds.append( cuFingerNumStdStr )
                    newJnts.append( newJnt )
                    cmds.select( newJnt )
                
                for i in range( 1, len( stds ) ):
                    cmds.aimConstraint( stds[i], newJnts[i-1], aim=aimDirection, u=[0,1,0], wu=[0,1,0], wut='objectrotation', wuo=stds[i-1] )
                
                
        
                    
                
    


    def createStdElementFromInfo(self, info ):
        
        newNode = pymel.core.createNode( 'transform' )
        newNode.dh.set( 1 )
        newNode.rename( info.name )
        newNode.t.set( info.position )
        newNode.r.set( info.rotation )
        return newNode





class Std:
    
    base     = 'StdJnt_Base'
    root     = 'StdJnt_Root'
    back01   = 'StdJnt_Back01'
    back02   = 'StdJnt_Back02'
    chest    = 'StdJnt_Chest'
    neck     = 'StdJnt_Neck'
    head     = 'StdJnt_Head'
    headEnd  = 'StdJnt_HeadEnd'
    
    clavicle_SIDE_ = 'StdJnt_clavicle_SIDE_'
    arm_SIDE_00 = 'StdJnt_Arm_SIDE_00'
    arm_SIDE_01 = 'StdJnt_Arm_SIDE_01'
    arm_SIDE_02 = 'StdJnt_Arm_SIDE_02'
    arm_SIDE_poleV = 'StdJnt_Arm_SIDE_PoleV'
    arm_SIDE_01_Offset = 'StdJnt_Arm_SIDE_01_Offset'
    arm_SIDE_lookAt = 'LookAtStdJnt_Arm_SIDE_00'
    fingers_SIDE_ = 'StdJnt_%s_SIDE_*'
    
    leg_SIDE_00   = 'StdJnt_Leg_SIDE_00'
    leg_SIDE_01   = 'StdJnt_Leg_SIDE_01'
    leg_SIDE_02   = 'StdJnt_Leg_SIDE_02'
    leg_SIDE_poleV = 'StdJnt_Leg_SIDE_PoleV'
    leg_SIDE_01_Offset = 'StdJnt_Leg_SIDE_01_Offset'
    leg_SIDE_lookAt = 'LookAtStdJnt_Leg_SIDE_00'
    foot_SIDE_Piv = 'StdJnt_FootPiv_SIDE_'
    foot_SIDE_ToePiv = 'StdJnt_FootToePiv_SIDE_'
    foot_SIDE_inside = 'StdJnt_FootIn_SIDE_'
    foot_SIDE_outside = 'StdJnt_FootOut_SIDE_'
    foot_SIDE_end = 'StdJnt_FootEnd_SIDE_'
    toe_SIDE_ = 'StdJnt_Toe_SIDE_'
    toe_SIDE_end = 'StdJnt_Toe_SIDE_End'    


    @staticmethod
    def getHeadList():
        return Std.base, Std.neck, Std.head
        

    @staticmethod
    def getBodyList():
        return Std.base, Std.root, Std.back01, Std.back02, Std.chest
    
    
    @staticmethod
    def getLeftClavicleList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdClavicle = Std.clavicle_SIDE_.replace( *replaceList )
        stdArm00    = Std.arm_SIDE_00.replace( *replaceList )
        return Std.base, stdClavicle, stdArm00
    
    
    @staticmethod
    def getRightClavicleList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdClavicle = Std.clavicle_SIDE_.replace( *replaceList )
        stdArm00    = Std.arm_SIDE_00.replace( *replaceList )
        return Std.base, stdClavicle, stdArm00
    
    
    @staticmethod
    def getLeftArmList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm00 = Std.arm_SIDE_00.replace( *replaceList )
        stdArm01 = Std.arm_SIDE_01.replace( *replaceList )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.arm_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.arm_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.arm_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    

    @staticmethod
    def getRightArmList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm00 = Std.arm_SIDE_00.replace( *replaceList )
        stdArm01 = Std.arm_SIDE_01.replace( *replaceList )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.arm_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.arm_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.arm_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    
    
    @staticmethod
    def getLeftLegList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm00 = Std.leg_SIDE_00.replace( *replaceList )
        stdArm01 = Std.leg_SIDE_01.replace( *replaceList )
        stdArm02 = Std.leg_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.leg_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.leg_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.leg_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    

    @staticmethod
    def getRightLegList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm00 = Std.leg_SIDE_00.replace( *replaceList )
        stdArm01 = Std.leg_SIDE_01.replace( *replaceList )
        stdArm02 = Std.leg_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.leg_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.leg_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.leg_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
        
    
    @staticmethod
    def getLeftIkFootList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdToe     = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        stdFootPiv = Std.foot_SIDE_Piv.replace( *replaceList )
        stdToePiv  = Std.foot_SIDE_ToePiv.replace( *replaceList )
        stdFootInside = Std.foot_SIDE_inside.replace( *replaceList )
        stdFootOutside = Std.foot_SIDE_outside.replace( *replaceList )
        stdFootEnd  = Std.foot_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd


    @staticmethod
    def getRightIkFootList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdToe     = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        stdFootPiv = Std.foot_SIDE_Piv.replace( *replaceList )
        stdToePiv  = Std.foot_SIDE_ToePiv.replace( *replaceList )
        stdFootInside = Std.foot_SIDE_inside.replace( *replaceList )
        stdFootOutside = Std.foot_SIDE_outside.replace( *replaceList )
        stdFootEnd  = Std.foot_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd
    
    
    @staticmethod
    def getLeftFkFootList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdToe  = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd
    
    
    @staticmethod
    def getRightFkFootList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdToe  = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd
    
    
    @staticmethod
    def getLeftHandList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        fingerString = Std.fingers_SIDE_.replace( *replaceList )
        return Std.base, stdArm02, fingerString


    @staticmethod
    def getRightHandList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        fingerString = Std.fingers_SIDE_.replace( *replaceList )
        return Std.base, stdArm02, fingerString




class HeadRig:
    
    def __init__(self, stdBase, stdNeck, stdHead ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdNeck = convertSg( stdNeck )
        self.stdHead = convertSg( stdHead )
        self.controllerSize = 1
    
    
    def createAll(self, controllerSize = 1 ):
        
        self.controllerSize = controllerSize
        self.createRigBase()
        self.createController()
        self.createJoints()
    
    
    def createAll_type2(self, controllerSize=1 ):
        
        self.controllerSize = controllerSize
        self.createRigBase()
        self.createController()
        self.createJoints_type2()
    

    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= 'RigBase_Head' )
        self.rigBase.xform( ws=1, matrix=self.stdNeck.wm.get() )
        dcmp = getDecomposeMatrix( getLocalMatrix( self.stdNeck, self.stdBase ) )
        dcmp.ot >> self.rigBase.t
        dcmp.outputRotate >> self.rigBase.r



    def createController(self):
        
        self.ctlNeck = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Neck', makeParent=1, colorIndex=23 )
        self.ctlNeck.setAttr( 'shape_ty', 0.289  )
        pCtlNeck = self.ctlNeck.parent()
        pCtlNeck.xform( ws=1, matrix= self.stdNeck.wm.get() )
        
        self.ctlHead = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Head', makeParent=1, colorIndex=5 )
        self.ctlHead.setAttr( 'shape_ty', 0.95  ).setAttr( 'shape_rx', 90 ).setAttr( 'shape_sx', 1.3 ).setAttr( 'shape_sy', 1.3 ).setAttr( 'shape_sz', 1.3 )
        pCtlHead = self.ctlHead.parent()
        pCtlHead.xform( ws=1, matrix= self.stdHead.wm.get() )
        pCtlHead.parentTo( self.ctlNeck )
        
        self.stdHead.t >> pCtlHead.t
        
        pCtlNeck.parentTo( self.rigBase )
        headCtlOrientObj = pCtlNeck.makeChild()
        
        self.stdHead.t >> headCtlOrientObj.t
        self.stdHead.r >> headCtlOrientObj.r
        
        constrain_rotate( headCtlOrientObj, pCtlHead )
        
    
    
    def createJoints(self):
        
        lookAtPointer01base = createNode( 'transform', n='lookAtPointerBase_neckMiddle01' )
        lookAtPointer01base.parentTo( self.ctlHead )
        lookAtPointer01base.setTransformDefault()
        
        lookAtPointer01 = lookAtPointer01base.makeChild( replaceName = ['lookAtPointerBase','lookAtPointer'] )
        multPointer01 = createNode( 'multiplyDivide' ).setAttr( 'input2', -0.25,-0.25,-0.25 )
        self.stdHead.t >> multPointer01.input1
        multPointer01.output >> lookAtPointer01.t
        
        self.stdNeck.r >> lookAtPointer01base.r
        
        lookAtHeadToNeck = createNode( 'transform', n='lookAtHeadToNeck' )
        lookAtHeadToNeck.parentTo( self.ctlHead )
        lookAtHeadToNeck.setTransformDefault()
        
        lookAtConnect( self.ctlNeck, lookAtHeadToNeck )
        
        lookAtPointer02base = createNode( 'transform', n='lookAtPointerBase_neckMiddle02' )
        lookAtPointer02base.parentTo( self.ctlNeck )
        lookAtPointer02base.setTransformDefault()
        
        lookAtConnect( self.ctlHead, lookAtPointer02base )
        
        lookAtPointer02 = lookAtPointer02base.makeChild( replaceName = ['lookAtPointerBase','lookAtPointer'] )
        multPointer02 = createNode( 'multiplyDivide' ).setAttr( 'input2', .75,.75,.75 )
        self.stdHead.t >> multPointer02.input1
        multPointer02.output >> lookAtPointer02.t

        lookAtPointer = createNode( 'transform', n='lookAtPointerBase_neckMiddle' )
        lookAtPointer.parentTo( self.ctlNeck.parent() )
        blendTwoMatrix( lookAtPointer01, lookAtPointer02, lookAtPointer, ct=1, cr=1 )
        
        select( d=1 )
        self.jntNeck = joint()
        self.jntNeckMiddle = joint()
        self.jntHead = joint()
        
        constrain_point( self.ctlNeck, self.jntNeck )
        lookAtConnect( lookAtPointer, self.jntNeck ) 
        
        dcmp = getDecomposeMatrix( getLocalMatrix( self.ctlHead, self.ctlNeck ) )
        distNode = getDistance( dcmp )
        multDist = createNode( 'multDoubleLinear' )
        distNode.distance >> multDist.input1
        multDist.input2.set( 0.5 )
        multDist.output >> self.jntNeckMiddle.ty
        multDist.output >> self.jntHead.ty
        
        constrain_rotate( self.ctlHead, self.jntHead )
        lookAtConnect( self.ctlHead, self.jntNeckMiddle )
        
        blendNode = getBlendTwoMatrixNode( lookAtPointer01base, lookAtPointer02base )
        dcmp = getDecomposeMatrix( getLocalMatrix( blendNode, lookAtPointer02) )
        
        dcmp.ory >> self.jntNeckMiddle.attr( 'rotateAxisY' )
        
        self.resultJnts = [ self.jntNeck, self.jntNeckMiddle, self.jntHead ]
    


    def createJoints_type2(self):
        
        select( d=1 )
        self.jntNeck = joint()
        self.jntHead = joint()
        
        constrain_point( self.ctlNeck, self.jntNeck )
        lookAtConnect( self.ctlHead, self.jntNeck ) 
        
        dcmp = getDecomposeMatrix( getLocalMatrix( self.ctlHead, self.ctlNeck ) )
        distNode = getDistance( dcmp )
        multDist = createNode( 'multDoubleLinear' )
        distNode.distance >> multDist.input1
        multDist.input2.set( 1 )
        multDist.output >> self.jntHead.ty
        
        constrain_rotate( self.ctlHead, self.jntHead )
        self.resultJnts = [ self.jntNeck, self.jntHead ]
    





class BodyRig:
    
    def __init__(self, stdBase, stdRoot, stdBackFirst, stdBackSecond, stdChest ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdRoot = convertSg( stdRoot )
        self.stdBackFirst = convertSg( stdBackFirst )
        self.stdBackSecond = convertSg( stdBackSecond )
        self.stdChest = convertSg( stdChest )
        
        self.controllerSize = 1
        
        
    
    def createAll(self, controllerSize = 1, numJoint=3 ):
        
        self.controllerSize = controllerSize
        
        self.createRigBase()
        self.createController_type1()
        self.createOrigCurve_type1()
        self.createCurve_type1()
        self.createResultJoints( numJoint )
    
    
    def createAll_type2(self, controllerSize = 1, numJoint=3 ):
        
        self.controllerSize = controllerSize
        
        self.createRigBase()
        self.createController_type2()
        self.createOrigCurve_type2()
        self.createCurve_type2()
        self.createResultJoints( numJoint )
    
        
    
    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= 'RigBase_body' )
        self.rigBase.xform( ws=1, matrix= self.stdRoot.wm.get() )


    def createController_type1(self):
        
        self.ctlRoot = makeController( sgdata.Controllers.movePoints, self.controllerSize, n= 'Ctl_Root', makeParent=1, colorIndex=HumanRig.rootColor )
        self.ctlPervis = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_PervisRotator', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlBodyRotator1 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotatorFirst', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlBodyRotator2 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotatorSecond', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlChest = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Chest', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlWaist = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Waist', makeParent=1, colorIndex=HumanRig.bodyColor )
        self.ctlHip   = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Hip', makeParent=1, colorIndex=HumanRig.bodyColor )
        
        self.ctlRoot.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlPervis.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlBodyRotator1.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlBodyRotator2.parent().xform( ws=1, matrix= self.stdBackSecond.wm.get() )
        self.ctlChest.parent().xform( ws=1, matrix= self.stdChest.wm.get() )
        self.ctlWaist.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlHip.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        
        self.ctlRoot.setAttr( 'shape_sx', 2.14 ).setAttr( 'shape_sy', 2.14 ).setAttr( 'shape_sz', 2.14 )
        self.ctlPervis.setAttr( 'shape_sx', 3.85 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.85 )
        self.ctlBodyRotator1.setAttr( 'shape_sx', 3.36 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.36 )
        self.ctlBodyRotator2.setAttr( 'shape_sx', 3.36 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.36 )
        self.ctlWaist.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlChest.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlHip.setAttr( 'shape_sx', 1.9 ).setAttr( 'shape_sy', 1.9 ).setAttr( 'shape_sz', 1.9 )
        
        pCtlHip = self.ctlHip.parent()
        pCtlWaist = self.ctlWaist.parent()
        pCtlChest = self.ctlChest.parent()
        pCtlRoot = self.ctlRoot.parent()
        pCtlPervis = self.ctlPervis.parent()
        pCtlBodyRotator1 = self.ctlBodyRotator1.parent()
        pCtlBodyRotator2 = self.ctlBodyRotator2.parent()
        
        parent( pCtlRoot, self.rigBase )
        parent( pCtlHip, self.ctlRoot )
        parent( pCtlPervis, self.ctlRoot )
        parent( pCtlBodyRotator1, self.ctlRoot )
        
        parent( pCtlBodyRotator2, self.ctlBodyRotator1 )
        parent( pCtlWaist, self.ctlBodyRotator1 )
        
        self.stdBackSecond.t >> pCtlBodyRotator2.t
        self.stdBackSecond.r >> pCtlBodyRotator2.r
        self.stdChest.t >> pCtlChest.t
        self.stdChest.r >> pCtlChest.r
        parent( pCtlChest, self.ctlBodyRotator2 )

        hipPivInWaist = createNode( 'transform', n='Pointer_hipInWaist' )
        pHipPivInWaist = createNode( 'transform', n='PPointer_hipInWaist' )
        parent( hipPivInWaist, pHipPivInWaist )
        parent( pHipPivInWaist, self.ctlWaist.parent() )
        pHipPivInWaist.setTransformDefault()
        dcmp_hipPivInWaist = getDecomposeMatrix( getLocalMatrix( self.ctlPervis, pCtlWaist ) )
        dcmp_hipPivInWaist.ot >> hipPivInWaist.t
        dcmp_hipPivInWaist.outputRotate >> hipPivInWaist.r
        self.ctlWaist.r >> pHipPivInWaist.r
        
        constrain_parent( hipPivInWaist, pCtlHip )
        
        waistPivInPervis = createNode( 'transform', n='Pointer_waistiInPervis' )
        parent( waistPivInPervis, self.ctlPervis )
        self.stdBackFirst.t >> waistPivInPervis.t

        constrain_point( waistPivInPervis, pCtlBodyRotator1 )
        
        self.stdBackFirst.r >> pCtlBodyRotator1.r
    
    
    
    def createOrigCurve_type1(self):
    
        pointerInHip = self.stdRoot.makeChild().rename( 'pointer_' + self.stdRoot.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = self.stdBackFirst.makeChild().rename( 'pointerGrp_' + self.stdBackFirst.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + self.stdBackFirst.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + self.stdBackFirst.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        connectBlendTwoMatrix( self.stdRoot, self.stdBackFirst, pointerInBack1_grp, cr=1 )
        
        pointerInBack2_grp = self.stdBackSecond.makeChild().rename( 'pointerGrp_' + self.stdBackSecond.name() )
        pointerInBack2_00 = pointerInBack2_grp.makeChild().rename( 'pointer00_' + self.stdBackSecond.name() )
        pointerInBack2_01 = pointerInBack2_grp.makeChild().rename( 'pointer01_' + self.stdBackSecond.name() )
        multForPointerInBack2_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack2_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack2_00 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdBackSecond ) )
        dcmpPointerInBack2_00.ot >> multForPointerInBack2_00.input1
        self.stdBackSecond.t >> multForPointerInBack2_01.input1
        multForPointerInBack2_00.output >> pointerInBack2_00.t
        multForPointerInBack2_01.output >> pointerInBack2_01.t
        connectBlendTwoMatrix( self.stdBackFirst, self.stdBackSecond, pointerInBack2_grp, cr=1 )
        
        pointerInChest = self.stdChest.makeChild().rename( 'pointer_' + self.stdChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.stdRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.stdRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.stdRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_00, self.stdRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdRoot ) )
        dcmpCurvePointer7 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_01, self.stdRoot ) )
        dcmpCurvePointer8 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.stdRoot ) )
        dcmpCurvePointer9 = getDecomposeMatrix( getLocalMatrix( self.stdChest, self.stdRoot ) )

        points = [[0,0,0] for i in range( 10 )]
        origCurve = curve( p=points, d=3 ).parentTo( self.ctlRoot ).setTransformDefault()
        origCurveShape = origCurve.shape()
        dcmpCurvePointer0.ot >> origCurveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> origCurveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> origCurveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> origCurveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> origCurveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> origCurveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> origCurveShape.attr( 'controlPoints[6]' )
        dcmpCurvePointer7.ot >> origCurveShape.attr( 'controlPoints[7]' )
        dcmpCurvePointer8.ot >> origCurveShape.attr( 'controlPoints[8]' )
        dcmpCurvePointer9.ot >> origCurveShape.attr( 'controlPoints[9]' )
        self.origCurve = origCurve
    
    
    
    def createCurve_type1(self):
        
        pointerGrp_inChest = createNode( 'transform' ).parentTo( self.ctlChest.parent() )
        pointerGrp_inChest.setTransformDefault()
        pointerBody1_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerBody2_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerGrp_inHip = createNode( 'transform' ).parentTo( self.ctlHip.parent() ).setTransformDefault()
        pointerBody1_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody2_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody1 = createNode( 'transform' ).parentTo( self.rigBase )
        pointerBody2 = createNode( 'transform' ).parentTo( self.rigBase )
        
        self.ctlChest.t >> pointerGrp_inChest.t
        self.ctlHip.t >> pointerGrp_inHip.t
        
        dcmpPointerBody1_inChest = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlChest.parent() ) )
        dcmpPointerBody2_inChest = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator2, self.ctlChest.parent() ) )
        dcmpPointerBody1_inHip   = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlHip.parent() ) )
        dcmpPointerBody2_inHip   = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator2, self.ctlHip.parent() ) )

        dcmpPointerBody1_inChest.ot >> pointerBody1_inChest.t
        dcmpPointerBody2_inChest.ot >> pointerBody2_inChest.t
        dcmpPointerBody1_inHip.ot >> pointerBody1_inHip.t
        dcmpPointerBody2_inHip.ot >> pointerBody2_inHip.t
        
        blendMtxPointer1 = getBlendTwoMatrixNode( pointerBody1_inChest, pointerBody1_inHip ).setAttr( 'blend', 0.6666 )
        blendMtxPointer2 = getBlendTwoMatrixNode( pointerBody2_inChest, pointerBody2_inHip ).setAttr( 'blend', 0.3333 )
        mmPointer1 = createNode( 'multMatrix' )
        mmPointer2 = createNode( 'multMatrix' )
        blendMtxPointer1.matrixOutput() >> mmPointer1.i[0]
        blendMtxPointer2.matrixOutput() >> mmPointer2.i[0]
        
        pointerBody1.pim >> mmPointer1.i[1]
        pointerBody2.pim >> mmPointer2.i[1]
        
        dcmpPointer1 = getDecomposeMatrix( mmPointer1 )
        dcmpPointer2 = getDecomposeMatrix( mmPointer2 )
        
        dcmpPointer1.ot >> pointerBody1.t
        dcmpPointer2.ot >> pointerBody2.t
        
        pointerInHip = self.ctlHip.makeChild().rename( 'pointer_' + self.ctlHip.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = pointerBody1.makeChild().rename( 'pointerGrp_' + pointerBody1.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + pointerBody1.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + pointerBody1.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        constrain_point( self.ctlWaist, pointerInBack1_grp )
        connectBlendTwoMatrix( self.ctlWaist, self.ctlBodyRotator1.parent(), pointerInBack1_grp, cr=1 )
        
        pointerInBack2_grp = pointerBody2.makeChild().rename( 'pointerGrp_' + pointerBody2.name() )
        pointerInBack2_00 = pointerInBack2_grp.makeChild().rename( 'pointer00_' + pointerBody2.name() )
        pointerInBack2_01 = pointerInBack2_grp.makeChild().rename( 'pointer01_' + pointerBody2.name() )
        multForPointerInBack2_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack2_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack2_00 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdBackSecond ) )
        dcmpPointerInBack2_00.ot >> multForPointerInBack2_00.input1
        self.stdBackSecond.t >> multForPointerInBack2_01.input1
        multForPointerInBack2_00.output >> pointerInBack2_00.t
        multForPointerInBack2_01.output >> pointerInBack2_01.t
        connectBlendTwoMatrix( self.ctlBodyRotator2, self.ctlBodyRotator2.parent(), pointerInBack2_grp, cr=1 )
        
        pointerInChest = self.ctlChest.makeChild().rename( 'pointer_' + self.ctlChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.ctlHip, self.ctlRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.ctlRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.ctlRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( pointerBody1, self.ctlRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.ctlRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_00, self.ctlRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( pointerBody2, self.ctlRoot ) )
        dcmpCurvePointer7 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_01, self.ctlRoot ) )
        dcmpCurvePointer8 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.ctlRoot ) )
        dcmpCurvePointer9 = getDecomposeMatrix( getLocalMatrix( self.ctlChest, self.ctlRoot ) )

        bodyCurve = curve( p=[[0,0,0] for i in range( 10 )], d=7 )
        curveShape = bodyCurve.shape()
        dcmpCurvePointer0.ot >> curveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> curveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> curveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> curveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> curveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> curveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> curveShape.attr( 'controlPoints[6]' )
        dcmpCurvePointer7.ot >> curveShape.attr( 'controlPoints[7]' )
        dcmpCurvePointer8.ot >> curveShape.attr( 'controlPoints[8]' )
        dcmpCurvePointer9.ot >> curveShape.attr( 'controlPoints[9]' )
        
        bodyCurve.parentTo( self.ctlRoot ).setTransformDefault()
        self.currentCurve = bodyCurve
    
    
    
    def createController_type2(self):
        
        self.ctlRoot = makeController( sgdata.Controllers.movePoints, self.controllerSize, n= 'Ctl_Root', makeParent=1, colorIndex=HumanRig.rootColor )
        self.ctlPervis = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_PervisRotator', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlBodyRotator1 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotatorFirst', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlChest = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Chest', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlWaist = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Waist', makeParent=1, colorIndex=HumanRig.bodyColor )
        self.ctlHip   = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Hip', makeParent=1, colorIndex=HumanRig.bodyColor )
        
        self.ctlRoot.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlPervis.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlBodyRotator1.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlChest.parent().xform( ws=1, matrix= self.stdChest.wm.get() )
        self.ctlWaist.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlHip.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        
        self.ctlRoot.setAttr( 'shape_sx', 2.14 ).setAttr( 'shape_sy', 2.14 ).setAttr( 'shape_sz', 2.14 )
        self.ctlPervis.setAttr( 'shape_sx', 3.85 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.85 )
        self.ctlBodyRotator1.setAttr( 'shape_sx', 3.36 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.36 )
        self.ctlWaist.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlChest.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlHip.setAttr( 'shape_sx', 1.9 ).setAttr( 'shape_sy', 1.9 ).setAttr( 'shape_sz', 1.9 )
        
        pCtlHip = self.ctlHip.parent()
        pCtlWaist = self.ctlWaist.parent()
        pCtlChest = self.ctlChest.parent()
        pCtlRoot = self.ctlRoot.parent()
        pCtlPervis = self.ctlPervis.parent()
        pCtlBodyRotator1 = self.ctlBodyRotator1.parent()
        
        parent( pCtlRoot, self.rigBase )
        parent( pCtlHip, self.ctlRoot )
        parent( pCtlPervis, self.ctlRoot )
        parent( pCtlBodyRotator1, self.ctlRoot )
        
        parent( pCtlWaist, self.ctlBodyRotator1 )
        
        hipPivInWaist = createNode( 'transform', n='Pointer_hipInWaist' )
        parent( hipPivInWaist, self.ctlWaist )
        dcmp_hipPivInWaist = getDecomposeMatrix( getLocalMatrix( self.ctlPervis, pCtlWaist ) )
        dcmp_hipPivInWaist.ot >> hipPivInWaist.t
        dcmp_hipPivInWaist.outputRotate >> hipPivInWaist.r
        
        constrain_parent( hipPivInWaist, pCtlHip )
        
        waistPivInPervis = createNode( 'transform', n='Pointer_waistiInPervis' )
        parent( waistPivInPervis, self.ctlPervis )
        
        blendNode = getBlendTwoMatrixNode( self.stdBackFirst, self.stdBackSecond )
        mm = createNode( 'multMatrix' )
        blendNode.matrixSum >> mm.i[0]
        self.stdRoot.wim >> mm.i[1]
        dcmp_pCtlBodyRotator1 = getDecomposeMatrix( mm )
        dcmp_pCtlBodyRotator1.ot >> waistPivInPervis.t
        dcmp_pCtlBodyRotator1.outputRotate >> waistPivInPervis.r
        constrain_point( waistPivInPervis, pCtlBodyRotator1 )
        dcmp_pCtlBodyRotator1.outputRotate >> pCtlBodyRotator1.r
    
        blendDcmp = createNode( 'decomposeMatrix' )
        blendNode.matrixSum >> blendDcmp.imat
        blendCompose = createNode( 'composeMatrix' )
        blendDcmp.ot >> blendCompose.it
        blendDcmp.outputRotate >> blendCompose.ir
        blendInv = createNode( 'inverseMatrix' )
        blendCompose.outputMatrix >> blendInv.inputMatrix
        multMtx = createNode( 'multMatrix' )
        self.stdChest.wm >> multMtx.i[0]
        blendInv.outputMatrix >> multMtx.i[1]
        dcmp_pChest = createNode( 'decomposeMatrix' )
        multMtx.o >> dcmp_pChest.imat
        dcmp_pChest.ot >> pCtlChest.t
        dcmp_pChest.outputRotate >> pCtlChest.r
        
        parent( pCtlChest, self.ctlBodyRotator1 )

    
    
    def createOrigCurve_type2(self):
    
        pointerInHip = self.stdRoot.makeChild().rename( 'pointer_' + self.stdRoot.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = self.stdBackFirst.makeChild().rename( 'pointerGrp_' + self.stdBackFirst.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + self.stdBackFirst.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + self.stdBackFirst.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        connectBlendTwoMatrix( self.stdRoot, self.stdBackFirst, pointerInBack1_grp, cr=1 )
        
        pointerInChest = self.stdChest.makeChild().rename( 'pointer_' + self.stdChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.stdRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.stdRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.stdRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.stdRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( self.stdChest, self.stdRoot ) )

        points = [[0,0,0] for i in range( 7 )]
        origCurve = curve( p=points, d=5 ).parentTo( self.ctlRoot ).setTransformDefault()
        origCurveShape = origCurve.shape()
        dcmpCurvePointer0.ot >> origCurveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> origCurveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> origCurveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> origCurveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> origCurveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> origCurveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> origCurveShape.attr( 'controlPoints[6]' )
        self.origCurve = origCurve
    
    
    
    def createCurve_type2(self):
        
        pointerGrp_inChest = createNode( 'transform' ).parentTo( self.ctlChest.parent() )
        pointerGrp_inChest.setTransformDefault()
        pointerBody1_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerBody2_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerGrp_inHip = createNode( 'transform' ).parentTo( self.ctlHip.parent() ).setTransformDefault()
        pointerBody1_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody2_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody1 = createNode( 'transform' ).parentTo( self.rigBase )
        pointerBody2 = createNode( 'transform' ).parentTo( self.rigBase )
        
        self.ctlChest.t >> pointerGrp_inChest.t
        self.ctlHip.t >> pointerGrp_inHip.t
        
        dcmpPointerBody1_inChest = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlChest.parent() ) )
        dcmpPointerBody1_inHip   = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlHip.parent() ) )

        dcmpPointerBody1_inChest.ot >> pointerBody1_inChest.t
        dcmpPointerBody1_inHip.ot >> pointerBody1_inHip.t
        
        blendMtxPointer1 = getBlendTwoMatrixNode( pointerBody1_inChest, pointerBody1_inHip ).setAttr( 'blend', 0.6666 )
        blendMtxPointer2 = getBlendTwoMatrixNode( pointerBody2_inChest, pointerBody2_inHip ).setAttr( 'blend', 0.3333 )
        mmPointer1 = createNode( 'multMatrix' )
        mmPointer2 = createNode( 'multMatrix' )
        blendMtxPointer1.matrixOutput() >> mmPointer1.i[0]
        blendMtxPointer2.matrixOutput() >> mmPointer2.i[0]
        
        pointerBody1.pim >> mmPointer1.i[1]
        pointerBody2.pim >> mmPointer2.i[1]
        
        dcmpPointer1 = getDecomposeMatrix( mmPointer1 )
        dcmpPointer2 = getDecomposeMatrix( mmPointer2 )
        
        dcmpPointer1.ot >> pointerBody1.t
        dcmpPointer2.ot >> pointerBody2.t
        
        pointerInHip = self.ctlHip.makeChild().rename( 'pointer_' + self.ctlHip.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = pointerBody1.makeChild().rename( 'pointerGrp_' + pointerBody1.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + pointerBody1.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + pointerBody1.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        connectBlendTwoMatrix( self.ctlBodyRotator1, self.ctlBodyRotator1.parent(), pointerInBack1_grp, cr=1 )
        
        pointerInChest = self.ctlChest.makeChild().rename( 'pointer_' + self.ctlChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.ctlHip, self.ctlRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.ctlRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.ctlRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( pointerBody1, self.ctlRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.ctlRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.ctlRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( self.ctlChest, self.ctlRoot ) )

        bodyCurve = curve( p=[[0,0,0] for i in range( 7 )], d=5 )
        curveShape = bodyCurve.shape()
        dcmpCurvePointer0.ot >> curveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> curveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> curveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> curveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> curveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> curveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> curveShape.attr( 'controlPoints[6]' )
        
        bodyCurve.parentTo( self.ctlRoot ).setTransformDefault()
        self.currentCurve = bodyCurve
    
    

    def createResultJoints(self, numJoints = 5 ):
        
        jnts = []
        select( d=1 )
        self.rootJnt = joint()
        for i in range( numJoints + 1 ):
            jnt = joint()
            jnt.ty.set( 1.0 );
            jnts.append( jnt )
        
        self.handle, self.effector = ikHandle( sj=jnts[0], ee=jnts[-1], curve= self.currentCurve, sol='ikSplineSolver',  ccv=False, pcv=False )
        self.handle.parentTo( self.rigBase )
        self.ctlChest.addAttr( ln="attach", min=0, max=1, dv=1, k=1 )
        
        currentShape = self.currentCurve.shape()
        origShape = self.origCurve.shape()
        
        currentInfos = []
        origInfos = []
        for i in range( numJoints + 1 ):
            currentParam = i / float( numJoints )
            currentInfo = createNode( 'pointOnCurveInfo' ).setAttr( 'top', 1 ).setAttr( 'parameter', currentParam )
            origInfo    = createNode( 'pointOnCurveInfo' ).setAttr( 'top', 1 ).setAttr( 'parameter', currentParam )
            currentShape.attr( 'local' ) >> currentInfo.inputCurve
            origShape.attr( 'local' ) >> origInfo.inputCurve
            currentInfos.append( currentInfo )
            origInfos.append( origInfo )
        
        for i in range( numJoints ):
            distCurrent = createNode( 'distanceBetween' )
            distOrig    = createNode( 'distanceBetween' )
            currentInfos[i].position >> distCurrent.point1
            currentInfos[i+1].position >> distCurrent.point2
            origInfos[i].position >> distOrig.point1
            origInfos[i+1].position >> distOrig.point2
            
            blendNode = createNode( 'blendTwoAttr' )
            distOrig.distance >> blendNode.input[0]
            distCurrent.distance >> blendNode.input[1]
            self.ctlChest.attach >> blendNode.attributesBlender
            blendNode.output >> jnts[i+1].ty
        
        self.handle.attr( 'dTwistControlEnable' ).set( 1 )
        self.handle.attr( 'dWorldUpType' ).set( 4 )
        self.handle.attr( 'dForwardAxis' ).set( 2 )
        self.handle.attr( 'dWorldUpAxis' ).set( 6 )
        self.handle.attr( 'dWorldUpVector' ).set( 1,0,0 )
        self.handle.attr( 'dWorldUpVectorEnd' ).set( 1,0,0 )
        self.ctlHip.wm   >> self.handle.attr( 'dWorldUpMatrix' )
        self.ctlChest.wm >> self.handle.attr( 'dWorldUpMatrixEnd' )
        
        constrain_rotate( self.ctlChest, jnts[-1] )
        constrain_parent( self.ctlHip, self.rootJnt )
        jnts.insert( 0, self.rootJnt )
        self.resultJnts = jnts
    

    @convertSg_dec
    def createClavicleConnector(self, stdClavicleL, stdClavicleR ):
        
        chestJnt = self.resultJnts[-1]
        
        connectorClavicleL = chestJnt.makeChild().rename( stdClavicleL.replace( self.stdPrefix, 'Connector_' ) )
        connectorClavicleR = chestJnt.makeChild().rename( stdClavicleR.replace( self.stdPrefix, 'Connector_' ) )
        
        stdClavicleL.t >> connectorClavicleL.t
        stdClavicleL.r >> connectorClavicleL.r
        stdClavicleR.t >> connectorClavicleR.t
        stdClavicleR.r >> connectorClavicleR.r
        
        self.connectorClavicleL = connectorClavicleL
        self.connectorClavicleR = connectorClavicleR
    

    @convertSg_dec
    def createHipConnector(self, stdHipL, stdHipR ):
        
        rootJnt = self.rootJnt
        lookAtTarget = self.ctlRoot.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'ConnectorLookTarget_' ) )
        dcmp = getDecomposeMatrix( getLocalMatrix( self.stdChest, self.stdRoot ) )
        dcmp.oty >> lookAtTarget.ty
        
        connectorOrientBaseParent = self.ctlRoot.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'PConnectorOrientBase_' ) )
        connectorOrientBase = connectorOrientBaseParent.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'ConnectorOrientBase_' ) )
        lookAtConnect( lookAtTarget, connectorOrientBase )
        constrain_rotate( self.ctlHip, connectorOrientBaseParent )
        
        connectorOrientL = connectorOrientBase.makeChild().rename( stdHipL.replace( self.stdPrefix, 'ConnectorOrient_' ) )
        connectorOrientR = connectorOrientBase.makeChild().rename( stdHipR.replace( self.stdPrefix, 'ConnectorOrient_' ) )
        
        self.ctlHipPinL = makeController( sgdata.Controllers.pinPoints, self.controllerSize, n='Ctl_HipPos_L_', makeParent=1, colorIndex = HumanRig.leftColor )
        self.ctlHipPinR = makeController( sgdata.Controllers.pinPoints, self.controllerSize, n='Ctl_HipPos_R_', makeParent=1, colorIndex = HumanRig.rightColor )
        self.ctlHipPinR.setAttr( 'shape_rz', 180 )
        pCtlHipPinL = self.ctlHipPinL.parent()
        pCtlHipPinR = self.ctlHipPinR.parent()
        pCtlHipPinL.parentTo( self.ctlHip )
        pCtlHipPinR.parentTo( self.ctlHip )
        
        connectorL = rootJnt.makeChild().rename( stdHipL.replace( self.stdPrefix, 'Connector_' ) )
        connectorR = rootJnt.makeChild().rename( stdHipR.replace( self.stdPrefix, 'Connector_' ) )
        
        stdHipL.t >> connectorOrientL.t
        stdHipR.t >> connectorOrientR.t
        stdHipL.r >> connectorOrientL.r
        stdHipR.r >> connectorOrientR.r
        
        stdHipL.t >> pCtlHipPinL.t
        stdHipR.t >> pCtlHipPinR.t
        constrain_rotate( connectorOrientL, pCtlHipPinL )
        constrain_rotate( connectorOrientR, pCtlHipPinR )
        
        constrain_parent( self.ctlHipPinL, connectorL )
        constrain_parent( self.ctlHipPinR, connectorR )
        
        self.connectorHipL = connectorL
        self.connectorHipR = connectorR
    
    
    @convertSg_dec
    def createNeckConnector(self, stdNeck ):
        
        checkJnt = self.resultJnts[-1]
        
        connectorNeck = checkJnt.makeChild().rename( stdNeck.replace( self.stdPrefix, 'Connector_' ) )
        
        stdNeck.t >> connectorNeck.t
        stdNeck.r >> connectorNeck.r
        
        self.connectorNeck = connectorNeck
    
    
        
        
        





class ClavicleRig:
    
    def __init__(self, stdBase, stdClavicle, stdShoulder ):

        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdClavicle = convertSg( stdClavicle )
        self.stdShoulder = convertSg( stdShoulder )
        self.controllerSize = 1
    
    
    def createAll(self, controllerSize = 1, colorIndex=0 ):
    
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createCtl()
        self.createJoints()
        self.createConnector()
    


    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= self.stdClavicle.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdClavicle.wm.get() )
        constrain_parent( self.stdClavicle, self.rigBase )
    


    def createCtl(self):
        
        self.ctlClavicle = makeController( sgdata.Controllers.pinPoints, self.controllerSize, typ='joint', n= self.stdClavicle.localName().replace( self.stdPrefix, 'Ctl_' ),
                                           makeParent=1, colorIndex= self.colorIndex )
        pCtlClavicle = self.ctlClavicle.parent()
        pCtlClavicle.parentTo( self.rigBase )
        self.stdShoulder.t >> pCtlClavicle.t
        
        pCtlClavicle.r.set( 0,0,0 )


    
    def createJoints(self):
        
        self.joints = []
        select( d=1 )
        jntFirst = joint()
        jntEnd = joint()
        jntEndOrientor = self.rigBase.makeChild().rename( self.stdClavicle.replace( self.stdPrefix, 'connectOrientor_' ) ) 
        self.stdShoulder.t >> jntEndOrientor.t
        self.stdShoulder.r >> jntEndOrientor.r
        constrain_rotate( jntEndOrientor, jntEnd )
        
        self.stdShoulder.t >> jntEnd.t
        constrain_point( self.rigBase, jntFirst )
        
        direction = [1,0,0]
        
        if self.stdShoulder.tx.get() < 0:
            direction = [-1,0,0]
        lookAtConnect( self.ctlClavicle, jntFirst, direction=direction )
        
        addOptionAttribute( self.ctlClavicle )
        self.ctlClavicle.addAttr( ln='attach', min=0, max=1, dv=0, k=1 )
        pCtlClavicle = self.ctlClavicle.parent()
        
        distBase = getDistance( pCtlClavicle )
        distCurrent = getDistance( getDecomposeMatrix(getLocalMatrix( self.ctlClavicle, self.rigBase )) )
        
        divNode = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
        distCurrent.distance >> divNode.input1X
        distBase.distance >> divNode.input2X
        
        blendNode = createNode( 'blendTwoAttr' ).setAttr( 'input[0]', 1 )
        divNode.outputX >> blendNode.input[1]
        
        self.ctlClavicle.attach >> blendNode.ab
        
        blendNode.output >> jntFirst.sx
        
        self.jntFirst = jntFirst
        self.jntEnd = jntEnd
        self.jntEndOrientor = jntEndOrientor
        
        self.resultJnts = [ self.jntFirst ]
        
    
    
    def createConnector(self):
        
        self.connector = createNode( 'transform' )
        self.connector.parentTo( self.rigBase )
        
        constrain_point( self.jntEnd, self.connector )
        constrain_rotate( self.jntEndOrientor, self.connector )
        







class ArmRig:
    
    def __init__(self, stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdFirst = convertSg( stdFirst )
        self.stdSecond = convertSg( stdSecond )
        self.stdEnd  = convertSg( stdEnd )
        self.stdSecondoffset = convertSg( stdSecondoffset )
        self.stdPoleV = convertSg( stdPoleV )
        self.stdLookAt = convertSg( stdLookAt )
    
    
    
    def createAll(self, controllerSize=1, colorIndex=0, numUpperJnts=3, numLowerJnts=3 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createIkController()
        self.createPoleVController()
        self.createIkJoints()
        self.connectAndParentIk()
        self.createFKController()
        self.createFkJoints()
        self.connectAndParentFk()
        self.createBlController()
        self.connectBlVisibility()
        self.createBlJoints()
        self.connectAndParentBl()
        self.createCurve()
        self.createSpJointsUpper(numUpperJnts)
        self.createSpJointsLower(numLowerJnts)
        self.createConnector()
        


    def createRigBase(self ):
        
        self.rigBase = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdFirst.wm.get() )
        constrain_parent( self.stdFirst, self.rigBase )
    

    
    def createIkController(self ):
        
        self.ctlIkEnd = makeController( sgdata.Controllers.cubePoints, self.controllerSize, typ='joint', n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Ik' ),
                                        makeParent=1, colorIndex = self.colorIndex )
        self.ctlIkEnd.setAttr( 'shape_sx', 0.1 )
        self.ctlIkEnd.setAttr( 'shape_sy', 1.5 )
        self.ctlIkEnd.setAttr( 'shape_sz', 1.5 )
        pCtlIkEnd = self.ctlIkEnd.parent()
        pCtlIkEnd.xform( ws=1, matrix= self.stdEnd.wm.get() )
    
        dcmpStdEnd = getDecomposeMatrix( self.stdEnd )
        composeMatrix = createNode( 'composeMatrix' )
        
        dcmpStdEnd.ot >> composeMatrix.it
        mmLocalEndPos = createNode( 'multMatrix' )
        composeMatrix.outputMatrix >> mmLocalEndPos.i[0]
        self.stdFirst.wim >> mmLocalEndPos.i[1]
        dcmpPCtlIkEnd = getDecomposeMatrix( mmLocalEndPos )
        
        dcmpPCtlIkEnd.ot >> pCtlIkEnd.t
        dcmpPCtlIkEnd.outputRotate >> pCtlIkEnd.r
        
        invCompose = createNode( 'inverseMatrix' )
        composeMatrix.outputMatrix >> invCompose.inputMatrix
        
        mmIkJo = createNode( 'multMatrix' )
        self.stdEnd.wm >> mmIkJo.i[0]
        invCompose.outputMatrix >> mmIkJo.i[1]
        dcmpJo = getDecomposeMatrix( mmIkJo )
        dcmpJo.outputRotate >> self.ctlIkEnd.jo
        
        addOptionAttribute( self.ctlIkEnd, 'ikOptions')
        
        
        
    def createPoleVController(self, twistReverse=True ):
        
        self.ctlIkPoleV = makeController( sgdata.Controllers.diamondPoints, self.controllerSize, n= self.stdPoleV.localName().replace( self.stdPrefix, 'Ctl_' ),
                                          makeParent=1, colorIndex=self.colorIndex )
        self.ctlIkPoleV.setAttr( 'shape_sx', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sy', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sz', 0.23 )
        pIkCtlPoleV = self.ctlIkPoleV.parent()
        pIkCtlPoleV.xform( ws=1, matrix = self.stdLookAt.wm.get() )
        self.poleVTwist = convertSg( makeParent( pIkCtlPoleV, n='Twist_' + self.stdPoleV.localName().replace( self.stdPrefix, '' ) ) )
        self.ctlIkEnd.addAttr( ln='twist', k=1, at='doubleAngle' )
        
        multNode = createNode( 'multDoubleLinear' )
        self.ctlIkEnd.twist >> multNode.input1
        multNode.output >> self.poleVTwist.rx
        
        multNode.input2.set( 1 )
        if twistReverse:
            multNode.input2.set( -1 )
        
        dcmpPoleVStd = getDecomposeMatrix( getLocalMatrix( self.stdPoleV, self.stdLookAt ))
        dcmpPoleVStd.ot >> pIkCtlPoleV.t
        dcmpPoleVStd.outputRotate >> pIkCtlPoleV.r
        
    
    
    
    def createIkJoints(self ):
        
        firstPos = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        cmds.select( d=1 )
        self.ikJntFirst  = joint( n=self.stdFirst.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.ikJntSecond = joint( n=self.stdSecond.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.ikJntEnd  = joint( n=self.stdEnd.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=thirdPos )
        
        self.stdSecond.tx >> self.ikJntSecond.tx
        self.stdEnd.tx >> self.ikJntEnd.tx
        
        secondRotMtx = listToMatrix( self.stdSecond.xform( q=1, os=1, matrix=1 ) )
        rot = OpenMaya.MTransformationMatrix( secondRotMtx ).eulerRotation().asVector()
        self.ikJntSecond.attr( 'preferredAngleY' ).set( math.degrees( rot.y ) )
        self.ikHandle = ikHandle( sj=self.ikJntFirst, ee=self.ikJntEnd, sol='ikRPsolver' )[0]
        self.ikJntFirst.v.set( 0 )
        self.ikHandle.v.set( 0 )
        constrain_rotate( self.ctlIkEnd, self.ikJntEnd )



    def connectAndParentIk(self):
        
        self.ikGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'IkGrp_' ) )
        
        lookAtChild = makeLookAtChild( self.ctlIkEnd, self.ikGroup, n='LookAt_' + self.ctlIkPoleV.localName().replace( 'Ctl_', '' ) )
        constrain_point( self.ctlIkEnd, self.ikHandle )
        parent( self.poleVTwist, lookAtChild )
        self.poleVTwist.setTransformDefault()
        
        parent( self.ikGroup, self.rigBase )
        self.ikGroup.setTransformDefault()
        
        parent( self.ctlIkEnd.parent(), self.ikGroup )
        parent( self.ikHandle, self.ikGroup )
        parent( self.ikJntFirst, self.ikGroup )
        
        poleVDcmp = getDecomposeMatrix( getLocalMatrix( self.ctlIkPoleV, self.rigBase ) )
        poleVDcmp.ot >> self.ikHandle.attr( 'poleVector' )
    
    
    
    def createFKController( self ):
        
        self.fkCtlFirst = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdFirst.localName().replace( self.stdPrefix, 'Ctl_Fk' ), 
                                          makeParent=1, colorIndex = self.colorIndex )
        self.fkCtlSecond = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdSecond.localName().replace( self.stdPrefix, 'Ctl_Fk' ),
                                          makeParent=1, colorIndex = self.colorIndex )
        self.fkCtlEnd = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Fk' ),
                                        makeParent=1, colorIndex = self.colorIndex )
        
        self.fkCtlFirst.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlSecond.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlEnd.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        
        self.fkCtlFirst.parent().xform( ws=1, matrix = self.stdFirst.wm.get() )
        self.fkCtlSecond.parent().xform( ws=1, matrix = self.stdSecond.wm.get() )
        self.fkCtlEnd.parent().xform( ws=1, matrix = self.stdEnd.wm.get() )
        parent( self.fkCtlEnd.parent(), self.fkCtlSecond )
        parent( self.fkCtlSecond.parent(), self.fkCtlFirst )
        
        self.stdSecond.tx >> self.fkCtlSecond.parent().tx
        self.stdEnd.tx >> self.fkCtlEnd.parent().tx
        self.stdSecond.r >> self.fkCtlSecond.parent().r
        self.stdEnd.r >> self.fkCtlEnd.parent().r
        
    
    
    def createFkJoints(self ):
        
        firstPos = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        cmds.select( d=1 )
        self.fkJntFirst  = joint( n=self.stdFirst.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.fkJntSecond = joint( n=self.stdSecond.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.fkJntEnd  = joint( n=self.stdEnd.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=thirdPos )
        self.fkJntFirst.v.set( 0 )
        
        
    
    def connectAndParentFk(self):
        
        self.fkGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'FkGrp_' ) )
        parent( self.fkGroup, self.rigBase )
        self.fkGroup.setTransformDefault()
        
        parent( self.fkCtlFirst.parent(), self.fkGroup )
        
        parent( self.fkJntFirst, self.fkGroup )
        constrain_parent( self.fkCtlFirst, self.fkJntFirst )
        constrain_parent( self.fkCtlSecond, self.fkJntSecond )
        constrain_parent( self.fkCtlEnd, self.fkJntEnd )
    


    def createBlController(self ):
        
        self.ctlBl = makeController( sgdata.Controllers.switchPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Bl' ),
                                     makeParent=1, colorIndex = self.colorIndex )
        pCtlBl = self.ctlBl.parent()
        pCtlBl.xform( ws=1, matrix= self.stdEnd.wm.get() )
        
        tyValue = 0.8
        if self.stdEnd.tx.get() < 0:
            tyValue *= -1
        
        self.ctlBl.setAttr( 'shape_sx', 0.3 ).setAttr( 'shape_sy', 0.3 ).setAttr( 'shape_sz', 0.3 ).setAttr( 'shape_ty', tyValue  )
        self.ctlBl.setTransformDefault()
        keyAttrs = self.ctlBl.listAttr( k=1 )
        for attr in keyAttrs:
            self.ctlBl.attr( attr ).set( e=1, lock=1, k=0 )
    
    
    def connectBlVisibility(self):
        
        addOptionAttribute( self.ctlBl )
        self.ctlBl.addAttr( ln='blend', min=0, max=1, k=1 )
        self.ctlBl.addAttr( ln='ikVis', at='long', min=0, max=1, cb=1 )
        self.ctlBl.addAttr( ln='fkVis', at='long', min=0, max=1, cb=1 )
        
        visIk  = createNode( 'condition' ).setAttr( 'op', 1 ).setAttr( 'colorIfTrueR', 1 ).setAttr( 'colorIfFalseR', 0 ).setAttr( 'secondTerm', 1 )
        visFk  = createNode( 'condition' ).setAttr( 'op', 1 ).setAttr( 'colorIfTrueR', 1 ).setAttr( 'colorIfFalseR', 0 ).setAttr( 'secondTerm', 0 )
        addVisIk = createNode( 'addDoubleLinear' )
        addVisFk = createNode( 'addDoubleLinear' )
        
        self.ctlBl.blend >> visIk.firstTerm
        self.ctlBl.blend >> visFk.firstTerm
        self.ctlBl.ikVis >> addVisIk.input1
        self.ctlBl.fkVis >> addVisFk.input1
        visIk.outColorR >> addVisIk.input2
        visFk.outColorR >> addVisFk.input2
        
        addVisIk.output >> self.ikGroup.attr( 'v' )
        addVisFk.output >> self.fkGroup.attr( 'v' )
    
    
    
    def createBlJoints(self ):
        
        firstPos  = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        self.blJntFirst  = joint( n=self.stdFirst.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.blJntSecond = joint( n=self.stdSecond.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.blJntEnd    = joint( n=self.stdEnd.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=thirdPos )
        
        offsetPos = self.stdSecondoffset.xform( q=1, ws=1, matrix=1 )
        select( self.blJntSecond )
        self.blOffset = joint( n=self.stdSecondoffset.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=offsetPos )
        
        self.blJntFirst.v.set( 0 )
    


    def connectAndParentBl(self):
        
        self.blGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'BlGrp_' ) )
        
        parent( self.blGroup, self.rigBase )
        self.blGroup.setTransformDefault()
        
        parent( self.blJntFirst, self.blGroup )
        parent( self.ctlBl.parent(), self.blGroup )
        
        constrain_parent( self.blJntEnd, self.ctlBl.parent() )
        
        blendNodeFirst = getBlendTwoMatrixNode( self.ikJntFirst, self.fkJntFirst, local=1 )
        blendNodeSecond = getBlendTwoMatrixNode( self.ikJntSecond, self.fkJntSecond, local=1 )
        blendNodeEnd = getBlendTwoMatrixNode( self.ikJntEnd, self.fkJntEnd, local=1 )
        
        blendNodeFirstDcmp = getDecomposeMatrix( blendNodeFirst )
        blendNodeSecondDcmp = getDecomposeMatrix( blendNodeSecond )
        blendNodeEndDcmp = getDecomposeMatrix( blendNodeEnd )
        
        blendNodeFirstDcmp.ot >> self.blJntFirst.t
        blendNodeFirstDcmp.outputRotate >> self.blJntFirst.r
        blendNodeSecondDcmp.ot >> self.blJntSecond.t
        blendNodeSecondDcmp.outputRotate >> self.blJntSecond.r
        blendNodeEndDcmp.ot >> self.blJntEnd.t
        blendNodeEndDcmp.outputRotate >> self.blJntEnd.r
        
        self.ctlBl.blend >> blendNodeFirst.blend
        self.ctlBl.blend >> blendNodeSecond.blend
        self.ctlBl.blend >> blendNodeEnd.blend
        self.stdSecondoffset.t >> self.blOffset.t
        


    def createCurve(self):
        
        self.curveUpper = curve( p=[[0,0,0],[0,0,0]], d=1 )
        self.curveLower = curve( p=[[0,0,0],[0,0,0]], d=1 )
        
        upperShape = self.curveUpper.shape()
        lowerShape = self.curveLower.shape()
        
        dcmpOffsetInUpper = getDecomposeMatrix( getLocalMatrix( self.blOffset, self.blJntFirst ) )
        
        dcmpOffsetInUpper.ot >> upperShape.attr( 'controlPoints[1]' )
        self.blOffset.t    >> lowerShape.attr( 'controlPoints[0]' )
        self.blJntEnd.t    >> lowerShape.attr( 'controlPoints[1]' )
        
        parent( self.curveUpper, self.blJntFirst )
        parent( self.curveLower, self.blJntSecond )
        self.curveUpper.setTransformDefault()
        self.curveLower.setTransformDefault()
        
        self.curveUpper.v.set(0)
        self.curveLower.v.set(0)
        


    
    def createSpJointsUpper(self, numJnt=3 ):
        
        select( d=1 )
        self.outJntsUpper = [ joint() ]
        for i in range( numJnt ):
            self.outJntsUpper.append( joint() )
        
        self.handleUpper, effector = ikHandle( sj=self.outJntsUpper[0], ee=self.outJntsUpper[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveUpper.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveUpper.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for upperJnt in self.outJntsUpper[1:]:
            multNode.output >> upperJnt.tx
        pass
    
        self.handleUpper.attr( 'dTwistControlEnable' ).set( 1 )
        self.handleUpper.attr( 'dWorldUpType' ).set( 4 )
        if self.blJntSecond.tx.get() < 0:
            self.handleUpper.attr( 'dForwardAxis' ).set( 1 )
            upObjectStart = convertSg( makeLookAtChild( self.blJntSecond, self.blGroup, direction=[-1,0,0] ) )
        else:
            upObjectStart = convertSg( makeLookAtChild( self.blJntSecond, self.blGroup, direction=[1,0,0] ) )
        upObjectEnd   = makeChild( upObjectStart )
        blMtx = getBlendTwoMatrixNode( self.blJntSecond, upObjectStart ).setAttr( 'blend', math.fabs( multValue ) )
        mmBl = createNode( 'multMatrix' )
        blMtx.matrixSum >> mmBl.i[0]
        upObjectEnd.pim >> mmBl.i[1]
        dcmpBl = getDecomposeMatrix( mmBl )
        dcmpBl.outputTranslate >> upObjectEnd.t
        dcmpBl.outputRotate >> upObjectEnd.r
        
        upObjectStart.wm >> self.handleUpper.attr( 'dWorldUpMatrix' )
        upObjectEnd.wm   >> self.handleUpper.attr( 'dWorldUpMatrixEnd' )
        
        for jnt in self.outJntsUpper:
            continue
        parent( self.handleUpper, self.rigBase )
        self.handleUpper.v.set( 0 )
        
        self.resultJnts = self.outJntsUpper[:-1]
        
    


    def createSpJointsLower(self, numJnt=3 ):
        
        self.outJntsUpper[-1].v.set( 0 )
        select( self.outJntsUpper[-2] )
        self.outJntsLower = [ joint() ]
        for i in range( numJnt ):
            self.outJntsLower.append( joint() )
        
        self.handleLower, effector = ikHandle( sj=self.outJntsLower[0], ee=self.outJntsLower[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveLower.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveLower.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for lowerJnt in self.outJntsLower[1:]:
            multNode.output >> lowerJnt.tx
        
        self.handleLower.attr( 'dTwistControlEnable' ).set( 1 )
        self.handleLower.attr( 'dWorldUpType' ).set( 4 )
        upObjectStart = self.blJntSecond
        if self.blJntSecond.tx.get() < 0:
            self.handleLower.attr( 'dForwardAxis' ).set( 1 )
            pUpObjectEnd  = makeLookAtChild( self.blJntSecond, self.blJntEnd, direction=[1,0,0] )
        else:
            pUpObjectEnd  = makeLookAtChild( self.blJntSecond, self.blJntEnd, direction=[-1,0,0] )
        upObjectEnd = makeChild( pUpObjectEnd )
        connectBlendTwoMatrix( pUpObjectEnd, upObjectStart, upObjectEnd, ct=1, cr=1 )
        upObjectEnd.blend.set( multValue )
        
        upObjectStart.wm >> self.handleLower.attr( 'dWorldUpMatrix' )
        upObjectEnd.wm   >> self.handleLower.attr( 'dWorldUpMatrixEnd' )
        
        for jnt in self.outJntsLower:
            continue
        
        constrain_rotate( self.blJntEnd, self.outJntsLower[-1] )
        parent( self.handleLower, self.rigBase )
        self.handleLower.v.set( 0 )
        
        self.resultJnts += self.outJntsLower[:-1]
        
    
    
    def createConnector(self):
        
        self.connector = self.outJntsLower[-1]

    
        



class LegRig( ArmRig ):
    
    def __init__( self, stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt ):
        ArmRig.__init__( self,stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt )


    def createAll(self, controllerSize=1, colorIndex = 0, numUpperJnts=3, numLowerJnts=3 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createIkController()
        self.createPoleVController()
        self.createIkJoints()
        self.connectAndParentIk()
        self.createFKController()
        self.createFkJoints()
        self.connectAndParentFk()
        self.createBlController()
        self.connectBlVisibility()
        self.createBlJoints()
        self.connectAndParentBl()
        self.createCurve()
        self.createSpJointsUpper(numUpperJnts)
        self.createSpJointsLower(numLowerJnts)
        if self.stdFirst.name().find( '_L_' ) != -1:
            self.createIkFootRig( *Std.getLeftIkFootList() )
            self.createFKFootRig( *Std.getLeftFkFootList() )
        else:
            self.createIkFootRig( *Std.getRightIkFootList() )
            self.createFKFootRig( *Std.getRightFkFootList() )
        self.createBlFootRig()
    
    
    
    @convertSg_dec
    def createIkFootRig(self, stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd ):
        
        self.footIkGrp = createNode( 'transform', n = self.stdEnd.localName().replace( self.stdPrefix, 'FootIkBase_' ) )
        constrain_parent( self.ctlIkEnd, self.footIkGrp )
        
        ctlFoot = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= stdFootPiv.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                  makeParent=1, colorIndex=self.colorIndex )
        ctlFoot.attr( 'shape_rz' ).set( 90 )
        pCtlFoot = ctlFoot.parent()
        parent( pCtlFoot, self.footIkGrp )
        
        select( ctlFoot )
        footPivJnt = joint( n= stdFootPiv.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        toePivJnt = joint( n= stdToePiv.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footInsideJnt = joint( n= stdFootInside.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footOusideJnt = joint( n= stdFootOutside.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footEndJnt = joint( n= stdFootEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        
        stdFootPiv.t >> pCtlFoot.t
        stdFootPiv.r >> pCtlFoot.r
        
        stdToePiv.t >> toePivJnt.t
        stdFootInside.t >> footInsideJnt.t
        stdFootOutside.t >> footOusideJnt.t
        stdFootEnd.t >> footEndJnt.t
        
        addOptionAttribute( ctlFoot )
        ctlFoot.addAttr( 'liftToe', k=1 )
        ctlFoot.addAttr( 'liftHill', k=1 )
        ctlFoot.addAttr( 'ballRot', k=1 )
        ctlFoot.addAttr( 'bank', k=1 )
        
        multMinusLiftToe = createNode( 'multDoubleLinear' ).setAttr( 'input2', -1 )
        ctlFoot.liftToe >> multMinusLiftToe.input1
        
        multMinusLiftToe.output >> footPivJnt.ry
        ctlFoot.liftHill >> footEndJnt.ry
        ctlFoot.ballRot >> toePivJnt.rx
        
        bankIn  = createNode( 'condition' ).setAttr( 'op', 2 ).setAttr( 'colorIfFalseR', 0 )
        bankOut = createNode( 'condition' ).setAttr( 'op', 4 ).setAttr( 'colorIfFalseR', 0 )
        
        multMinuseBank = createNode( 'multDoubleLinear' ).setAttr( 'input2', -1 )
        ctlFoot.bank >> multMinuseBank.input1
        
        multMinuseBank.output >> bankIn.firstTerm
        multMinuseBank.output >> bankOut.firstTerm
        multMinuseBank.output >> bankIn.colorIfTrueR
        multMinuseBank.output >> bankOut.colorIfTrueR
        
        bankIn.outColorR >> footInsideJnt.rz
        bankOut.outColorR >> footOusideJnt.rz

        select( footEndJnt )
        pivToeJnt = joint( n= 'Piv' + stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        toeJnt = joint( n=stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footToAnkleJnt = joint( n= toeJnt.localName() + '_end' )
        
        localDcmpToeJnt = getDecomposeMatrix( getLocalMatrix( stdToe, stdFootEnd ) )
        localDcmpToeJnt.ot >> toeJnt.t

        worldDcmpToeJnt = getDecomposeMatrix( stdToe )
        worldDcmpToePiv  = getDecomposeMatrix( self.stdEnd )
        composeWorldToe = createNode( 'composeMatrix' )
        worldDcmpToeJnt.ot >> composeWorldToe.it
        worldDcmpToePiv.outputRotate >> composeWorldToe.ir
        invWorldToe = createNode( 'inverseMatrix' )
        composeWorldToe.outputMatrix >> invWorldToe.inputMatrix
        mmLocalStdEnd = createNode( 'multMatrix' )
        self.stdEnd.wm >> mmLocalStdEnd.i[0]
        invWorldToe.outputMatrix >> mmLocalStdEnd.i[1]
        dcmpToeEnd = getDecomposeMatrix( mmLocalStdEnd )
        dcmpToeEnd.ot >> footToAnkleJnt.t
        
        
        ctlToeEnd = makeController( sgdata.Controllers.spherePoints, self.controllerSize, n= stdToeEnd.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                    makeParent=1, colorIndex=self.colorIndex )
        ctlToeEnd.setAttr( 'shape_sx', 0.2 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.2 )
        pCtlToeEnd = ctlToeEnd.parent()
        parent( pCtlToeEnd, ctlFoot )
        constrain_parent( footEndJnt, pCtlToeEnd )
        ctlToeEnd.r >> pivToeJnt.r
        
        ctlToe = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= stdToe.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                 makeParent=1, colorIndex=self.colorIndex )
        if stdFootPiv.tx.get() < 0:
            ctlToe.setAttr( 'shape_sx', 0.5 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.15 ).setAttr( 'shape_ry', 15 ).setAttr( 'shape_tx', 0.3  )
        else:
            ctlToe.setAttr( 'shape_sx', -0.5 ).setAttr( 'shape_sy', -0.2 ).setAttr( 'shape_sz', -0.15 ).setAttr( 'shape_ry', 15 ).setAttr( 'shape_tx', -0.3  )
        ctlToe.setAttr( 'shape_rz', 90 )
        pCtlToe = ctlToe.parent()
        parent( pCtlToe, ctlToeEnd )
        pCtlToe.setTransformDefault()
        localDcmpToeJnt.ot >> pCtlToe.t
        ctlToe.r >> toeJnt.r
        
        select( footToAnkleJnt )
        self.ikJntFoot = joint( n= self.stdEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        self.ikJntToe  = joint( n= stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        self.ikJntToeEnd  = joint( n= stdToeEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        
        distNode = getDistance( dcmpToeEnd )
        distMultNode = createNode( 'multDoubleLinear' )
        distNode.distance >> distMultNode.input1
        distMultNode.input2.set( 1 )
        if stdFootPiv.tx.get() < 0:
            distMultNode.input2.set( -1 )
        distMultNode.output >> self.ikJntToe.tx
        
        distNode = getDistance( localDcmpToeJnt )
        distMultNode = createNode( 'multDoubleLinear' )
        distNode.distance >> distMultNode.input1
        distMultNode.input2.set( 1 )
        if stdFootPiv.tx.get() < 0:
            distMultNode.input2.set( -1 )
        distMultNode.output >> self.ikJntToeEnd.tx
        
        direction = [1,0,0]
        if stdFootPiv.tx.get() < 0:
            direction = [-1,0,0]
        
        lookAtConnect( ctlToe, self.ikJntFoot, direction=direction )
        lookAtConnect( ctlToeEnd, self.ikJntToe, direction=direction )
        
        rCons = self.ikJntToe.r.listConnections( s=1, d=0, p=1 )
        rCons[0] // self.ikJntToe.r
        rCons[0] >> self.ikJntToe.jo
        
        self.ikJntToe.r.set( 0,0,0 )
    
        addOptionAttribute(ctlToe)
        ctlToe.addAttr( ln='toeRot', k=1 )
        ctlToe.toeRot >> self.ikJntToe.ry
        
        constrain_point( footToAnkleJnt, self.ikHandle )
        constrain_point( self.ikJntEnd, self.ikJntFoot )
        parent( self.footIkGrp, self.ikGroup )
        
        footPivJnt.v.set( 0 )



    @convertSg_dec
    def createFKFootRig(self, stdToe, stdToeEnd ):
        
        self.footFkGrp = createNode( 'transform', n = self.stdEnd.localName().replace( self.stdPrefix, 'FootFkBase_' ) )
        
        ctlFkToe = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= stdToe.localName().replace( self.stdPrefix, 'Ctl_FootFk' ),
                                   makeParent=1, colorIndex=self.colorIndex )
        ctlFkToe.setAttr( 'shape_sx', 0.63 ).setAttr( 'shape_sy', 0.31 ).setAttr( 'shape_sz', 0.28 ).setAttr( 'shape_rz', 90 )
        pCtlFkToe = ctlFkToe.parent()
        constrain_parent( self.fkCtlEnd, self.footFkGrp )
        parent( pCtlFkToe, self.footFkGrp )
        
        composeLocalToe    = createNode( 'composeMatrix' )
        composeLocalToeEnd = createNode( 'composeMatrix' )
        inverseToe = createNode( 'inverseMatrix' )
        
        dcmpLocalToeEnd = getDecomposeMatrix( getLocalMatrix( stdToeEnd, self.stdEnd ) )
        
        stdToe.t >> composeLocalToe.it
        dcmpLocalToeEnd.ot >> composeLocalToeEnd.it
        
        composeLocalToe.outputMatrix >> inverseToe.inputMatrix
        
        mmLocalToeEnd = createNode( 'multMatrix' )
        composeLocalToeEnd.outputMatrix >> mmLocalToeEnd.i[0]
        inverseToe.outputMatrix >> mmLocalToeEnd.i[1]
        dcmpLocalToeEndTrans = getDecomposeMatrix( mmLocalToeEnd )
        
        angleNode = createNode( 'angleBetween' )
        if self.stdEnd.tx.get() > 0:
            angleNode.vector1.set( 1,0,0 )
        else:
            angleNode.vector1.set( -1,0,0 )
        dcmpLocalToeEndTrans.ot >> angleNode.vector2
        
        stdToe.t >> pCtlFkToe.t
        angleNode.euler >> pCtlFkToe.r
        
        composeToe = createNode( 'composeMatrix' )
        stdToe.t        >> composeToe.it
        angleNode.euler >> composeToe.ir
        inverseComposeToe = createNode( 'inverseMatrix' )
        
        composeToe.outputMatrix >> inverseComposeToe.inputMatrix
        
        mmToeEndInToe = createNode( 'multMatrix' )
        composeLocalToeEnd.outputMatrix >> mmToeEndInToe.i[0]
        inverseComposeToe.outputMatrix >> mmToeEndInToe.i[1]
        dcmpToeEndInToe = getDecomposeMatrix( mmToeEndInToe )
        
        childToeEnd = makeChild( ctlFkToe )
        dcmpToeEndInToe.ot >> childToeEnd.t
        
        select( self.footFkGrp )
        self.fkJntFoot = joint( n= self.stdEnd.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        self.fkJntToe  = joint( n= stdToe.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        self.fkJntToeEnd  = joint( n= stdToeEnd.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        
        direction = [1,0,0]
        if self.stdEnd.tx.get() < 0:
            direction = [-1,0,0]
        lookAtConnect( ctlFkToe, self.fkJntFoot, direction=direction )
        constrain_parent( ctlFkToe, self.fkJntToe )
        childToeEnd.t >> self.fkJntToeEnd.t
        
        parent( self.footFkGrp, self.fkGroup )
        self.fkJntFoot.v.set( 0 )

        
    @convertSg_dec
    def createBlFootRig(self):
        
        self.outJntsFoot = []
        select( self.outJntsLower[-2] )
        
        outJntFoot = joint()
        outJntToe = joint()
        outJntToeEnd = joint()
        
        self.outJntsLower[-1].t >> outJntFoot.t
        connectBlendTwoMatrix( self.ikJntFoot, self.fkJntFoot, outJntFoot, cr=1 )
        connectBlendTwoMatrix( self.ikJntToe,  self.fkJntToe,  outJntToe, ct=1, cr=1, local=1 )
        connectBlendTwoMatrix( self.ikJntToeEnd, self.fkJntToeEnd, outJntToeEnd, ct=1, local=1 )
        
        self.ctlBl.blend >> outJntFoot.blend
        self.ctlBl.blend >> outJntToe.blend
        self.ctlBl.blend >> outJntToeEnd.blend
        
        self.resultJnts += [outJntFoot,outJntToe,outJntToeEnd]
        
        pass





class HandRig:
    
    def __init__(self, stdBase, stdArm02, fingerString ):
        
        self.stdPrefix       = 'StdJnt'
        self.stdHandPrefixList = ['StdJntGrip','StdJntSpread']
        
        thumbStr = 'Thumb'
        indexStr = 'Index'
        middleStr = 'Middle'
        ringStr = 'Ring'
        pinkyStr = 'Pinky'
        add1Str = 'Add1'
        add2Str = 'Add2'
        
        thumbStds = fingerString % thumbStr
        indexStds = fingerString % indexStr
        middleStds = fingerString % middleStr
        ringStds = fingerString % ringStr
        pinkyStds = fingerString % pinkyStr
        add1Stds = fingerString % add1Str
        add2Stds = fingerString % add2Str

        self.stdBase   = convertSg( stdBase )
        self.stdArm02  = convertSg( stdArm02 )
        self.thumbStds = listNodes( thumbStds, type='joint' )
        self.indexStds = listNodes( indexStds, type='joint' )
        self.middleStds = listNodes( middleStds, type='joint' )
        self.ringStds = listNodes( ringStds, type='joint' )
        self.pinkyStds = listNodes( pinkyStds, type='joint' )
        self.add1Stds = listNodes( add1Stds, type='joint' )
        self.add2Stds = listNodes( add2Stds, type='joint' )
        self.controllerSize = 1

    
    @convertName_dec
    def getSide(self, nodeName ):
        
        if nodeName.find( '_L_' ) != -1:
            return '_L_'
        else:
            return '_R_'


    
    def createAll(self, controllerSize = 1, colorIndex=0 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createControllers()
        self.createJoints()
        #self.createFingerAttributeControl( self.stdHandPrefixList )
    


    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n=self.stdArm02.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdArm02.wm.get() )
        constrain_parent( self.stdArm02, self.rigBase )



    def createControllers(self):
        
        self.stdLists = []
        self.ctlLists = []
        if self.thumbStds:
            self.stdLists.append( self.thumbStds )
            self.ctlLists.append( [] )
        if self.indexStds:
            self.stdLists.append( self.indexStds )
            self.ctlLists.append( [] )
        if self.middleStds:
            self.stdLists.append( self.middleStds )
            self.ctlLists.append( [] )
        if self.ringStds:
            self.stdLists.append( self.ringStds )
            self.ctlLists.append( [] )
        if self.pinkyStds:
            self.stdLists.append( self.pinkyStds )
            self.ctlLists.append( [] )
        
        for k in range( len( self.stdLists ) ):
            currentParentCtl = self.rigBase
            for i in range( len( self.stdLists[k] ) ):
                ctl = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n= self.stdLists[k][i].name().replace( self.stdPrefix, 'Ctl' ), makeParent=1 ,
                                      colorIndex = self.colorIndex )
                pCtl = ctl.parent()
                self.stdLists[k][i].t >> pCtl.t
                self.stdLists[k][i].r >> pCtl.r
                self.ctlLists[k].append( ctl )
                parent( pCtl, currentParentCtl )
                currentParentCtl = ctl
    


    def createJoints(self):
        
        if not self.ctlLists: return None
        
        select( d=1 )
        baseJoint = joint()
        constrain_parent( self.rigBase, baseJoint )
        
        jntLists = [ [] for i in range( len( self.ctlLists ) ) ]
        lookAtDirection = [1,0,0]
        
        if self.stdLists[0][0].tx.get() < 0:
            lookAtDirection = [-1,0,0]
        
        for i in range( len( self.ctlLists ) ):
            select( baseJoint )
            ctlParent = self.rigBase
            for j in range( len( self.ctlLists[i] ) ):
                newJoint = joint()
                dcmpMove = getDecomposeMatrix( getLocalMatrix( self.ctlLists[i][j], ctlParent) )
                dcmpOrig = getDecomposeMatrix( getLocalMatrix( self.ctlLists[i][j].parent(), ctlParent) )
                distanceMove = getDistance( dcmpMove )
                distanceOrig = getDistance( dcmpOrig )
                div = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
                distanceMove.distance >> div.input1X
                distanceOrig.distance >> div.input2X
                if j != 0:
                    div.outputX >> jntLists[i][j-1].sx
                    aimConstraint( self.ctlLists[i][j], jntLists[i][j-1], aim=lookAtDirection, u=[0,0,1], wu=[0,0,1], wut='objectrotation', wuo=self.ctlLists[i][j-1] )
                    dcmpOrig.ot >> newJoint.t
                else:
                    constrain_point( self.ctlLists[i][j], newJoint )

                jntLists[i].append( newJoint )
                select( newJoint )
                
                ctlParent = self.ctlLists[i][j]
        
        self.resultJnts = [baseJoint] + jntLists

                



def duplicateStdHand( targetStd, attrList ):

    targetStd = pymel.core.ls( targetStd )[0]
    PREFIX = 'StdJnt'
    
    for attr in attrList:
        TARGETPREFIX = PREFIX + attr    
        duStdHand = pymel.core.duplicate( targetStd, n=targetStd.shortName().replace( PREFIX, TARGETPREFIX ) )[0]    
        children = targetStd.listRelatives( c=1, ad=1, type='joint' )
        duChildren = duStdHand.listRelatives( c=1, ad=1, type='joint' )
        targetStd.t >> duStdHand.t
        targetStd.r >> duStdHand.r
        for i in range( len( duChildren ) ):
            child = children[i]
            duChild = duChildren[i]
            duChild.rename( child.shortName().replace( PREFIX, TARGETPREFIX ) )        
            child.t >> duChild.t
            child.r >> duChild.jo
            duChild.r.set( 0,0,0 )
        duStdHand.v.set( 0 )
    
    
    
def addMiddleJoint( joint ):
    
    jointP = cmds.listRelatives( joint, p=1, f=1 )[0]
    cmds.select( jointP )
    middleJnt = cmds.joint()
    cmds.connectAttr( joint + '.t', middleJnt + '.t' )
    
    addMtx = cmds.createNode( 'addMatrix' )
    cmds.setAttr( addMtx + '.matrixIn[0]', matrixToList( OpenMaya.MMatrix() ), type='matrix' )
    cmds.connectAttr( joint + '.m', addMtx + '.matrixIn[1]' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    cmds.connectAttr( addMtx + '.matrixSum', dcmp + '.imat' )
    cmds.connectAttr( dcmp + '.or', middleJnt+ '.r' )
    cmds.select( middleJnt )
    return  middleJnt
    



class StdControl:
    
    def __init__(self):
        pass
    

    @convertSg_dec
    def setSymmetryElement( self, sel ):
    
        matList = sel.wm.get()
        
        matList[1]  *= -1
        matList[2]  *= -1
        matList[5]  *= -1
        matList[6]  *= -1
        matList[9] *= -1
        matList[10] *= -1
        matList[12] *= -1
        sel.xform( ws=1, matrix= matList )
    
    
    
    @convertSg_dec
    def setSymmetryElement_trans(self, sel ):
        
        matList = sel.wm.get()
        
        matList[12] *= -1
        sel.xform( ws=1, matrix= matList )
        


    
    @convertSg_dec
    def setSymmetry( self, targetStd, **options ):
        
        fromSide = '_L_'
        toSide = '_R_'
        
        if options.has_key( 'from' ):
            fromSide = options['from']
        if options.has_key( 'to' ):
            toSide = options['to']
        
        symtype = 'default'
        if options.has_key( 'symtype' ):
            symtype = options['symtype']
        
        ns = targetStd.name().split( 'Std_' )[0]
        
        stds = listNodes( ns + 'Std_*', type='transform' )
        
        for std in stds:
            if std.name().find( fromSide ) == -1: continue
            if not cmds.objExists( std.name().replace( fromSide, toSide ) ): continue
            
            stdToSide = convertSg( std.name().replace( fromSide, toSide ) )
            
            if symtype == 'trans':
                origMtx = std.wm.get()
                stdToSide.xform( ws=1, t= origMtx[12:-1] )
                self.setSymmetryElement_trans( stdToSide )
            else:
                stdToSide.xform( ws=1, matrix= std.wm.get() )
                self.setSymmetryElement( stdToSide )





def createHumanByStd( **options ):
    
    controllerSize = 1
    numBodyJnts = 3
    
    numArmUpperJnts = 3
    numArmLowerJnts = 3
    numLegUpperJnts = 3
    numLegLowerJnts = 3
    
    bodyType = 1
    headType = 1
    
    if options.has_key( 'controllerSize' ):
        controllerSize = options['controllerSize']
    if options.has_key( 'numBodyJnts' ):
        numBodyJnts = options['numBodyJnts' ]
        
    if options.has_key( 'numArmJnts' ):
        numArmUpperJnts = options['numArmJnts' ]
        numArmLowerJnts = options['numArmJnts' ]
    if options.has_key( 'numArmUpperJnts' ):
        numArmUpperJnts = options['numArmUpperJnts' ]
    if options.has_key( 'numArmLowerJnts' ):
        numArmLowerJnts = options['numArmLowerJnts' ]
    if options.has_key( 'numLegJnts' ):
        numLegUpperJnts = options['numLegJnts' ]
        numLegLowerJnts = options['numLegJnts' ]
    if options.has_key( 'numLegUpperJnts' ):
        numLegUpperJnts = options['numLegUpperJnts' ]
    if options.has_key( 'numLegLowerJnts' ):
        numLegLowerJnts = options['numLegLowerJnts' ]
        
    if options.has_key( 'bodyType' ):
        bodyType = options['bodyType']
    if options.has_key( 'headType' ):
        headType = options['headType']
    
    bodyRig = BodyRig( *Std.getBodyList() )
    if bodyType == 2:
        bodyRig.createAll_type2( controllerSize, numBodyJnts )
    else:
        bodyRig.createAll( controllerSize, numBodyJnts )
    cmds.refresh()
    
    bodyRig.createClavicleConnector( Std.clavicle_SIDE_.replace( '_SIDE_', '_L_'), Std.clavicle_SIDE_.replace( '_SIDE_', '_R_'))
    bodyRig.createHipConnector( Std.leg_SIDE_00.replace( '_SIDE_', '_L_'), Std.leg_SIDE_00.replace( '_SIDE_', '_R_') )
    bodyRig.createNeckConnector( Std.neck )
    cmds.refresh()
    
    headRig = HeadRig( *Std.getHeadList() )
    if headType == 2:
        headRig.createAll_type2( controllerSize )
    else:
        headRig.createAll( controllerSize )
    constrain_parent( bodyRig.connectorNeck, headRig.rigBase )
    cmds.refresh()
    
    leftClavicleRig = ClavicleRig( *Std.getLeftClavicleList() )
    leftClavicleRig.createAll(controllerSize, HumanRig.leftColor )
    constrain_parent( bodyRig.connectorClavicleL, leftClavicleRig.rigBase )
    cmds.refresh()
    
    leftArmRig = ArmRig( *Std.getLeftArmList() )
    leftArmRig.createAll( controllerSize, HumanRig.leftColor, numArmUpperJnts, numArmLowerJnts  )
    constrain_parent( leftClavicleRig.connector, leftArmRig.rigBase )
    cmds.refresh()
    
    leftLegRig = LegRig( *Std.getLeftLegList() )
    leftLegRig.createAll( controllerSize, HumanRig.leftColor, numLegUpperJnts, numLegLowerJnts )
    constrain_parent( bodyRig.connectorHipL, leftLegRig.rigBase )
    cmds.refresh()
    
    leftHandRig = HandRig( *Std.getLeftHandList())
    leftHandRig.createAll( controllerSize * 0.3, HumanRig.leftHandColor  )
    constrain_parent( leftArmRig.connector, leftHandRig.rigBase )
    cmds.refresh()
    
    rightClavicleRig = ClavicleRig( *Std.getRightClavicleList() )
    rightClavicleRig.createAll(controllerSize, HumanRig.rightColor )
    constrain_parent( bodyRig.connectorClavicleR, rightClavicleRig.rigBase )
    cmds.refresh()
    
    rightArmRig = ArmRig( *Std.getRightArmList() )
    rightArmRig.createAll( controllerSize, HumanRig.rightColor, numArmUpperJnts, numArmLowerJnts )
    constrain_parent( rightClavicleRig.connector, rightArmRig.rigBase )
    cmds.refresh()
    
    rightLegRig = LegRig( *Std.getRightLegList() )
    rightLegRig.createAll( controllerSize, HumanRig.rightColor, numLegUpperJnts, numLegLowerJnts )
    constrain_parent( bodyRig.connectorHipR, rightLegRig.rigBase )
    cmds.refresh()
    
    rightHandRig = HandRig( *Std.getRightHandList() )
    rightHandRig.createAll( controllerSize * 0.3, HumanRig.rightHandColor )
    constrain_parent( rightArmRig.connector, rightHandRig.rigBase )
    cmds.refresh()
    
    parent( headRig.resultJnts[0], bodyRig.resultJnts[-1] ); headRig.resultJnts[0].jo.set(0,0,0)
    parent( leftClavicleRig.resultJnts[0], bodyRig.resultJnts[-1] ); leftClavicleRig.resultJnts[0].jo.set(0,0,0)
    parent( rightClavicleRig.resultJnts[0], bodyRig.resultJnts[-1] ); rightClavicleRig.resultJnts[0].jo.set(0,0,0)
    parent( leftArmRig.resultJnts[0], leftClavicleRig.resultJnts[-1] ); leftArmRig.resultJnts[0].jo.set(0,0,0)
    parent( rightArmRig.resultJnts[0], rightClavicleRig.resultJnts[-1] ); rightArmRig.resultJnts[0].jo.set(0,0,0)
    try:parent( leftHandRig.resultJnts[0], leftArmRig.resultJnts[-1] ); leftHandRig.resultJnts[0].jo.set(0,0,0)
    except:pass
    try:parent( rightHandRig.resultJnts[0], rightArmRig.resultJnts[-1] ); rightHandRig.resultJnts[0].jo.set(0,0,0)
    except:pass
    parent( leftLegRig.resultJnts[0], bodyRig.resultJnts[0] ); leftLegRig.resultJnts[0].jo.set(0,0,0)
    parent( rightLegRig.resultJnts[0], bodyRig.resultJnts[0] ); rightLegRig.resultJnts[0].jo.set(0,0,0)
    cmds.refresh()
    
    ctlsGrp = createNode( 'transform', n='ctls' )
    ctlWorld = makeController( sgdata.Controllers.circlePoints, controllerSize * 3.5, n='Ctl_World', makeParent=1, colorIndex=6 )
    pCtlWorld = ctlWorld.parent()
    ctlMove  = makeController( sgdata.Controllers.crossArrowPoints, controllerSize * 3, n='Ctl_Move', makeParent=1, colorIndex = 29 )
    pCtlMove = ctlMove.parent()
    ctlFly  = makeController( sgdata.Controllers.flyPoints, controllerSize * 2, n='Ctl_Fly', makeParent=1, colorIndex=15 )
    ctlFly.setAttr( 'shape_sy', 1.5 ).setAttr( 'shape_tz', -1 ).setAttr( 'shape_ty', 0.2 )
    pCtlFly = ctlFly.parent()
    pCtlFly.xform( ws=1, matrix= bodyRig.ctlRoot.parent().wm.get() )
    
    parent( pCtlFly, ctlMove )
    parent( pCtlMove, ctlWorld )
    parent( pCtlWorld, ctlsGrp )
    
    rootDcmp = getDecomposeMatrix( getLocalMatrix( Std.root, Std.base ) )
    rootDcmp.outputTranslate >> pCtlFly.t
    rootDcmp.outputRotate >> pCtlFly.r
    
    parent( bodyRig.rigBase, ctlFly )
    parent( headRig.rigBase, ctlFly )
    parent( leftClavicleRig.rigBase, ctlFly )
    parent( rightClavicleRig.rigBase, ctlFly )
    parent( leftArmRig.rigBase, ctlFly )
    parent( rightArmRig.rigBase, ctlFly )
    parent( leftHandRig.rigBase, ctlFly )
    parent( rightHandRig.rigBase, ctlFly )
    parent( leftLegRig.rigBase, ctlFly )
    parent( rightLegRig.rigBase, ctlFly )
    
    jntGrp = createNode( 'transform', n='jointGrp' )
    parent( bodyRig.resultJnts[0], jntGrp )
    constrain_all( ctlFly, jntGrp )
    
    rigGrp = createNode( 'transform', n='rig' )
    parent( jntGrp, ctlsGrp, rigGrp )
    
    versionNum = int( pymel.core.about( v=1 ).split( '-' )[0] )
    if versionNum < 2016:
        AddAndFixRig.fixFor2015AndLater()
        



class FollowingIk:
    
    stdBase  = 'StdJnt_Base'
    stdRoot  = 'StdJnt_Root'
    stdShoulder_SIDE_ = 'StdJnt_Arm_SIDE_00'
    stdHip_SIDE_   = 'StdJnt_Leg_SIDE_00'
    stdWrist_SIDE_ = 'StdJnt_Arm_SIDE_02'
    stdAnkle_SIDE_ = 'StdJnt_Leg_SIDE_02'
    
    world     = 'Ctl_World'
    move     = 'Ctl_Move'
    fly      = 'Ctl_Fly'
    root     = 'Ctl_Root'
    chest    = 'Ctl_Chest'
    
    armBase_SIDE_ = 'RigBase_Arm_SIDE_00'
    legBase_SIDE_ = 'RigBase_Leg_SIDE_00'
    armIk_SIDE_ = 'Ctl_IkArm_SIDE_02'
    legIk_SIDE_ = 'Ctl_IkLeg_SIDE_02'
    
    def __init__(self, targetIk, targetBase, targetStd, targetBaseStd ):
        
        self.targetBase = pymel.core.ls( targetBase )[0]
        self.targetBaseStd = pymel.core.ls( targetBaseStd )[0]
        self.targetIk = pymel.core.ls( targetIk )[0]
        self.targetStd = pymel.core.ls( targetStd )[0]
    

    def create(self, *targets ):
        
        origPointer = pymel.core.createNode( 'transform' )
        pymel.core.parent( origPointer, self.targetBase )
        
        def getLocalDecomposeMatrix( localObj, parentObj ):
            
            localObj = pymel.core.ls( localObj )[0]
            parentObj = pymel.core.ls( parentObj )[0]
            
            mm = pymel.core.createNode( 'multMatrix' )
            dcmp = pymel.core.createNode( 'decomposeMatrix' )
            compose = pymel.core.createNode( 'composeMatrix' )
            dcmpTrans = pymel.core.createNode( 'decomposeMatrix' )
            localObj.wm >> dcmpTrans.imat
            dcmpTrans.ot >> compose.it
            compose.outputMatrix >> mm.i[0]
            parentObj.wim >> mm.i[1]
            mm.o >> dcmp.imat
            return dcmp
        
        origDcmp = getLocalDecomposeMatrix( self.targetStd, self.targetBaseStd )
        origPointer = pymel.core.createNode( 'transform' )
        origDcmp.ot >> origPointer.t
        origDcmp.outputRotate >> origPointer.r
        pymel.core.parent( origPointer, self.targetBase )

        blendMatrix = pymel.core.createNode( 'wtAddMatrix' )
        origPointer.wm >> blendMatrix.i[0].m
        
        sumWeight = pymel.core.createNode( 'plusMinusAverage' )
        rangeNode = pymel.core.createNode( 'setRange' )
        revNode   = pymel.core.createNode( 'reverse' )
        sumWeight.output1D >> rangeNode.valueX; rangeNode.maxX.set( 1 ); rangeNode.oldMaxX.set( 1 )
        rangeNode.outValueX >> revNode.inputX
        revNode.outputX >> blendMatrix.i[0].w
        
        divSumNode = pymel.core.createNode( 'condition' )
        divSumNode.secondTerm.set( 1 ); divSumNode.operation.set( 2 ); divSumNode.colorIfFalseR.set( 1 )
        sumWeight.output1D >> divSumNode.firstTerm
        sumWeight.output1D >> divSumNode.colorIfTrueR
        divSumAttr = divSumNode.outColorR

        addOptionAttribute( self.targetIk.name(), 'followOptions' )

        wIndex = 1
        for targetCtl, targetStd in targets:
            
            if not pymel.core.objExists( targetCtl ):
                print "%s is not exists" % targetCtl
                continue
            if not pymel.core.objExists( targetStd ):
                print "%s is not exists" % targetStd
                continue
            
            targetCtl = pymel.core.ls( targetCtl )[0]
            targetStd = pymel.core.ls( targetStd )[0]
            
            cuLocalDcmp = getLocalDecomposeMatrix( self.targetStd, targetStd )
            cuPointer = pymel.core.createNode( 'transform' )
            cuLocalDcmp.ot >> cuPointer.t
            cuLocalDcmp.outputRotate >> cuPointer.r
            cuPointer.rename(  'fPointer_' + self.targetIk.name() + '_in_' + targetCtl.name() )
            pymel.core.parent( cuPointer, targetCtl )
            cuPointer.wm >> blendMatrix.i[wIndex].m
            
            try:self.targetIk.addAttr( 'follow_%s' % targetCtl.name(), k=1, min=0, max=1, dv=0 )
            except:pass
            divWeight = pymel.core.createNode( 'multiplyDivide' ); divWeight.op.set( 2 )
            self.targetIk.attr( 'follow_%s' % targetCtl.name() ) >> divWeight.input1X
            divSumAttr >> divWeight.input2X
            divWeight.outputX >> blendMatrix.i[wIndex].w
            
            self.targetIk.attr( 'follow_%s' % targetCtl.name() ) >> sumWeight.input1D[ wIndex -1 ]
            
            wIndex += 1
        
        multMtx = pymel.core.createNode( 'multMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        blendMatrix.matrixSum >> multMtx.i[0]
        self.targetIk.getParent().pim >> multMtx.i[1]
        multMtx.matrixSum >> dcmp.imat
        
        dcmp.ot >> self.targetIk.getParent().t
        dcmp.outputRotate >> self.targetIk.getParent().r
    


    @staticmethod
    def getLeftArmList():
        
        replaceList = ( '_SIDE_', '_L_' )
        rigBase = FollowingIk.armBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.armIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdShoulder_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdWrist_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase 


    @staticmethod
    def getRightArmList():
        
        replaceList = ( '_SIDE_', '_R_' )
        rigBase = FollowingIk.armBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.armIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdShoulder_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdWrist_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase
    


    @staticmethod
    def getLeftLegList():
        
        replaceList = ( '_SIDE_', '_L_' )
        rigBase = FollowingIk.legBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.legIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdHip_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdAnkle_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase



    @staticmethod
    def getRightLegList():
        
        replaceList = ( '_SIDE_', '_R_' )
        rigBase = FollowingIk.legBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.legIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdHip_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdAnkle_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase
    


    @staticmethod
    def getFollowList( **options ):
        
        root = True
        fly  = True
        move = True
        world = True
        
        if options.has_key( 'root' ):
            root = options['root']
        if options.has_key( 'fly' ):
            fly = options['fly']
        if options.has_key( 'move' ):
            move = options['move']
        if options.has_key( 'world' ):
            world = options['world']
        
        returnTargets = []
        if root: returnTargets.append( [FollowingIk.root,  FollowingIk.stdRoot] )
        if fly: returnTargets.append( [FollowingIk.fly,   FollowingIk.stdRoot] )
        if move: returnTargets.append( [FollowingIk.move,   FollowingIk.stdBase] )
        if world: returnTargets.append( [FollowingIk.world,   FollowingIk.stdBase] )
        
        return returnTargets
    
    
    @staticmethod
    def createAll():
        
        try:
            armIkLeft = FollowingIk( *FollowingIk.getLeftArmList() )
            armIkLeft.create( *FollowingIk.getFollowList() )
        except:
            pass
        try:
            armIkRight = FollowingIk( *FollowingIk.getRightArmList() )
            armIkRight.create( *FollowingIk.getFollowList() )
        except:
            pass
        
        try:
            legIkLeft = FollowingIk( *FollowingIk.getLeftLegList() )
            legIkLeft.create( *FollowingIk.getFollowList() )
        except:pass
        try:
            legIkRight = FollowingIk( *FollowingIk.getRightLegList() )
            legIkRight.create( *FollowingIk.getFollowList() )
        except:pass



class AddAndFixRig:

    @staticmethod
    def fixFor2015AndLater():
        ikHandle1 = pymel.core.ls( 'ikHandle1' )[0]
        
        startJoint = ikHandle1.startJoint.listConnections( s=1, d=0 )[0]
        endEffector = ikHandle1.endEffector.listConnections( s=1, d=0 )[0]
        endJoint = endEffector.listConnections( s=1, d=0 )[0]
        
        allParents = endJoint.getAllParents()
        targetJoints = [endJoint]
        for parent in allParents:
            if parent == startJoint: break
            targetJoints.append( parent )
        
        for targetJoint in targetJoints:
            cons = targetJoint.ty.listConnections( s=1, d=0, p=1 )
            cons[0] // targetJoint.ty
            targetJoint.ty.set( 0 )
            cons[0] >> targetJoint.tx
        
        
        ikHandles = pymel.core.ls( 'ikHandle9', 'ikHandle10', 'ikHandle12', 'ikHandle13' )
        
        for ikHandle1 in ikHandles:
            endEffector = ikHandle1.endEffector.listConnections( s=1, d=0 )[0]
            endJoint = endEffector.listConnections( s=1, d=0 )[0]
            
            md = endJoint.tx.listConnections( s=1, d=0 )[0]
            md.input2.set( -md.input2.get() )


    @staticmethod
    def fixSplineJointConnections( inputCurveShape, *inputJnts ):
        
        curveShape = pymel.core.ls( inputCurveShape )[0]
        jnts = pymel.core.ls( inputJnts )
        beforeInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        curveShape.local >> beforeInfo.inputCurve
        beforeInfo.top.set( 1 )
        eachParam = 1.0/( len( jnts ) )
        for i in range( len( jnts ) ):
            cuInfo = pymel.core.createNode( 'pointOnCurveInfo' )
            curveShape.local >> cuInfo.inputCurve
            cuInfo.top.set( 1 )
            cuInfo.parameter.set( eachParam * i )
            distNode = pymel.core.createNode( 'distanceBetween' )
            beforeInfo.position >> distNode.point1
            cuInfo.position >> distNode.point2
            multNode = pymel.core.createNode( 'multDoubleLinear' )
            distNode.distance >> multNode.input1
            multNode.input2.set( 1 )
            if jnts[i].tx.get() < 0:
                multNode.input2.set( -1 )
            multNode.output >> jnts[i].tx
            beforeInfo = cuInfo

    @staticmethod
    def addIkScaleAndSlide( ikCtl, ikJntTop ):
        
        ikJntGrp    = convertSg( cmds.listRelatives( ikJntTop, p=1, f=1 )[0] )
        ikJntMiddle = convertSg( cmds.listRelatives( ikJntTop, c=1, f=1 )[0] )
        ikJntEnd    = convertSg( cmds.listRelatives( ikJntMiddle.name(), c=1, f=1 )[0] )
        
        upperCon = ikJntMiddle.tx.listConnections( s=1, d=0, p=1 )
        lowerCon = ikJntEnd.tx.listConnections( s=1, d=0, p=1 )
        
        if upperCon:
            upperCon = upperCon[0]
        else:
            upperCon = createNode( 'addDoubleLinear' ).setAttr( 'input1', ikJntMiddle.tx.get() ).output
        if lowerCon:
            lowerCon = lowerCon[0]
        else:
            lowerCon = createNode( 'addDoubleLinear' ).setAttr( 'input1', ikJntEnd.tx.get() ).output
    
        ikCtl = convertSg( ikCtl )
        addOptionAttribute( ikCtl, 'scaleIk' )
        ikCtl.addAttr( ln='addScale',   min=-1, max=1, k=1 )
        ikCtl.addAttr( ln='slideScale', min=-1, max=1, k=1 )
        ikCtl.addAttr( ln='stretch', min=0, max=1, k=1 )
        
        powNode = createNode( 'multiplyDivide' ).setAttr( 'op', 3 )
        addUpper = createNode( 'addDoubleLinear' )
        addLower = createNode( 'addDoubleLinear' )
        lowerReverse = createNode( 'multDoubleLinear' ).setAttr( 'input2', -1 )
        
        multUpper = createNode( 'multDoubleLinear' )
        multLower = createNode( 'multDoubleLinear' )
        
        powNode.input1X.set( 2 )
        ikCtl.addScale >> powNode.input2X
        powNode.outputX >> addUpper.input1
        powNode.outputX >> addLower.input1
        ikCtl.slideScale >> addUpper.input2
        ikCtl.slideScale >> lowerReverse.input1
        lowerReverse.output >> addLower.input2
        addUpper.output >> multUpper.input2
        addLower.output >> multLower.input2
        
        upperCon >> multUpper.input1
        lowerCon >> multLower.input1
        
        multUpper.output >> ikJntMiddle.tx
        multLower.output >> ikJntEnd.tx
    
        distTarget = ikCtl.name().replace( 'Ctl_IkLeg', 'FootIkJnt_Toe' ).replace( '02', '_end' )
        if cmds.objExists( distTarget ):
            distIk = getDistance( getLocalDecomposeMatrix( distTarget, ikJntGrp ) )
        else:
            distIk = getDistance( getLocalDecomposeMatrix( ikCtl, ikJntGrp ) )
        
        cuUpperAndLowerAdd = createNode( 'addDoubleLinear' )
        cuUpperAndLowerDist = createNode( 'distanceBetween' )
        multUpper.output >> cuUpperAndLowerAdd.input1
        multLower.output >> cuUpperAndLowerAdd.input2
        cuUpperAndLowerAdd.output >> cuUpperAndLowerDist.point1X
        
        distCondition = createNode( 'condition' )
        distIk.distance >> distCondition.firstTerm
        cuUpperAndLowerDist.distance >> distCondition.secondTerm
        distCondition.op.set( 2 )
        
        distRate = createNode( 'multiplyDivide' )
        distRate.op.set( 2 )
        distIk.distance >> distRate.input1X
        cuUpperAndLowerDist.distance >> distRate.input2X
        
        stretchedUpper = createNode( 'multDoubleLinear' )
        stretchedLower = createNode( 'multDoubleLinear' )
        
        multUpper.output >> stretchedUpper.input1
        multLower.output >> stretchedLower.input1
        distRate.outputX >> stretchedUpper.input2
        distRate.outputX >> stretchedLower.input2
        
        blendNodeUpper = createNode( 'blendTwoAttr' )
        blendNodeLower = createNode( 'blendTwoAttr' )
        ikCtl.stretch >> blendNodeUpper.ab
        ikCtl.stretch >> blendNodeLower.ab
        
        multUpper.output >> blendNodeUpper.input[0]
        multLower.output >> blendNodeLower.input[0]
        stretchedUpper.output >> blendNodeUpper.input[1]
        stretchedLower.output >> blendNodeLower.input[1]
        
        blendNodeUpper.output >> distCondition.colorIfTrueR
        blendNodeLower.output >> distCondition.colorIfTrueG
        multUpper.output >> distCondition.colorIfFalseR
        multLower.output >> distCondition.colorIfFalseG
        
        distCondition.outColorR >> ikJntMiddle.tx
        distCondition.outColorG >> ikJntEnd.tx
    
    @staticmethod
    def addFlexibleControlToCurve( inputTargetCurve ):
        
        targetCurve= pymel.core.ls( inputTargetCurve )[0]
        targetCurveShape = targetCurve.getShape()
        curveBase = targetCurve.getParent()
        
        blBase = None
        for parent in curveBase.getAllParents():
            if parent.nodeType() == 'transform':
                blBase = parent
                break
        if not blBase: return None
        
        point2Con = targetCurveShape.controlPoints[1].listConnections( s=1, d=0, p=1 )
        
        lookAtObject = pymel.core.createNode( 'transform', n='lookAtObject' )
        pymel.core.parent( lookAtObject, curveBase )
        lookAtObject.t.set( 0,0,0 )
        angleNode = pymel.core.createNode( 'angleBetween' )
        
        ctl, circleNode = pymel.core.circle()
        ctlP = pymel.core.createNode( 'transform' )
        ctlP.setParent( blBase )
        ctl.setParent( ctlP )
        ctl.t.set( 0,0,0 ); ctl.r.set( 0,0,0 )
        constrain_parent( lookAtObject, ctlP )

        pointNode = pymel.core.createNode( 'multiplyDivide' )
        baseVector = getDirection( point2Con[0].get() )
        angleNode.vector1.set( baseVector )
        point2Con[0] >> pointNode.input1
        point2Con[0] >> angleNode.vector2
        pointNode.input2.set( 0.5, 0.5, 0.5 )
        pointNode.output >> lookAtObject.t
        angleNode.euler >> lookAtObject.r
        
        circleNode.normal.set( baseVector )
        
        curvePoint1Mult = pymel.core.createNode( 'multDoubleLinear' )
        curvePoint2Mult = pymel.core.createNode( 'multDoubleLinear' )
        curvePoint1Compose = pymel.core.createNode( 'composeMatrix' )
        curvePoint2Compose = pymel.core.createNode( 'composeMatrix' )
        point2Con[0].getChildren()[0] >> curvePoint1Mult.input1
        point2Con[0].getChildren()[0] >> curvePoint2Mult.input1
        curvePoint1Mult.input2.set( -.3 )
        curvePoint2Mult.input2.set( 0.3 )
        curvePoint1Mult.output >> curvePoint1Compose.itx
        curvePoint2Mult.output >> curvePoint2Compose.itx
        
        mmPoint1 = pymel.core.createNode( 'multMatrix' )
        dcmpPoint1 = pymel.core.createNode( 'decomposeMatrix' )
        curvePoint1Compose.outputMatrix >> mmPoint1.i[0]
        ctl.wm >> mmPoint1.i[1]
        targetCurve.getParent().wim >> mmPoint1.i[2]
        mmPoint1.o >> dcmpPoint1.imat
        mmPoint2 = pymel.core.createNode( 'multMatrix' )
        dcmpPoint2 = pymel.core.createNode( 'decomposeMatrix' )
        curvePoint2Compose.outputMatrix >> mmPoint2.i[0]
        ctl.wm >> mmPoint2.i[1]
        lookAtObject.getParent().wim >> mmPoint2.i[2]
        mmPoint2.o >> dcmpPoint2.imat
        
        pointAttrs = [ None, dcmpPoint1.ot, dcmpPoint2.ot, point2Con[0] ]
        
        newCurve = pymel.core.curve( p=[[0,0,0] for i in range(4)], d=3 )
        newCurveShape = newCurve.getShape()
        for i in range( 4 ):
            if not pointAttrs[i]: continue
            pointAttrs[i] >> newCurveShape.controlPoints[i]
        
        pymel.core.parent( newCurve, curveBase )
        newCurve.t.set( 0,0,0 )
        newCurve.r.set( 0,0,0 )
        
        for origCon, destCon in targetCurveShape.listConnections( s=0, d=1, p=1, c=1 ):
            attrName = origCon.attrName()
            newCurve.attr( attrName ) >> destCon
        
        selShape = newCurveShape
        curveInfo = selShape.listConnections( s=0, d=1, type='curveInfo' )[0]
        multNode = curveInfo.listConnections( d=1, s=0, type='multDoubleLinear' )[0]
        joints = multNode.listConnections( s=0, d=1, type='joint' )
        maxValue = selShape.maxValue.get()
        
        pointOnCurve = pymel.core.createNode( 'pointOnCurveInfo' )
        selShape.local >> pointOnCurve.inputCurve
        jntAndCurveInfos = [[0.0,None,pointOnCurve]]
        
        for jnt in joints:
            paramValue = getClosestParamAtPoint( jnt, selShape.getParent() )/maxValue
            pointOnCurve = pymel.core.createNode( 'pointOnCurveInfo' )
            selShape.local >> pointOnCurve.inputCurve
            pointOnCurve.parameter.set( paramValue )
            jntAndCurveInfos.append( [ paramValue, jnt, pointOnCurve ] )
        jntAndCurveInfos.sort()
        for i in range( 1, len( jntAndCurveInfos ) ):
            beforeCurveInfo = jntAndCurveInfos[i-1][2]
            param, jnt, curveInfo = jntAndCurveInfos[i]
            distNode= pymel.core.createNode( 'distanceBetween' )
            beforeCurveInfo.position >> distNode.point1
            curveInfo.position >> distNode.point2
            eachMultNode = pymel.core.createNode( 'multDoubleLinear' )
            eachMultNode.input2.set( 1 )
            distNode.distance >> eachMultNode.input1
            eachMultNode.output >> jnt.tx
            if multNode.input2.get() < 0:
                eachMultNode.input2.set( -1 )
            eachMultNode.output >> jnt.tx
        
        pymel.core.delete( targetCurve )
    
    
    @staticmethod
    def fixFootAttribute( inputCtlFootPiv ):
        
        inputCtlToeEnd = inputCtlFootPiv.replace( 'FootIkFootPiv', 'FootIkToe' ) + 'End'
        inputCtlToe = inputCtlFootPiv.replace( 'FootIkFootPiv', 'FootIkToe' )
        
        ctlFootPiv = pymel.core.ls( inputCtlFootPiv )[0]
        ctlToeEnd  = pymel.core.ls( inputCtlToeEnd )[0]
        ctlToe     = pymel.core.ls( inputCtlToe )[0]
        
        ctlFootPiv.addAttr( 'liftBall', k=1 )
        ctlFootPiv.addAttr( 'hillTwist', k=1 )
        ctlFootPiv.addAttr( 'ballTwist', k=1 )
        ctlFootPiv.addAttr( 'toeTwist',  k=1 )
        ctlFootPiv.addAttr( 'toeRot', k=1 )
        
        conTargets = ctlFootPiv.ballRot.listConnections( s=0, d=1, p=1 )
        
        ctlFootPiv.liftBall >> ctlToe.ry
        ctlFootPiv.hillTwist >> ctlFootPiv.rx
        for conTarget in conTargets:
            ctlFootPiv.ballTwist >> conTarget
        ctlFootPiv.toeTwist >> ctlToeEnd.rx
        ctlFootPiv.toeRot >> ctlToe.toeRot
        
        ctlToeEnd.v.set( 0 )
        
        if pymel.core.attributeQuery( 'ballRot', node=ctlFootPiv, ex=1 ):
            ctlFootPiv.ballRot.delete()
    
    
    @staticmethod
    def fixIkToeJointOrient():
        
        for side in ['_L_', '_R_']:
            
            if side == '_L_': direction = [1,0,0]
            elif side == '_R_': direction = [-1,0,0]
            
            lookBase = pymel.core.ls( 'PCtl_FootIkToe' + side )[0]
            lookTarget = pymel.core.ls( 'Ctl_FootIkToe%sEnd' % side )[0]
            targetJoint = pymel.core.ls( 'FootIkJnt_Toe' + side )[0]
            lookChild = makeLookAtChild_( lookTarget, lookBase, direction=direction )
            
            mm = pymel.core.createNode( 'multMatrix' )
            lookChild.wm >> mm.i[0]
            targetJoint.getParent().wim >> mm.i[1]
            dcmp= pymel.core.createNode( 'decomposeMatrix' )
            mm.matrixSum >> dcmp.imat
            dcmp.outputRotate >> targetJoint.jo
            
        
        
    @staticmethod
    def addAutoTwistPoleVector( ctlIk ):
        
        twistTarget = ctlIk.replace( 'Ctl_IkLeg', 'FootIkJnt_Toe' ).replace( '02', '_end' )
        twistTargetBase = cmds.createNode( 'transform' )
        cmds.connectAttr( ctlIk + '.jo', twistTargetBase + '.r' )
        cmds.connectAttr( ctlIk + '.t', twistTargetBase + '.t' )
        selP = cmds.listRelatives( ctlIk, p=1, f=1 )[0]
        twistTargetBase = cmds.parent( twistTargetBase, selP )[0]
        localMtx = cmds.createNode( 'multMatrix' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( twistTarget + '.wm', localMtx + '.i[0]' )
        cmds.connectAttr( twistTargetBase + '.wim', localMtx + '.i[1]' )
        cmds.connectAttr( localMtx + '.o', dcmp + '.imat' )
        localTwistObj = cmds.createNode( 'transform' )
        cmds.connectAttr( dcmp + '.or', localTwistObj + '.r' )
        localTwistObj = cmds.parent( localTwistObj, twistTargetBase )[0]
        cmds.setAttr( localTwistObj + '.t', 0,0,0 )
        autoTwistNode = getAutoTwistNode( localTwistObj )
        dcmpAutoTwistNode = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( autoTwistNode + '.matrixSum', dcmpAutoTwistNode + '.imat' )
        
        twistLegPoleV = ctlIk.replace( 'Ctl_IkLeg', 'Twist_Leg' ).replace( '02', 'PoleV' )
        baseTwistLegPoleV = cmds.listRelatives( twistLegPoleV, p=1, f=1 )[0]
        
        pTwist = cmds.parent( cmds.createNode( 'transform', n='Auto_' + twistLegPoleV ), baseTwistLegPoleV )[0]
        cmds.setAttr( pTwist + '.t', 0,0,0 )
        cmds.connectAttr( dcmpAutoTwistNode + '.or', pTwist + '.r' )
        
        addOptionAttribute( ctlIk, 'autoPoleVTwist' )
        cmds.addAttr( ctlIk, ln='autoTwistPoleV', min=0, max=1, dv=1 )
        cmds.setAttr( ctlIk + '.autoTwistPoleV', e=1, k=1 )
        cmds.connectAttr( ctlIk + '.autoTwistPoleV', autoTwistNode + '.blend' )
        
        cmds.parent( twistLegPoleV, pTwist )[0]
        
        
        
    @staticmethod
    def createFingerAttributeControl( fingerCtl ):
    
        side = ''
        if fingerCtl.find( '_L_' ) != -1:
            baseStdNames = 'StdJnt*_Arm_L_02'
            side = 'L'
        else:
            baseStdNames = 'StdJnt*_Arm_R_02'
            side = 'R'
    
        baseStdName = 'StdJnt_Arm_%s_02' % side
        baseStds = cmds.ls( baseStdNames )
        handAttrList = []
        for baseStd in baseStds:
            if baseStd == baseStdName: continue
            attrName = baseStd.replace( 'StdJnt', '' ).replace( '_Arm_%s_02' % side, '' )
            handAttrList.append( attrName )
    
        stdLists = []
        for fingerName in ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']:
            fingers = cmds.ls( baseStdName.replace( 'Arm', fingerName ).replace( '02', '*' ), type='joint' )
            if not fingers: continue
            stdLists.append( fingers )
        
        for i in range( len( stdLists ) ):
            for j in range( len( stdLists[i] ) ):
                plusNode   = cmds.createNode( 'plusMinusAverage' )
                for k in range( len( handAttrList ) ):
                    targetStd = stdLists[i][j].replace( 'StdJnt', 'StdJnt' + handAttrList[k] )
                    multTarget = cmds.createNode( 'multiplyDivide' )
                    addAttr( fingerCtl, ln=handAttrList[k], k=1 )   
                    cmds.connectAttr( targetStd + '.r', multTarget + '.input1' )                 
                    cmds.connectAttr( fingerCtl + '.' + handAttrList[k], multTarget + '.input2X' )
                    cmds.connectAttr( fingerCtl + '.' + handAttrList[k], multTarget + '.input2Y' )
                    cmds.connectAttr( fingerCtl + '.' + handAttrList[k], multTarget + '.input2Z' )
                    cmds.connectAttr( multTarget + '.output', plusNode + '.input3D[%d]' % k )
                
                offsetCtl = stdLists[i][j].replace( 'StdJnt', 'OffsetCtl' )
                
                divNode = cmds.createNode( 'multiplyDivide' )
                cmds.connectAttr( plusNode + '.output3D', divNode + '.input1' )
                cmds.setAttr( divNode + '.input2', 0.1, 0.1, 0.1 )
                
                cmds.connectAttr( divNode + '.output', offsetCtl + '.r', f=1 )





class RigControllerControl:
    
    origNameAttr = 'rig_origName'
    parentAttr   = 'rig_parents'
    reverseAttrs = 'rig_reverseAttrs'
    sidePrefixAttr = 'rig_sidePrefix'
    outerMatrixAttr= 'rig_outerMatrix'
    innerMatrixAttr= 'rig_innerMatrix'
    
    leftPrefixList = ['_L_', 'left', 'Left']
    rightPrefixList = ['_R_', 'right', 'Right']
    

    def __init__(self, name ):
        
        self.name = name
        self.namespace = ''
        self.origName = name
        self.origNameAttr = RigControllerControl.origNameAttr
        if not cmds.attributeQuery( self.origNameAttr, node=self.name, ex=1 ): return None
            

    
    def parents(self):
        
        parentObjs = []
        if not cmds.attributeQuery( self.parentAttr, node= self.name, ex=1 ): 
            return None
        if not cmds.getAttr( self.name + '.' + self.parentAttr ):
            return None
        origName = cmds.getAttr( self.name + '.' + self.origNameAttr )
        parentOrigNames = cmds.getAttr( self.name + '.' + self.parentAttr )
        
        ns = self.name.replace( origName, '' )
        
        for parentOrigName in parentOrigNames.split( ',' ):
            parentName = ns + parentOrigName.strip()
            parentObjs.append( RigControllerControl( parentName ) )
        if not parentObjs: 
            cmds.warning( "%s parent is real Parent" % self.name )
            return None
        return parentObjs
    


    def matrix(self):
        
        return listToMatrix( cmds.getAttr( self.name + '.wm' ) )
        

        
    def getSide(self):
        
        for leftPrefix in RigControllerControl.leftPrefixList:
            if self.name.find( leftPrefix ) != -1:
                return 'left'
        for rightPrefix in RigControllerControl.rightPrefixList:
            if self.name.find( rightPrefix ) != -1:
                return 'right'    
        return 'center'



    def getOtherSide(self):
        
        if not cmds.attributeQuery( self.sidePrefixAttr, node= self.name, ex=1 ):
            return self
        if not cmds.getAttr( self.name + '.' + self.sidePrefixAttr ):
            return self
        prefixValue = cmds.getAttr( self.name + '.' + self.sidePrefixAttr )
        if prefixValue in RigControllerControl.leftPrefixList:
            otherPrefixValue = RigControllerControl.rightPrefixList[ RigControllerControl.leftPrefixList.index(prefixValue) ]
        if prefixValue in RigControllerControl.rightPrefixList:
            otherPrefixValue = RigControllerControl.leftPrefixList[ RigControllerControl.rightPrefixList.index(prefixValue) ]
        otherName = self.name.replace( prefixValue, otherPrefixValue )
        if not cmds.objExists( otherName ):
            cmds.warning( '%s is not Exists' % otherName )
            return self
        return RigControllerControl( otherName )
    


    def getCtlData(self):
        
        parentObjs = self.parents()
        if not parentObjs:
            return None, None, None
        localMatrix = self.matrix() * parentObjs[0].matrix().inverse()
        
        udAttrs = cmds.listAttr( self.name, k=1, ud=1 )
        if not udAttrs: udAttrs = []
        udAttrValues = []
        
        for attr in udAttrs:
            udAttrValues.append(  cmds.getAttr( self.name + '.' + attr ) )
        
        keyAttrs = cmds.listAttr( self.name, k=1, sn=1 )
        for attr in ['sx', 'sy', 'sz']:
            if attr in keyAttrs:
                udAttrs.append( attr )
                udAttrValues.append( cmds.getAttr( self.name + '.'+ attr ) )
        
        return localMatrix, udAttrs, udAttrValues
    


    def getInnerMatrix(self):
        
        attrName = RigControllerControl.innerMatrixAttr
        if not cmds.attributeQuery( attrName, node= self.name, ex=1 ): return None
        innerMatrixValue = cmds.getAttr( self.name + '.' + attrName )
        if not innerMatrixValue:
            return OpenMaya.MMatrix()
        
        mtxList = []
        exec( 'mtxList = %s' % innerMatrixValue )
        return listToMatrix( mtxList )



    def getOuterMatrix(self):
        
        attrName = RigControllerControl.outerMatrixAttr
        if not cmds.attributeQuery( attrName, node= self.name, ex=1 ): return None
        outerMatrixValue = cmds.getAttr( self.name + '.' + attrName )
        if not outerMatrixValue:
            return OpenMaya.MMatrix()
        
        mtxList = []
        exec( 'mtxList = %s' % outerMatrixValue )
        return listToMatrix( mtxList )
    
    

    def setCtlData(self, localMatrix, udAttrs, udAttrValues ):
        
        parentMatrix = listToMatrix( cmds.getAttr( self.parents()[0].name + '.wm' ) )
        
        innerMtx  = self.getInnerMatrix()
        outerMtx  = self.getOuterMatrix()
        
        if not innerMtx or not outerMtx: 
            cmds.warning( "%s is not Rig Controller" % self.name )
            return None 
        
        mtxResult = innerMtx * localMatrix * outerMtx * parentMatrix
        
        if cmds.nodeType( self.name ) == 'joint':
            realParentMatrix = listToMatrix( cmds.getAttr( cmds.listRelatives( self.name, p=1, f=1 )[0] + '.wm' ) )
            joMatrix = getMatrixFromRotate( cmds.getAttr( self.name + '.jo' )[0] )
            joWorldMatrix = joMatrix * realParentMatrix
            trValue = getTranslateFromMatrix( mtxResult )
            cmds.move( trValue[0], trValue[1], trValue[2], self.name, ws=1 )
            mtxResult *= joWorldMatrix.inverse()
            rotValue = getRotateFromMatrix( mtxResult )
            cmds.rotate( rotValue[0], rotValue[1], rotValue[2], self.name, os=1 )
        else:
            mtxList = matrixToList( mtxResult )
            cmds.xform( self.name, ws=1, matrix=mtxList )
        
        for i in range( len( udAttrs ) ):
            cmds.setAttr( self.name + '.' + udAttrs[i], udAttrValues[i] )
    


    def setFlip(self):
        
        otherSide = self.getOtherSide()
        
        selfLocalMtx,  selfUdAttrs, selfUdAttrValues = self.getCtlData()
        otherLocalMtx, otherUdAttrs, otherUdValues  = otherSide.getCtlData()
        
        if not selfLocalMtx or not otherLocalMtx: 
            cmds.warning( "%s Flip is not worked" % self.name )
            return None
    
        otherSide.setCtlData( selfLocalMtx, selfUdAttrs, selfUdAttrValues )
        self.setCtlData( otherLocalMtx, otherUdAttrs, otherUdValues )
    
    
    
    def children(self):
        
        origName = cmds.getAttr( self.name + '.' + RigControllerControl.origNameAttr )
        ns = self.name.replace( origName, '' )
        
        targetNodes = []
        for attr in cmds.ls( ns + '*.' + RigControllerControl.parentAttr ):
            values = cmds.getAttr( attr )
            for value in values.split( ',' ):
                if value.strip() == origName:
                    targetNodes.append( RigControllerControl(attr.split( '.' )[0]) )
        return targetNodes


    def allChildren(self):
        
        localChildren = self.children()
        childrenH = []
        for localChild in localChildren:
            childrenH += localChild.allChildren()
        localChildren += childrenH
        childrenNames = []

        localChildrenSet = []
        for localChild in localChildren:
            name = localChild.name
            if name in childrenNames: continue
            childrenNames.append( name )
            localChildrenSet.append( localChild )
        
        return localChildrenSet
    
    
    def hierarchy(self):
        
        localChildren = [self]
        localChildren += self.allChildren()
        return localChildren
    
    
    def flipH(self):
        
        H = self.hierarchy()
    
        flipedList = []
        sourceList = []
        targetList = []
        sourceDataList = []
        targetDataList = []
        
        for h in H:
            if h.name in flipedList: continue
            name = h.getOtherSide().name
            if name in flipedList: continue
            flipedList.append( h.name )
            
            
            otherSide = h.getOtherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDataList.append( h.getCtlData() )
            targetDataList.append( otherSide.getCtlData() )
        
        for i in range( len( sourceList ) ):
            sourceList[i].setCtlData( *targetDataList[i] )
            targetList[i].setCtlData( *sourceDataList[i] )




def setCharacterCurrentAsDefault():
    
    transforms = cmds.ls( 'Ctl_*', type='transform' )
    
    ctls = []
    for transform in transforms:
        shapes = cmds.listRelatives( transform, s=1 )
        if not shapes: continue
        ctls.append( transform )
    
    for ctl in ctls:
        attrs  = cmds.listAttr( ctl, ud=1, k=1 )
        if not attrs: attrs = []
        cbAttrs = cmds.listAttr( ctl, ud=1, cb=1 )
        if not cbAttrs: cbAttrs = []
        attrs += cbAttrs
        
        for attr in attrs:
            value = cmds.getAttr( ctl + '.' + attr )
            cmds.addAttr( ctl + '.' + attr, e=1, dv=value )
        



class ControllerMirrorInfo:
    
    def __init__(self, ctlName ):
        
        self.ctlName = ctlName
        addAttr( ctlName, ln= RigControllerControl.origNameAttr, dt='string' )
        cmds.setAttr( ctlName + '.' + RigControllerControl.origNameAttr, self.ctlName, type='string' )
        
        targetPrefix = ''
        for i in range( len( RigControllerControl.leftPrefixList ) ):
            leftPrefix = RigControllerControl.leftPrefixList[i]
            if self.ctlName.find( leftPrefix ) != -1:
                targetPrefix = leftPrefix
                break
        for i in range( len( RigControllerControl.rightPrefixList ) ):
            rightPrefix = RigControllerControl.rightPrefixList[i]
            if self.ctlName.find( rightPrefix ) != -1:
                targetPrefix = rightPrefix
                break
        
        if targetPrefix:
            addAttr( ctlName, ln= RigControllerControl.sidePrefixAttr, dt='string' )
            cmds.setAttr( ctlName + '.' + RigControllerControl.sidePrefixAttr, targetPrefix, type='string' )
        
    
    def setParentName( self, parentName ):
        
        self.parentName = parentName
        addAttr( self.ctlName, ln= RigControllerControl.parentAttr, dt='string' )
        cmds.setAttr( self.ctlName+ '.' + RigControllerControl.parentAttr, self.parentName, type='string' )
        
    
    def setReverseAttrs( self, reverseAttrs ):
        
        self.reverseAttrs = reverseAttrs
        addAttr( self.ctlName, ln= RigControllerControl.reverseAttrs, dt='string' )
        cmds.setAttr( self.ctlName+ '.' + RigControllerControl.reverseAttrs, self.reverseAttrs, type='string' )
    
    
    def setOuterMatrixAttr( self, inputMtx ):
        
        if type( inputMtx ) == str:
            matrixStr = inputMtx
        else:
            matrixStr = str( matrixToList( inputMtx ) )
        
        self.outerMatrix = matrixStr
        addAttr( self.ctlName, ln= RigControllerControl.outerMatrixAttr, dt='string' )
        cmds.setAttr( self.ctlName+ '.' + RigControllerControl.outerMatrixAttr, self.outerMatrix, type='string' )
    

    def setInnerMatrixAttr( self, inputMtx ):
        
        if type( inputMtx ) == str:
            matrixStr = inputMtx
        else:
            matrixStr = str( matrixToList( inputMtx ) )
        
        self.innerMatrix = matrixStr
        addAttr( self.ctlName, ln= RigControllerControl.innerMatrixAttr, dt='string' )
        cmds.setAttr( self.ctlName+ '.' + RigControllerControl.innerMatrixAttr, self.innerMatrix, type='string' )
    
    


def setCharacterSymmetryInfo():
    
    reverseMatrix = [-1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1]
    xRotateMatrix = [1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1]
    yRotateMatrix = [-1,0,0,0, 0,1,0,0, 0,0,-1,0, 0,0,0,1]
    zRotateMatrix = [1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1]
    xMirrorMatrix = [-1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    yMirrorMatrix = [1,0,0,0, 0,-1,0,0, 0,0,1,0, 0,0,0,1]
    zMirrorMatrix = [1,0,0,0, 0,1,0,0, 0,0,-1,0, 0,0,0,1]
    
    Ctl_World = ['Ctl_World', 'PCtl_World', '', '', '' ]
    Ctl_Move  = ['Ctl_Move', 'Ctl_World', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Fly   = ['Ctl_Fly', 'Ctl_Move', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Root  = ['Ctl_Root', 'Ctl_Fly', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_PervisRotator     = ['Ctl_PervisRotator', 'Ctl_Root', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_BodyRotatorFirst  = ['Ctl_BodyRotatorFirst', 'Ctl_PervisRotator', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_BodyRotatorSecond = ['Ctl_BodyRotatorSecond', 'Ctl_BodyRotatorFirst', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Chest  = ['Ctl_Chest', 'Ctl_BodyRotatorSecond', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Waist  = ['Ctl_Waist', 'Ctl_BodyRotatorFirst', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Hip    = ['Ctl_Hip', 'Ctl_Waist', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Neck   = ['Ctl_Neck', 'Ctl_Chest', '', xMirrorMatrix, yRotateMatrix ]
    Ctl_Head   = ['Ctl_Head', 'Ctl_Neck', '', xMirrorMatrix, yRotateMatrix ]
    
    Ctl_HipPos_SIDE_   = ['Ctl_HipPos_SIDE_', 'Ctl_Hip', '', xMirrorMatrix, reverseMatrix ]
    Ctl_IkLeg_SIDE_02  = ['Ctl_IkLeg_SIDE_02', 'Ctl_HipPos_SIDE_', '', reverseMatrix, reverseMatrix ]
    Ctl_Leg_SIDE_PoleV = ['Ctl_Leg_SIDE_PoleV', 'Ctl_IkLeg_SIDE_02', '', reverseMatrix, reverseMatrix ]
    Ctl_FootIkFoot_SIDE_Piv = ['Ctl_FootIkFoot_SIDE_Piv', 'Ctl_IkLeg_SIDE_02', '', reverseMatrix, reverseMatrix ]
    Ctl_FootIkToe_SIDE_End  = ['Ctl_FootIkToe_SIDE_End', 'Ctl_FootIkFoot_SIDE_Piv', '', reverseMatrix, reverseMatrix ]
    Ctl_FootIkToe_SIDE_     = ['Ctl_FootIkToe_SIDE_', 'Ctl_FootIkToe_SIDE_End', '', reverseMatrix, reverseMatrix ]
    
    Ctl_FkLeg_SIDE_00 = ['Ctl_FkLeg_SIDE_00', 'Ctl_HipPos_SIDE_', '', reverseMatrix, reverseMatrix ]
    Ctl_FkLeg_SIDE_01 = ['Ctl_FkLeg_SIDE_01', 'Ctl_FkLeg_SIDE_00', '', reverseMatrix, reverseMatrix ]
    Ctl_FkLeg_SIDE_02 = ['Ctl_FkLeg_SIDE_02', 'Ctl_FkLeg_SIDE_01', '', reverseMatrix, reverseMatrix ]
    Ctl_FootFkToe_SIDE_ = ['Ctl_FootFkToe_SIDE_', 'Ctl_FkLeg_SIDE_02', '', reverseMatrix, reverseMatrix ]
    
    Ctl_BlLeg_SIDE_02 = ['Ctl_BlLeg_SIDE_02', 'Ctl_HipPos_SIDE_', '',  '', '' ]

    Ctl_clavicle_SIDE_ = ['Ctl_clavicle_SIDE_', 'Ctl_Chest', '', xMirrorMatrix, yRotateMatrix ]
    
    Ctl_IkArm_SIDE_02 = ['Ctl_IkArm_SIDE_02', 'Ctl_clavicle_SIDE_', '', reverseMatrix, reverseMatrix ]
    Ctl_Arm_SIDE_PoleV = ['Ctl_Arm_SIDE_PoleV', 'Ctl_IkArm_SIDE_02', '', reverseMatrix, reverseMatrix ]
    
    Ctl_FkArm_SIDE_00 = ['Ctl_FkArm_SIDE_00', 'Ctl_clavicle_SIDE_', '', reverseMatrix, reverseMatrix ]
    Ctl_FkArm_SIDE_01 = ['Ctl_FkArm_SIDE_01', 'Ctl_FkArm_SIDE_00', '',  reverseMatrix, reverseMatrix ]
    Ctl_FkArm_SIDE_02 = ['Ctl_FkArm_SIDE_02', 'Ctl_FkArm_SIDE_01', '',  reverseMatrix, reverseMatrix ]
    
    Ctl_BlArm_SIDE_02 = ['Ctl_BlArm_SIDE_02', 'Ctl_clavicle_SIDE_', '',  '', '' ]
    
    Ctl_Finger_SIDE_ = [ 'Ctl_Finger_SIDE_', 'Ctl_FkArm_SIDE_02,Ctl_IkArm_SIDE_02', '', '', '' ]
    
    listCtlInfo = [Ctl_World, Ctl_Move, Ctl_Fly, Ctl_Root, Ctl_PervisRotator, Ctl_BodyRotatorFirst, Ctl_BodyRotatorSecond,
                    Ctl_Chest, Ctl_Waist, Ctl_Hip, Ctl_Neck, Ctl_Head,
                    Ctl_HipPos_SIDE_, Ctl_IkLeg_SIDE_02, Ctl_Leg_SIDE_PoleV,
                    Ctl_FootIkFoot_SIDE_Piv, Ctl_FootIkToe_SIDE_End, Ctl_FootIkToe_SIDE_,
                    Ctl_FkLeg_SIDE_00, Ctl_FkLeg_SIDE_01, Ctl_FkLeg_SIDE_02, Ctl_FootFkToe_SIDE_,
                    Ctl_clavicle_SIDE_, Ctl_IkArm_SIDE_02, Ctl_Arm_SIDE_PoleV,
                    Ctl_FkArm_SIDE_00, Ctl_FkArm_SIDE_01, Ctl_FkArm_SIDE_02,
                    Ctl_Finger_SIDE_, Ctl_BlLeg_SIDE_02, Ctl_BlArm_SIDE_02 ]
    
    for ctlInfo in listCtlInfo:
        sideReplaceList = [['_SIDE_','_SIDE_']]
        if ctlInfo[0].find( '_SIDE_' ) != -1:
            sideReplaceList = [('_SIDE_','_L_'),('_SIDE_','_R_')]
        
        for replaceSrc, replaceDst in sideReplaceList:
            inst = ControllerMirrorInfo( ctlInfo[0].replace( replaceSrc, replaceDst ) )
            inst.setParentName( ctlInfo[1].replace( replaceSrc, replaceDst ) )
            inst.setReverseAttrs( ctlInfo[2] )
            inst.setOuterMatrixAttr( ctlInfo[3] )
            inst.setInnerMatrixAttr( ctlInfo[4] )
    
    listFingerNames = ['Ctl_Thumb_SIDE_*', 'Ctl_Index_SIDE_*', 'Ctl_Middle_SIDE_*', 'Ctl_Ring_SIDE_*', 'Ctl_Pinky_SIDE_*']
    
    for fingerName in listFingerNames:
        sideReplaceList = [('_SIDE_','_L_'),('_SIDE_','_R_')]
        for replaceSrc, replaceDst in sideReplaceList:
            fingerCtls = cmds.ls( fingerName.replace( replaceSrc, replaceDst ), type='transform' )
            if not fingerCtls: continue
            beforeParent = Ctl_Finger_SIDE_[0].replace( replaceSrc, replaceDst )
            for fingerCtl in fingerCtls:
                if not cmds.listRelatives( fingerCtl, s=1 ): continue
                inst = ControllerMirrorInfo( fingerCtl )
                inst.setParentName( beforeParent )
                inst.setReverseAttrs( '' )
                inst.setOuterMatrixAttr( reverseMatrix )
                inst.setInnerMatrixAttr( reverseMatrix )
                beforeParent = fingerCtl


