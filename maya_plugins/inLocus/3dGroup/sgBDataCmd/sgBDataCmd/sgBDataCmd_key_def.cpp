#include  "sgBDataCmd_key.h"
#include  "sgBDataCmd.h"

#include <io.h>
#include <conio.h>


MStatus sgBDataCmd_key::setObjectKeyDataDefault( sgObject_keyData& objectKeyData, const MDagPath& dagPathTarget, bool bMatrixType )
{
	MStatus status;
	objectKeyData.oTargetNode = dagPathTarget.node();
	objectKeyData.numAttr = 0;
	objectKeyData.namesAttribute.clear();
	objectKeyData.lengthTime = 0;
	objectKeyData.dArrTime.clear();
	objectKeyData.dArrValuesArray.clear();

	MFnDagNode fnDagNode = dagPathTarget;

	MPlugArray plugArrTransform;
	MPlugArray plugArrVis;

	plugArrTransform.append( fnDagNode.findPlug( "tx" ) );
	plugArrTransform.append( fnDagNode.findPlug( "ty" ) );
	plugArrTransform.append( fnDagNode.findPlug( "tz" ) );
	plugArrTransform.append( fnDagNode.findPlug( "rx" ) );
	plugArrTransform.append( fnDagNode.findPlug( "ry" ) );
	plugArrTransform.append( fnDagNode.findPlug( "rz" ) );
	plugArrTransform.append( fnDagNode.findPlug( "sx" ) );
	plugArrTransform.append( fnDagNode.findPlug( "sy" ) );
	plugArrTransform.append( fnDagNode.findPlug( "sz" ) );

	plugArrVis.append( fnDagNode.findPlug( "v" ) );

	if( bMatrixType )
	{
		if( plugsHasConnection( plugArrVis ) )
		{
			objectKeyData.numAttr++;
			objectKeyData.namesAttribute.append( "visibility" );
		}
		if( plugsHasConnection( plugArrTransform ) )
		{
			objectKeyData.numAttr += 9;
			objectKeyData.namesAttribute.append( "translateX" );
			objectKeyData.namesAttribute.append( "translateY" );
			objectKeyData.namesAttribute.append( "translateZ" );
			objectKeyData.namesAttribute.append( "rotateX" );
			objectKeyData.namesAttribute.append( "rotateY" );
			objectKeyData.namesAttribute.append( "rotateZ" );
			objectKeyData.namesAttribute.append( "scaleX" );
			objectKeyData.namesAttribute.append( "scaleY" );
			objectKeyData.namesAttribute.append( "scaleZ" );
		}
	}
	else
	{
		MPlugArray plugArr;
		for( unsigned int j=0; j< plugArrTransform.length(); j++ )
		{
			MPlug& plug = plugArrTransform[j];

			plug.connectedTo( plugArr, true, false );
			if( !plugArr.length() )
			{
				MPlug plugParent = plug.parent( &status );
				if( !status ) continue;
				plugParent.connectedTo( plugArr, true, false );
				if( !plugArr.length() ) continue;
			}
			objectKeyData.numAttr++;
			objectKeyData.namesAttribute.append( MFnAttribute( plug.attribute() ).name() );
		}
		plugArrVis[0].connectedTo( plugArr, true, false );
		if( plugArr.length() )
		{
			objectKeyData.numAttr++;
			objectKeyData.namesAttribute.append( MFnAttribute( plugArrVis[0].attribute() ).name() );
		}
	}
	objectKeyData.dArrValuesArray.clear();
	return MS::kSuccess;
}




MStatus sgBDataCmd_key::startExport( MString pathFolder )
{
	MStatus status;

	m_filePaths.clear();
	for( unsigned int i=0; i< m_pathArrExport.length(); i++ )
	{
		MFnDagNode fnNode( m_pathArrExport[i], &status );
		if( !status ) continue;
		MString targetName = fnNode.partialPathName();
		targetName.substitute( ":", "_" );
		targetName.substitute( "|", "_" );
		m_filePaths.append( pathFolder + "\\" + targetName + ".sgKeyData" );
	}

	m_objectKeyDatasExport.setLength( m_pathArrExport.length() );

	for( unsigned int i=0; i< m_pathArrExport.length(); i++ )
	{
		setObjectKeyDataDefault( m_objectKeyDatasExport[i], m_pathArrExport[i], m_exportByMatrix );

		unsigned int unit = MTime().unit();
		MString  nameTarget = MFnDagNode( m_pathArrExport[i] ).fullPathName();

		std::ofstream outFile( m_filePaths[i].asChar(), ios::binary );

		writeString( nameTarget, outFile );
		writeUnsignedInt( unit, outFile );
		writeStringArray( m_objectKeyDatasExport[i].namesAttribute, outFile );

		outFile.close();
	}
	return MS::kSuccess;
}


MStatus sgBDataCmd_key::writeData( bool exportByMatrix )
{
	MStatus status;
	
	double dTime  = MAnimControl::currentTime().value();

	if( exportByMatrix )
	{
		for( unsigned int i=0; i<m_pathArrExport.length(); i++ )
		{
			m_objectKeyDatasExport[i].lengthTime++;
			m_objectKeyDatasExport[i].dArrTime.append( dTime );
			MFnDependencyNode fnNode( m_objectKeyDatasExport[i].oTargetNode );

			if( m_objectKeyDatasExport[i].numAttr == 0 )
			{
				continue;
			}
			if( m_objectKeyDatasExport[i].numAttr == 1 )
			{
				MPlug plug = fnNode.findPlug( m_objectKeyDatasExport[i].namesAttribute[0] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( plug.asDouble() );
			}
			else
			{
				if( m_objectKeyDatasExport[i].numAttr == 10 )
				{
					MPlug plug = fnNode.findPlug( m_objectKeyDatasExport[i].namesAttribute[0] );
					m_objectKeyDatasExport[i].dArrValuesArray.append( plug.asDouble() );
				}

				MDagPath dagPath;
				dagPath.getAPathTo( m_objectKeyDatasExport[i].oTargetNode, dagPath );

				MTransformationMatrix trMtx = dagPath.inclusiveMatrix() * dagPath.exclusiveMatrixInverse();
				MVector trans   = trMtx.translation( MSpace::kTransform );
				double rotValues[3] ={0,0,0};
				MTransformationMatrix::RotationOrder order = MTransformationMatrix::kZXY;
				trMtx.getRotation( rotValues, order, MSpace::kTransform );
				double scales[3];
				trMtx.getScale( scales, MSpace::kTransform );

				m_objectKeyDatasExport[i].dArrValuesArray.append( trans.x );
				m_objectKeyDatasExport[i].dArrValuesArray.append( trans.y );
				m_objectKeyDatasExport[i].dArrValuesArray.append( trans.z );
				m_objectKeyDatasExport[i].dArrValuesArray.append( rotValues[0] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( rotValues[1] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( rotValues[2] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( scales[0] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( scales[1] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( scales[2] );
			}
		}
	}
	else
	{
		for( unsigned int i=0; i<m_pathArrExport.length(); i++ )
		{
			m_objectKeyDatasExport[i].lengthTime++;
			m_objectKeyDatasExport[i].dArrTime.append( dTime );
			MFnDependencyNode fnNode( m_objectKeyDatasExport[i].oTargetNode );

			for( unsigned int j=0; j< m_objectKeyDatasExport[i].numAttr; j++ )
			{
				MPlug plug = fnNode.findPlug( m_objectKeyDatasExport[i].namesAttribute[j] );
				m_objectKeyDatasExport[i].dArrValuesArray.append( plug.asDouble() );
			}
		}
	}

	return MS::kSuccess;
}


void sgBDataCmd_key::endExport()
{
	for( unsigned int i=0; i< m_pathArrExport.length(); i++ )
	{
		std::ofstream outFile( m_filePaths[i].asChar(), ios::binary | ios::app );
		writeDoubleArray( m_objectKeyDatasExport[i].dArrTime, outFile );
		for( unsigned int j=0; j< m_objectKeyDatasExport[i].dArrValuesArray.length(); j++ )
			outFile.write( ( char* )&m_objectKeyDatasExport[i].dArrValuesArray[j], sizeof( double ) );
		outFile.close();
	}

	m_objectKeyDatasExport.setLength( 0 );
	m_pathArrExport.clear();
	m_filePaths.clear();
}



MStatus sgBDataCmd_key::readData( MString nameFilePath )
{
	MStatus status;

	std::ifstream inFile( nameFilePath.asChar(), ios::binary );

	MString nameTarget;
	readString( nameTarget, inFile );

	MSelectionList selList;
	nameTarget.substitute( ":", "_" );
	MGlobal::getSelectionListByName( nameTarget, selList );
	MObject oTarget;
	selList.getDependNode( 0, oTarget );
	MFnDagNode fnNode( oTarget );

	m_objectKeyDataImport.oTargetNode = oTarget;
	readUnsignedInt( m_objectKeyDataImport.unit, inFile );

	readStringArray( m_objectKeyDataImport.namesAttribute, inFile );
	readDoubleArray( m_objectKeyDataImport.dArrTime, inFile );

	unsigned int lengthValues = m_objectKeyDataImport.namesAttribute.length() * m_objectKeyDataImport.dArrTime.length();
	m_objectKeyDataImport.dArrValuesArray.setLength( lengthValues );
	for( unsigned int j=0; j<lengthValues; j++ )
		inFile.read( ( char* )&m_objectKeyDataImport.dArrValuesArray[j], sizeof( double ) );

	inFile.close();

	return MS::kSuccess;
}


MStatus sgBDataCmd_key::importData()
{
	MStatus status;

	MTime::Unit currentUnit = MTime().unit();

	MPlugArray connections;

	sgObject_keyData& objectKeyData = m_objectKeyDataImport;
	MObject& oTarget = objectKeyData.oTargetNode;
	MDoubleArray& dArrTime = objectKeyData.dArrTime;
	MTime::Unit unit = (MTime::Unit)objectKeyData.unit;
	MFnDagNode fnNode = oTarget;

	MPlugArray targetPlugs;

	unsigned int numAttr = objectKeyData.namesAttribute.length();
	unsigned int lengthTime = dArrTime.length();

	for( unsigned int j=0; j<numAttr; j++ )
	{
		if( numAttr <= j ) break;
		MPlug targetPlug = fnNode.findPlug( objectKeyData.namesAttribute[j] );
		
		targetPlug.connectedTo( connections, true, false );
		if( connections.length() ){
			m_dgMod_connection.disconnect( connections[0], targetPlug );
			m_dgMod_delete.deleteNode( connections[0].node() );
		}
		m_dgMod_connection.doIt();
		m_dgMod_delete.doIt();

		MObject oAnimCurve = MFnAnimCurve().create( targetPlug );
		m_oArrKeyAfter.append( oAnimCurve );
		MFnAnimCurve fnAnimCurve( oAnimCurve );
		for( unsigned int k=0; k<lengthTime; k++ )
		{
			double& dTime  = dArrTime[k];
			double& dValue = objectKeyData.dArrValuesArray[ k*numAttr+j ];

			MTime mTime( dTime, unit );
			mTime.setUnit( currentUnit );
			fnAnimCurve.addKeyframe( mTime, dValue );
		}
	}

	return MS::kSuccess;
};