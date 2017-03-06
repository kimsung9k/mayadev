#include  "sgHair_controlJoint.h"



MMatrix sgHair_controlJoint::buildMatrix( MVector vX, MVector vY, MVector vZ, MPoint pPoint )
{
	MMatrix mtxReturn;

	mtxReturn( 0, 0 ) = vX.x;
	mtxReturn( 0, 1 ) = vX.y;
	mtxReturn( 0, 2 ) = vX.z;
	mtxReturn( 1, 0 ) = vY.x;
	mtxReturn( 1, 1 ) = vY.y;
	mtxReturn( 1, 2 ) = vY.z;
	mtxReturn( 2, 0 ) = vZ.x;
	mtxReturn( 2, 1 ) = vZ.y;
	mtxReturn( 2, 2 ) = vZ.z;
	mtxReturn( 3, 0 ) = pPoint.x;
	mtxReturn( 3, 1 ) = pPoint.y;
	mtxReturn( 3, 2 ) = pPoint.z;

	return mtxReturn;
}



void sgHair_controlJoint::normalizeMatrix( MMatrix& mtx )
{
	MVector vAim( mtx(0,0), mtx(0,1), mtx(0,2) );
	MVector vUp( mtx(1,0), mtx(1,1), mtx(1,2) );
	MVector vCross( mtx(2,0), mtx(2,1), mtx(2,2) );

	vAim.normalize();
	vUp.normalize();
	vCross.normalize();

	mtx( 0, 0 ) = vAim.x; mtx( 0, 1 ) = vAim.y; mtx( 0, 2 ) = vAim.z;
	mtx( 1, 0 ) = vUp.x;  mtx( 1, 1 ) = vUp.y;  mtx( 1, 2 ) = vUp.z;
	mtx( 2, 0 ) = vCross.x;  mtx( 2, 1 ) = vCross.y;  mtx( 2, 2 ) = vCross.z;
}



void sgHair_controlJoint::cleanMatrix( MMatrix& mtx )
{
	MVector vAim( mtx(0,0), mtx(0,1), mtx(0,2) );
	MVector vUp( mtx(1,0), mtx(1,1), mtx(1,2) );

	MVector vCross = vAim ^ vUp;
	vUp = vCross ^ vAim;

	vAim.normalize();
	vUp.normalize();
	vCross.normalize();

	mtx( 0, 0 ) = vAim.x; mtx( 0, 1 ) = vAim.y; mtx( 0, 2 ) = vAim.z;
	mtx( 1, 0 ) = vUp.x;  mtx( 1, 1 ) = vUp.y;  mtx( 1, 2 ) = vUp.z;
	mtx( 2, 0 ) = vCross.x;  mtx( 2, 1 ) = vCross.y;  mtx( 2, 2 ) = vCross.z;
}



MMatrix sgHair_controlJoint::getAngleWeightedMatrix( const MMatrix& targetMtx, double weight )
{
	MMatrix mtx;
	if( m_bStaticRotation )
	{
		mtx = MMatrix() * ( weight-1 ) + targetMtx * weight;
		cleanMatrix( mtx );
	}
	else
	{
		MVector vUpDefault( 0, 1, 0 );
		MVector vCrossDefault( 0,0,1 );
		MVector vUpInput( targetMtx(1,0), targetMtx(1,1), targetMtx(1,2) );

		double angleUp = vUpInput.angle( vUpDefault ) * weight;

		if( vUpInput.x == 0 && vUpInput.z == 0 ) vUpInput.x = 1;
		MVector direction( vUpInput.x, 0, vUpInput.z );
		direction.normalize();

		MVector vUp( sin( angleUp ) * direction.x, cos( angleUp ), sin( angleUp ) * direction.z );
		double dot = vUp * MVector( 0.0, 0.0, 1.0 );
		MVector vCross( 0.0, -dot, (dot+1) );
		MVector vAim = vUp ^ vCross;

		vAim.normalize();
		vUp.normalize();
		vCross = vAim ^ vUp;

		mtx( 0, 0 ) = vAim.x;
		mtx( 0, 1 ) = vAim.y;
		mtx( 0, 2 ) = vAim.z;
		mtx( 1, 0 ) = vUp.x;
		mtx( 1, 1 ) = vUp.y;
		mtx( 1, 2 ) = vUp.z;
		mtx( 2, 0 ) = vCross.x;
		mtx( 2, 1 ) = vCross.y;
		mtx( 2, 2 ) = vCross.z;
	}
	return mtx;
}





MStatus sgHair_controlJoint::getTopJointFromPlug( const MPlug& plug, MObject& oTopJoint )
{
	MStatus status;

	MPlugArray plugArrConnection;
	plug.connectedTo( plugArrConnection, true, false );

	if( !plugArrConnection.length() ) return MS::kSuccess;
	oTopJoint = plugArrConnection[0].node();

	return MS::kSuccess;
}



MStatus sgHair_controlJoint::getJointPositionBaseWorld()
{
	MStatus status;

	if( !m_bStaticRotation )
	{
		MVector vAim;
		MVector vUp( m_mtxJointParentBase(1,0), m_mtxJointParentBase(1,1), m_mtxJointParentBase(1,2) );
		MVector vCross;
		MMatrix mtxLocal;
		MMatrix mtxWorld = m_mtxJointParentBase;

		m_mtxArrBase.setLength( m_cvs.length() );

		for( int i=0; i< m_cvs.length()-1; i++ )
		{
			vAim = ( m_cvs[i+1] - m_cvs[i] )*m_mtxBaseCurve;
			vCross = vAim ^ vUp;
			vUp = vCross ^ vAim;
			vAim.normalize();
			vUp.normalize();
			vCross.normalize();
			m_mtxArrBase[i] = buildMatrix( vAim, vUp, vCross, m_cvs[i]*m_mtxBaseCurve );
		}
		MPoint pointWorld = m_cvs[m_cvs.length()-1]*m_mtxBaseCurve;

		MMatrix mtxLastWorld;
		mtxLastWorld( 3, 0 ) = pointWorld.x;
		mtxLastWorld( 3, 1 ) = pointWorld.y;
		mtxLastWorld( 3, 2 ) = pointWorld.z;

		m_mtxArrBase[m_cvs.length()-1] = mtxLastWorld;
	}
	else
	{
		MVector aim( 1,0,0 );
		MVector up( 0,1,0 );
		MVector cross( 0,0,1 );

		m_mtxArrBase.setLength( m_cvs.length() );

		aim *= m_mtxJointParentBase;
		up *= m_mtxJointParentBase;
		cross *= m_mtxJointParentBase;

		for( int i=0; i< m_cvs.length(); i++ )
		{
			m_mtxArrBase[i] = buildMatrix( aim, up, cross, m_cvs[i]*m_mtxBaseCurve );
		}
	}

	return MS::kSuccess;
}




MStatus sgHair_controlJoint::setGravityJointPositionWorld()
{
	MStatus status;

	m_mtxArrGravityAdd = m_mtxArrBase;

	if( m_weightGravity == 0 ) return MS::kSuccess;

	if( !m_bStaticRotation )
	{
		double minParam = m_paramGravity - m_rangeGravity;
		double maxParam = m_paramGravity;
		double divRate = maxParam - minParam;
		if( divRate == 0 ) divRate = 0.0001;

		if( minParam > m_mtxArrBase.length()-1 ) return MS::kSuccess;
		MDoubleArray dArrGravityWeights;
		dArrGravityWeights.setLength( m_mtxArrBase.length() );

		double beforeWeight = 1.0;
		for( int i= m_mtxArrBase.length()-1; i > minParam, i >= 0; i-- )
		{
			double paramRate = ( i - minParam ) / divRate;
			if( paramRate > 1 ) paramRate = 1.0;
			else if( paramRate < 0 ) paramRate = 0.0;
			double cuRate = beforeWeight - paramRate;
			if( cuRate < 0 ) cuRate = 0;
			dArrGravityWeights[i] = cuRate * m_weightGravity;
			beforeWeight = paramRate;
		}

		MMatrix mtxDefault;
		MMatrix mtxMult;

		for( int i= m_mtxArrBase.length()-1; i > minParam, i >= 0; i-- )
		{
			if( dArrGravityWeights[i] == 0 ) continue;
			double weight = dArrGravityWeights[i];

			mtxDefault( 3,0 ) = m_mtxArrBase[i]( 3,0 );
			mtxDefault( 3,1 ) = m_mtxArrBase[i]( 3,1 );
			mtxDefault( 3,2 ) = m_mtxArrBase[i]( 3,2 );

			mtxMult = getAngleWeightedMatrix( m_mtxGravityOffset, weight );
			mtxMult( 3,0 ) = m_mtxArrBase[i]( 3,0 );
			mtxMult( 3,1 ) = m_mtxArrBase[i]( 3,1 );
			mtxMult( 3,2 ) = m_mtxArrBase[i]( 3,2 );

			mtxMult = mtxDefault.inverse() * mtxMult;

			for( int j=i; j< m_mtxArrBase.length(); j++ )
			{
				m_mtxArrGravityAdd[j] *= mtxMult;
			}
		}
	}
	else
	{
		double minParam = m_paramGravity - m_rangeGravity;
		double maxParam = m_paramGravity;
		double divRate = maxParam - minParam;
		if( divRate == 0 ) divRate = 0.0001;

		MDoubleArray dArrGravityWeights;
		dArrGravityWeights.setLength( m_mtxArrBase.length() );

		double weight;
		for( int i= 0; i < m_mtxArrBase.length(); i++ )
		{
			if( i < minParam )weight=0;
			else weight = (i-minParam)/divRate;
			if( weight > 1 ) weight = 1;
			m_mtxArrGravityAdd[i] = m_mtxArrBase[i];

			double invWeight = 1-weight;
			MMatrix mtx = weight * m_mtxGravityOffset*m_mtxArrBase[i] + invWeight * m_mtxArrBase[i]; 

			cleanMatrix( mtx );

			m_mtxArrGravityAdd[i] = mtx;
			m_mtxArrGravityAdd[i]( 3,0 ) = m_mtxArrBase[i]( 3,0 );
			m_mtxArrGravityAdd[i]( 3,1 ) = m_mtxArrBase[i]( 3,1 );
			m_mtxArrGravityAdd[i]( 3,2 ) = m_mtxArrBase[i]( 3,2 );
		}
		cout << endl;
	}
	return MS::kSuccess;
}



MStatus sgHair_controlJoint::setOutput()
{
	MStatus status;

	m_vectorArrTransJoint.setLength( m_mtxArrGravityAdd.length() );
	m_vectorArrRotateJoint.setLength( m_mtxArrGravityAdd.length() );

	MMatrix mtxLocal;
	MMatrix parentInverse = m_mtxJointParentBase.inverse();

	MMatrixArray mtxArrInParent, mtxArrInParentNormalize;
	mtxArrInParent.setLength( m_mtxArrGravityAdd.length() );
	mtxArrInParentNormalize.setLength( m_mtxArrGravityAdd.length() );

	for( int i=0; i< m_mtxArrGravityAdd.length(); i++ )
	{
		mtxArrInParent[i] = m_mtxArrGravityAdd[i] * parentInverse;
		mtxArrInParentNormalize[i] = mtxArrInParent[i];
		normalizeMatrix( mtxArrInParentNormalize[i] );
	}

	MTransformationMatrix trMtx( mtxArrInParent[0] );
	m_vectorArrTransJoint[0] = trMtx.translation( MSpace::kTransform );
	m_vectorArrRotateJoint[0] = trMtx.eulerRotation().asVector();

	for( int i=1; i< m_mtxArrGravityAdd.length(); i++ )
	{
		mtxLocal = mtxArrInParent[i] * mtxArrInParentNormalize[i-1].inverse();

		MTransformationMatrix trMtx( mtxLocal );
		m_vectorArrTransJoint[i] = trMtx.translation( MSpace::kTransform );
		m_vectorArrRotateJoint[i] = trMtx.eulerRotation().asVector();
	}

	return MS::kSuccess;
}