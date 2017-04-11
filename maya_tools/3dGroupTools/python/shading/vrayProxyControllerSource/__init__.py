melString = """
///Produced by Sung Min Hong sophist82@naver.com

///This procedure is for proxy browsing...
global proc disableproxyName(){
    int $selected_export_type = `radioButtonGrp -q -select VrayExportGrp`;
    if($selected_export_type !=1){
        textFieldGrp -e -en 0 VraysetproxyName;        
        }
    else{
        textFieldGrp -e -en 1 VraysetproxyName;
        }        
    }
    
global proc get_shader(){
    string $get_shaders[] = `ls -l -sl`;
    if(`attributeExists "outColor" $get_shaders[0]`){
        textFieldButtonGrp -e -text $get_shaders[0] Vray_shader_to_proxy;
        }
    }

global proc vray_browse_proxies_export(){
    string $directory_names[];
    int $num_directories;
    string $project_path = `workspace -q -rd`;
    string $set_filepath[] =`fileDialog2 -okCaption "Set Path" -fm 3 -dir $project_path`;
    print $set_filepath[0];
    string $pure_directory;
    if($set_filepath[0] != ""){
        $num_directories = `tokenize $set_filepath[0] "/" $directory_names`;
        for($i=0; $i<($num_directories); $i++){
            $pure_directory += ($directory_names[$i]+"/");
            }
        textFieldButtonGrp -e -text $pure_directory VrayproxyExportdirectory;
        }
    }

global proc vray_browse_proxies(){
    string $directory_names[];
    int $num_directories;
    string $project_path = `workspace -q -rd`;
    string $set_filepath[] =`fileDialog2 -ff "*.vrmesh"-okCaption "List all proxy" -fm 2 -dir $project_path`;
    string $pure_directory;
    if($set_filepath[0] != ""){
        $num_directories = `tokenize $set_filepath[0] "/" $directory_names`;
        for($i=0; $i<($num_directories); $i++){
            $pure_directory += ($directory_names[$i]+"/");
            }
        textFieldButtonGrp -e -text $pure_directory Vrayproxydirectory;
        }
    list_all_proxy();
    }

global proc list_all_proxy(){
    textScrollList -e -ra vrayproxylist;
    string $getproxyfolder = `textFieldButtonGrp -q -tx Vrayproxydirectory`;
    string $getlistfiles[] = `getFileList -folder $getproxyfolder -filespec "*.vrmesh"`;
    int $getnumfiles = `size($getlistfiles)`;
    for($r=0; $r < $getnumfiles; $r++){
        if($getnumfiles<20){
            textScrollList -e -nr ($r+2) -append $getlistfiles[$r] vrayproxylist;
            }
        else if($getnumfiles>=20){
            textScrollList -e -nr 20 -append $getlistfiles[$r] vrayproxylist;
            }
        }
    }
    
global proc Export_proxies(){
    int $selected_export_type = `radioButtonGrp -q -select VrayExportGrp`;
    string $export_path = `textFieldButtonGrp -q -text VrayproxyExportdirectory`;
    string $filename_set = `textFieldGrp -q -text VraysetproxyName`;
    string $selected[] = `ls -sl`;
    int $numesel= size($selected);
    int $amount= 0;
    int $percentage;
    if($selected_export_type == 2){
        vrayCreateProxy -dir $export_path -fname "mesh.vrmesh" -overwrite 1 -exportType 2 -animType 0 -startFrame 0 -endFrame 10;
        }
    else if($selected_export_type == 1){
        vrayCreateProxy -dir $export_path -fname ($filename_set+".vrmesh") -overwrite 1 -exportType 1 -animType 0 -startFrame 0 -endFrame 10;
        }    
    else if($selected_export_type == 3){
        progressWindow -title "Importing Proxy mesh" -progress $amount -max $numesel -status ("Total "+$numesel+" proxies to import: 0%") -isInterruptable true;
        for($i=0; $i<size($selected); $i++){
            select $selected[$i];
            vrayCreateProxy -dir $export_path -fname ($selected[$i]+".vrmesh") -overwrite 1 -exportType 1 -animType 0 -startFrame 0 -endFrame 10;
            
            $amount += 1;
            $percentage= (($i+1)/$numesel)*100;
            progressWindow -edit -progress $amount -status ("Total "+$numesel+" proxies to import: "+$percentage+"%");
            }
        progressWindow -endProgress;
        }
    }
            
global proc import_proxies(){
    string $selecteditems_proxy[] = `textScrollList -q -si vrayproxylist`;
    string $list_shape[];
    string $list_sg[];
    string $list_mtl[];
    string $purefilename[];
    int $filenumtok;
    int $applyshader = `checkBox -q -v Vrayproxyapplyshader`;   
    int $numesel = `size($selecteditems_proxy)`;
    string $proxy_path = `textFieldButtonGrp -q -tx Vrayproxydirectory`;
    string $current_proxy_node[];
    string $proxy_material;
    string $proxy_shaders[];
    int $proxy_shaders_num;
    string $shaders_realname;   
    float $percentage;
    int $amount;
    progressWindow -title "Importing Proxy mesh" -progress $amount -max $numesel -status ("Total "+$numesel+" proxies to import: 0%") -isInterruptable true;

    for($e=0; $e<$numesel; $e++){
        if ( `progressWindow -query -isCancelled`){
            break;
            }
        $filenumtok = `tokenize $selecteditems_proxy[$e] "." $purefilename`;
        for($q=2; $q<$filenumtok; $q++){
            $purefilename[0] = ($purefilename[0]+$purefilename[($q-1)]);
            }
        vrayCreateProxyExisting("proxy__"+$purefilename[0], ($proxy_path + $selecteditems_proxy[$e]), "" );
        
        pickWalkUp;
        CenterPivot;
        $current_proxy_node = `ls -l -sl`;
            
        $list_shape = `listRelatives -shapes -f $current_proxy_node[0]`;
             
        $list_sg = `listConnections -type "shadingEngine" $list_shape[0]`;
        $list_mtl = `listConnections -s 1 -type "VRayMeshMaterial" $list_sg[0]`;
        
        if($applyshader){
            
            $proxy_material = $list_mtl[0];
            $proxy_shaders = `listAttr -multi -string "shaders" $proxy_material`;
            $proxy_shaders_num = `size($proxy_shaders)`;
            for($i = 0; $i < $proxy_shaders_num; $i++){
                $shaders_realname = `getAttr ($proxy_material+".shaderNames["+$i+"]")`;
                if(objExists($shaders_realname)==1){
                    connectAttr -f ($shaders_realname+".outColor") ($proxy_material+"."+$proxy_shaders[$i]);                       
                    }
                } 
            }
        $amount += 1;
        $percentage= (($e+1)/$numesel)*100;
        progressWindow -edit -progress $amount -status ("Total "+$numesel+" proxies to import: "+$percentage+"%");
        }
    progressWindow -endProgress;
    }

global proc substitude_proxies(){
    string $selected[] = `ls -sl`;
    string $list_sg[];
    string $list_mtl[];
    string $list_shape[];
    string $parents_selected[];
    string $sub_tran;
    string $animation_nodes[];
    string $destination_nodes[];
    string $pure_connect_name[];
    string $proxy_node_name;
    int $num_connected;
    float $sub_pivot[];
    string $selecteditems_proxy[] = `textScrollList -q -si vrayproxylist`;
    string $purefilename[];
    string $tok_purefilename[];
    string $pure_heirachy_name;
    int $filenumtok;
    int $applyshader = `checkBox -q -v Vrayproxyapplyshader`;   
    int $numesel = `size($selecteditems_proxy)`;
    string $proxy_path = `textFieldButtonGrp -q -tx Vrayproxydirectory`;
    string $current_proxy_node[];
    string $proxy_material;
    string $proxy_shaders[];
    int $proxy_shaders_num;
    string $shaders_realname;   
    float $percentage;
    int $amount;
    progressWindow -title "substituting Proxy mesh" -progress $amount -max $numesel -status ("Total "+size($selected)+" proxies to import: 0%") -isInterruptable true;
    
    for($i=0; $i<size($selected);$i++){
        if ( `progressWindow -query -isCancelled`){
            break;
            }
        
        $sub_pivot =`getAttr ($selected[$i]+".rotatePivot")`;
        $animation_nodes= `listConnections -type "animCurve" $selected[$i]`;
        $sub_tran=`createNode "transform" -n ("grp_"+$selected[$i])`;
        
        move -r $sub_pivot[0] $sub_pivot[1] $sub_pivot[2] ($sub_tran+".scalePivot") ($sub_tran+".rotatePivot");
        
        for($a=0; $a<size($animation_nodes);$a++){
            $destination_nodes = `listConnections -d 1 -plugs 1 $animation_nodes[$a]`;
            $num_connected = `tokenize $destination_nodes[0] "." $pure_connect_name`;
            connectAttr ($animation_nodes[$a]+".output") ($sub_tran+"."+$pure_connect_name[1]);
            }
        $parents_selected = `listRelatives -p -f $selected[$i]`;
        if($parents_selected[0]!=""){
            parent $sub_tran $parents_selected[0];
            }
        delete $selected[$i];
                   
        for($e=0; $e<$numesel; $e++){
            $filenumtok = `tokenize $selecteditems_proxy[$e] "." $purefilename`;
                for($q=2; $q<$filenumtok; $q++){
                    $purefilename[0] = ($purefilename[0]+$purefilename[($q-1)]);
                    }   
            vrayCreateProxyExisting($purefilename[0], ($proxy_path + $selecteditems_proxy[$e]), "");
            
            pickWalkUp;
            CenterPivot;
            $current_proxy_node = `ls -l -sl`;
            
            $list_shape = `listRelatives -shapes -f $current_proxy_node[0]`;
             
            $list_sg = `listConnections -type "shadingEngine" $list_shape[0]`;
            $list_mtl = `listConnections -s 1 -type "VRayMeshMaterial" $list_sg[0]`;

            if($applyshader){
                $proxy_material = $list_mtl[0];
                $proxy_shaders = `listAttr -multi -string "shaders" $proxy_material`;
                $proxy_shaders_num = `size($proxy_shaders)`;
                for($i = 0; $i < $proxy_shaders_num; $i++){
                    
                    $shaders_realname = `getAttr ($proxy_material+".shaderNames["+$i+"]")`;
                    if(objExists($shaders_realname)==1){
                        connectAttr -f ($shaders_realname+".outColor") ($proxy_material+"."+$proxy_shaders[$i]);                       
                        }
                    }
            
                }
            parent $current_proxy_node[0] $sub_tran;
            }                
        $amount += 1;
        $percentage= (($e+1)/size($selected))*100;
        progressWindow -edit -progress $amount -status ("Total "+size($selected)+" proxies to import: "+$percentage+"%");
        }
    progressWindow -endProgress;
    }
global proc disconnect_shaders(){
    string $current_proxy_node[] = `ls -l -sl`;       
    string $list_shape[];
    string $list_sg[];
    string $proxy_material[];
    int $proxy_shaders_num;
    string $shaders_realname;
    string $vraymesh[];
    string $material_status;    
    for($i=0; $i<size($current_proxy_node); $i++){            
        $list_shape = `listRelatives -shapes -f $current_proxy_node[$i]`;
        if(size($list_shape)!=0){
            $vraymesh = `listConnections -type "VRayMesh" $list_shape[0]`;
            }
        if(size($vraymesh)!=0 && size($list_shape)!=0){
            $list_sg = `listConnections -type "shadingEngine" $list_shape[0]`;
            $proxy_material = `listConnections -s 1 -type "VRayMeshMaterial" $list_sg[0]`;
            $proxy_shaders = `listAttr -multi -string "shaders" $proxy_material[0]`;
            $proxy_shaders_num = `size($proxy_shaders)`;
            for($m = 0; $m < $proxy_shaders_num; $m++){
                $material_status = `connectionInfo -sfd ($proxy_material[0]+"."+$proxy_shaders[$m])`;
                if($material_status != ""){
                    if(objExists($material_status)==1){
                        disconnectAttr ($material_status) ($proxy_material[0]+"."+$proxy_shaders[$m]);                       
                        }
                    }
                }
            }
        }    
   }

global proc reassign_shaders(){
    string $current_proxy_node[] = `ls -l -sl`;       
    string $list_shape[];
    string $list_sg[];
    string $proxy_material[];
    int $proxy_shaders_num;
    string $shaders_realname;
    string $vraymesh[];
    string $material_status;    
    for($i=0; $i<size($current_proxy_node); $i++){            
        $list_shape = `listRelatives -shapes -f $current_proxy_node[$i]`;
        if(size($list_shape)!=0){
            $vraymesh = `listConnections -type "VRayMesh" $list_shape[0]`;
            }
        if(size($vraymesh)!=0 && size($list_shape)!=0){
            $list_sg = `listConnections -type "shadingEngine" $list_shape[0]`;
            $proxy_material = `listConnections -s 1 -type "VRayMeshMaterial" $list_sg[0]`;
            $proxy_shaders = `listAttr -multi -string "shaders" $proxy_material[0]`;
            $proxy_shaders_num = `size($proxy_shaders)`;
            for($m = 0; $m < $proxy_shaders_num; $m++){
                $material_status = `connectionInfo -sfd ($proxy_material[0]+"."+$proxy_shaders[$m])`;
                $shaders_realname = `getAttr ($proxy_material[0]+".shaderNames["+$m+"]")`;
                if($material_status == ""){
                    if(objExists($shaders_realname)==1){
                        connectAttr -f ($shaders_realname+".outColor") ($proxy_material[0]+"."+$proxy_shaders[$m]);                       
                        }
                    }
                else if($material_status != ""){
                    disconnectAttr ($material_status) ($proxy_material[0]+"."+$proxy_shaders[$m]);
                    if(objExists($shaders_realname)==1){
                        connectAttr -f ($shaders_realname+".outColor") ($proxy_material[0]+"."+$proxy_shaders[$m]);
                        }
                    }
                }
            }
        }
    }
global proc Assign_shaders(){
    string $shader_name_to_assign = `textFieldButtonGrp -q-text Vray_shader_to_proxy`;
    string $current_proxy_node[] = `ls -l -sl`;       
    string $list_shape[];
    string $list_sg[];
    string $proxy_material[];
    int $proxy_shaders_num;
    string $shaders_realname;
    string $vraymesh[];
    string $material_status;    
    for($i=0; $i<size($current_proxy_node); $i++){            
        $list_shape = `listRelatives -shapes -f $current_proxy_node[$i]`;
        if(size($list_shape)!=0){
            $vraymesh = `listConnections -type "VRayMesh" $list_shape[0]`;
            }
        if(size($vraymesh)!=0 && size($list_shape)!=0){
            $list_sg = `listConnections -type "shadingEngine" $list_shape[0]`;
            $proxy_material = `listConnections -s 1 -type "VRayMeshMaterial" $list_sg[0]`;
            $proxy_shaders = `listAttr -multi -string "shaders" $proxy_material[0]`;
            $proxy_shaders_num = `size($proxy_shaders)`;
            for($m = 0; $m < $proxy_shaders_num; $m++){
                $material_status = `connectionInfo -sfd ($proxy_material[0]+"."+$proxy_shaders[$m])`;
                if($material_status != ""){
                    if(objExists($material_status)==1){
                        disconnectAttr ($material_status) ($proxy_material[0]+"."+$proxy_shaders[$m]);                       
                        connectAttr -f ($shader_name_to_assign+".outColor") ($proxy_material[0]+"."+$proxy_shaders[$m]);
                        }
                    }
                else if($material_status == ""){
                    connectAttr -f ($shader_name_to_assign+".outColor") ($proxy_material[0]+"."+$proxy_shaders[$m]);
                    }
                }
            }
        }    
   }
   
///This procedure is for adjusting Vray Proxy attributes.
global proc apply_val(){

    int $vrayuiincludefile = `checkBox -q -v vrayuiincludefile`;
    string $vraybasicfile = `textFieldButtonGrp -q -text VrayBasicfilename`;
    int $vrayproxybound = `checkBox -q -v Vrayproxyboundingbox`;
    int $vrayshowwholemesh = `checkBox -q -v Vrayshowwholemesh`;
    int $vrayexceptnorm =`checkBox -q -v Vrayexceptnormals`;
    float $vrayplayspeed = `floatSliderGrp -q -v Vrayplayspeed`;    
    float $vraystratoffset =`floatSliderGrp -q -v Vraystratoffset`; 
    string $vrayplaytype =`optionMenuGrp -q -v VrayplaybackType`;
    string $vrayshaderconnection =`optionMenuGrp -q -v Vrayshaderconnection`;       
    string $list_shape[];
        menuItem -label "Use global setting";
        menuItem -label "Use Maya Shader";
        menuItem -label "Use Proxy Shader";


    int $amount = 0;
    float $percentage;
    string $sel[] = `ls -l -sl`;
    int $sizsel = size($sel);
    string $vrayshapenodes[]; 
    string $vraymesh[];
    
    progressWindow -title "Applying Values to Proxies" -progress $amount -max $sizsel -status ("Total "+$sizsel+" proxies to copy: 0%") -isInterruptable true;
        
    for($i=0; $i<$sizsel; $i++){
        
        if ( `progressWindow -query -isCancelled` ) break;
        
        $list_shape = `listRelatives -shapes -f $sel[$i]`;
        if(size($list_shape)!=0){
            $vraymesh = `listConnections -type "VRayMesh" $list_shape[0]`;
            }     
        
        if($list_shape[0]!=""&& $vraymesh[0] !=""){
            select $sel[$i];        
            if($vrayuiincludefile){
                setAttr -type "string" ($vraymesh[0]+".fileName") $vraybasicfile;
                }
        
            setAttr ($vraymesh[0]+".showBBoxOnly") $vrayproxybound;
            setAttr ($vraymesh[0]+".dontSetNormals") $vrayexceptnorm;
        
            if($vrayproxybound==0){
                setAttr ($vraymesh[0]+".showWholeMesh") $vrayshowwholemesh;
                }
        
            setAttr ($vraymesh[0]+".animSpeed") $vrayplayspeed;
            setAttr ($vraymesh[0]+".animOffset") $vraystratoffset;
        
            if($vrayplaytype=="loop"){
                setAttr ($vraymesh[0]+".animType") 0;
                }
        
            else if($vrayplaytype=="Once"){
                setAttr ($vraymesh[0]+".animType") 1;
                }
        
            else if($vrayplaytype=="Ping-pong"){
                setAttr ($vraymesh[0]+".animType") 2;
                }
        
            else if($vrayplaytype=="Still"){
                setAttr ($vraymesh[0]+".animType") 3;
                }
        
            if($vrayshaderconnection=="Use global setting"){
                setAttr ($vraymesh[0]+".useMayaShader") 0;
                }
        
            else if($vrayshaderconnection=="Use Maya Shader"){
                setAttr ($vraymesh[0]+".useMayaShader") 1;
                }
        
            else if($vrayshaderconnection=="Use Proxy Shader"){
                setAttr ($vraymesh[0]+".useMayaShader") 2;
                }
            }
        $amount += 1;
        $percentage= (($i+1)/$sizsel)*100;
        progressWindow -edit -progress $amount -status ("Total "+$sizsel+" proxies to copy: "+$percentage+"%");
        }
    progressWindow -endProgress;
    select -cl;
    for($i=0; $i<$sizsel; $i++){
        select -add $sel[$i];
        }
    }

global proc vray_browse(){
    string $filepath =`fileDialog -m 0 -directoryMask "/usr/u/bozo/myFiles/*.vrmesh"`;
    if($filepath != ""){
        textFieldButtonGrp -e -text $filepath VrayBasicfilename;
        }
    }

global proc disableshowwholemesh(){
    int $whetherdisable=`checkBox -q -v Vrayproxyboundingbox`;
    if($whetherdisable==1){ 
        checkBox -e -en 0 Vrayshowwholemesh;
        }
    else{   
        checkBox -e -en 1 Vrayshowwholemesh;
        }
    }

global proc creatmeshfromproxy(){
    int $vrayreassignshader=`checkBox -q -v Vrayreassignshaders`;
    
    string $sel[] = `ls -l -sl`;
    int $sizsel = size($sel);
    string $vrayshapenodes[]; 
    string $vraymesh[];
        int $amount = 0;
    float $percentage;
    
    progressWindow -title "Restoring Proxy mesh" -progress $amount -max $sizsel -status ("Total "+$sizsel+" proxies to copy: 0%") -isInterruptable true;

    for($i=0; $i<$sizsel; $i++){
        if ( `progressWindow -query -isCancelled` ) break;
        select $sel[$i];
        pickWalk -d down;
        $vrayshapenodes = `ls -l -sl`;
        $vraymesh = `listConnections -type "VRayMesh" $vrayshapenodes`;
        setAttr ($vraymesh[0]+".reassignShaders") $vrayreassignshader;
        vray restoreMesh $vraymesh[0];
        $amount += 1;
        $percentage= (($i+1)/$sizsel)*100;
        progressWindow -edit -progress $amount -status ("Total "+$sizsel+" proxies to copy: "+$percentage+"%");
        }
    progressWindow -endProgress;
    }


global proc VrayProxyContrl(){
    if(`window -ex vrayproxymaincontrl`){
        deleteUI -window vrayproxymaincontrl;
    }
    
        
    string $mainWnd = `window -w 600 -h 200 -t "Vray Proxy Controller v.1.3" vrayproxymaincontrl`;
    
    scrollLayout -horizontalScrollBarThickness 16 -verticalScrollBarThickness 16;
    

    //Controlling Proxy Attributes.
    columnLayout -adj 1 ;

    separator -style "double" -w 200 -h 25;
    text -label "Export Proxy files" -align "left";
    separator -w 200 -h 25;
    radioButtonGrp -select 3 -onCommand "disableproxyName()" -vertical -numberOfRadioButtons 3 -label "Export type: " -labelArray3 "Export all selected objects in a single file" "Export each selected object in a seperate file" "Export each selected groups in seperate file" VrayExportGrp;
    string $selected[] = `ls -sl`;
    
    textFieldGrp -en 0 -label "Set Proxy filename" -text $selected[0] VraysetproxyName;
    separator -style "in" -w 200 -h 25;
    textFieldButtonGrp -label "Proxy Directory" -text "search through browse....." -buttonLabel "browse..." -bc "vray_browse_proxies_export()" VrayproxyExportdirectory;
    separator -style "in" -w 200 -h 25;

    button -l "Export all selected items." -w 160 -h 50 -c "Export_proxies()";
    
    separator -style "double" -w 200 -h 25 sep11;
    text -label "Import Proxy files" -align "left";
    separator -w 200 -h 25 sep12;

    textFieldButtonGrp -label "Proxy Directory" -text "search through browse....." -buttonLabel "browse..." -cc "list_all_proxy()" -bc "vray_browse_proxies()" Vrayproxydirectory;
    separator -w 200 -h 15 sep13;
    
    textScrollList -w 200 -nr 1 -ams 1 -h 150 vrayproxylist ;
    separator -w 200 -h 25 sep14;
    
    checkBox -v 1 -label "Apply shaders  (Check this, only if there is corresponding shaders in current scene!)" -align "left" Vrayproxyapplyshader;
        
    separator -w 200 -h 25 sep15;   
    
    button -l "Import all selected items." -w 160 -h 50 -c "import_proxies()";
    
    separator -style "in" -w 200 -h 5 ; 
    separator -style "in" -w 200 -h 5 ; 
    
    separator -style "in" -w 200 -h 5 ; 

    text -label "Usage: Select Proxies which to substitude, and select .vrmesh list from above which you want to substitude from" -align "left";
    text -label ".vrmesh files should have prefix before __ with the same name of proxies to substitude " -align "left";
    
    button -l "Substitude proxy based on nameing convention" -w 160 -h 50 -c "substitude_proxies()";
    
    separator -style "in" -w 200 -h 25;
    
    button -l "Disconnect Shaders Plugged on Proxy" -w 160 -h 30 -c "disconnect_shaders()";
    
    separator -style "in" -w 200 -h 25;
    
    button -l "Reassign Shaders Exist on current scene" -w 160 -h 30 -c "reassign_shaders()";
    
    separator -style "in" -w 200 -h 25;
    
    textFieldButtonGrp -label "Shader to Assign" -text "" -buttonLabel ">>>>>" -bc "get_shader()" Vray_shader_to_proxy; 
    button -l "Assign specified Shader to all proxies" -w 160 -h 30 -c "Assign_shaders()";
    
    separator -style "double" -w 200 -h 25 sep1;
    text -label "Basic parameters" -align "left";
    separator -w 200 -h 25 sep2;
    
    textFieldButtonGrp -label "File name" -text "search through browse....." -buttonLabel "browse..." -bc "vray_browse()" VrayBasicfilename;
    checkBox -v 0 -label "Bounding box" -align "left" -cc "disableshowwholemesh()" Vrayproxyboundingbox;
    checkBox -v 0 -label "Show whole mesh" -align "left" Vrayshowwholemesh;
    checkBox -v 0 -label "Don't set normals(much faster)" -align "left" Vrayexceptnormals;

    separator -style "double" -w 200 -h 25 sep3;
    text -label "Animation parameters" -align "left";
    separator -w 200 -h 25 sep4;

    floatSliderGrp -l "Playback speed" -f 1 -min 0 -max 10 -fmn 0 -fmx 1000000000 -pre 3 -s 0.001 -fs 0.01 -ss 0.1 -v 1 Vrayplayspeed;  
    floatSliderGrp -l "Start offset" -f 1 -min 0 -max 10 -fmn 0 -fmx 1000000000 -pre 3 -s 0.001 -fs 0.01 -ss 0.1 -v 0 Vraystratoffset;  
    optionMenuGrp -en 1 -label "Playback type" VrayplaybackType;
        menuItem -label "loop";
        menuItem -label "Once";
        menuItem -label "Ping-pong";
        menuItem -label "Still";
        
    separator -style "double" -w 200 -h 25 sep5;
    text -label "Shaders" -align "left";
    separator -w 200 -h 25 sep6;

    optionMenuGrp -en 1 -label "Shader connection" Vrayshaderconnection;
        menuItem -label "Use global setting";
        menuItem -label "Use Maya Shader";
        menuItem -label "Use Proxy Shader";
        
    separator -style "double" -w 200 -h 25 sep7;
    separator -w 200 -h 25 sep8;
    
    checkBox -v 0 -label "Include file path" -align "left" vrayuiincludefile;
    button -l "Apply values to all selections" -w 160 -h 50 -c "apply_val()";
    
    optionMenuGrp -e -v "loop" VrayplaybackType;
    optionMenuGrp -e -v "Use global setting" Vrayshaderconnection;
    
    separator -style "double" -w 200 -h 25 sep9;
    text -label "Restore the mesh" -align "left";
    separator -w 200 -h 25 sep10;
    
    checkBox -v 1 -label "Reassign shaders" -align "left" Vrayreassignshaders;
    button -l "Create a mesh from this proxy" -w 160 -h 50 -c "creatmeshfromproxy()";

    showWindow $mainWnd;
}
VrayProxyContrl();
"""