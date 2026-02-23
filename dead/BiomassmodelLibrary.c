// Copyright (c) 2007 Simosol Oy. Distributed under the GNU General Public License 2.0.

//////////////////////////////////////////////////////////////////////////////
//
//  BiomassmodelLibrary.cpp
//
//	Biomass model library - Source file
//
//	Here are the conventional calls of the functions

#include <stdio.h>
#include "BiomassmodelLibrary.h"
#include "SimoUtils.h"

#include <math.h>
#include <stdlib.h>
#include <string.h>


int Biomass_stem_pine_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(7.6066*(d/(d+14))+0.02*h+0.8658*log(h)-2.6864);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_bark_of_stem_pine_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(7.2482*(d/(d+16))+0.4487*log(h)-3.2765);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_with_needles_pine_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(13.3955*(d/(d+10))-1.1955*log(h)-2.5413);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_dead_branches_pine_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(7.1270*(d/(d+10))-0.0465*h+1.1060*log(h)-5.8926);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_pine_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(11.0481*(d/(d+15))-3.9657);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_little_roots_pine_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(8.8795*(d/(d+10))-3.8375);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_big_roots_pine_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(13.2902*(d/(d+9))-6.3413)+exp(8.8795*(d/(d+10))-3.8375);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_spruce_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(7.2309*(d/(d+14))+0.0355*h+0.703*log(h)-2.3032);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_bark_of_stem_spruce_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(8.3089*(d/(d+15))+0.0147*h+0.2295*log(h)-3.402);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_with_needles_spruce_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(10.9708*(d/(d+13))-0.0124*h-0.4923*log(h)-1.2063);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_dead_branches_spruce_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(3.6518*(d/(d+18))+0.0493*h+1.0129*log(h)-4.6351);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_spruce_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(10.6686*(d/(d+17))-3.3645);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_little_roots_spruce_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(7.6283*(d/(d+12))-2.5706);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_big_roots_spruce_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(13.3703*(d/(d+8))-6.3851)+exp(7.6283*(d/(d+12))-2.5706);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_birch_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(8.1184*(d/(d+11))+0.9783*log(h)-3.3045);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_bark_of_stem_birch_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(8.3019*(d/(d+14))+0.7433*log(h)-4.0778);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_without_leaves_birch_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(8.3019*(d/(d+14))+0.7433*log(h)-4.0778);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_foliage_birch_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(12.1095*(d/(d+7))+0.0413*h-1.565*log(h)-3.4781);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_dead_branches_birch_Marklund (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(11.2872*(d/(d+30))-0.3081*h+2.6821*log(h)-6.6237);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_birch_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(11.0481*(d/(d+15))-3.9657);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_little_roots_birch_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(8.8795*(d/(d+10))-3.8375);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_big_roots_birch_Marklund (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;



	*nres = 1;

	double res = exp(13.2902*(d/(d+9))-6.3413)+exp(8.8795*(d/(d+10))-3.8375);

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_and_roots_pine_Petersson_Stohl (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//d should be in mm
	d=d*10;

	*nres = 1;

	double res = (exp(11.06537*(d/(d+113))+3.44275))/1000;

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_and_roots_spruce_Petersson_Stohl (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//d should be in mm
	d=d*10;

	*nres = 1;

	double res = (exp(10.44035*(d/(d+138))+4.58761))/1000;

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stump_and_roots_birch_Petersson_Stohl (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;


	//d should be in mm
	d=d*10;

	*nres = 1;

	double res = (exp(10.01111*(d/(d+225))+6.1708))/1000;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_pine_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-3.778+8.294*(d_s/(d_s+14))+4.949*(h/(h+12))+(0.002+0.008/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_pine_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-3.756+8.616*(d_s/(d_s+12))+0.277*log(h)+(0.013+0.054/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_pine_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-6.024+15.289*(d_s/(d_s+12))-3.202*(h/(h+12))+(0.033+0.096/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_needles_pine_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-5.007+15.066*(d_s/(d_s+6))-5.896*(h/(h+1))+(0.097+0.123/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_pine_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-5.334+10.789*(d_s/(d_s+16)))*1.242;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_pine_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.215+9.764*(d_s/(d_s+12))+2.889*(h/(h+20))+(0.001+0.013/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_pine_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-6.739+12.658*(d_s/(d_s+12))+(0.009+0.044/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_pine_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-9.601+15.931*(d_s/(d_s+8))+(0.000+0.065/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-3.655+7.942*(d_s/(d_s+14))+0.907*log(h)+0.018*h+(0.006+0.008/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-4.349+9.879*(d_s/(d_s+18))+0.274*log(h)+(0.016+0.036/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.914+15.220*(d_s/(d_s+13))-4.350*(h/(h+5))+(0.022+0.089/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_needles_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-2.394+12.752*(d_s/(d_s+10))-4.470*(h/(h+1))+(0.103+0.107/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-5.467+6.252*(d_s/(d_s+18))+1.068*log(h))*1.181;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_spruce_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-1.729+9.697*(d_s/(d_s+20))+0.398*log(h)+(0.004+0.015/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_spruce_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.962+11.725*(d_s/(d_s+26))+(0.065+0.058/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_spruce_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-2.295+10.649*(d_s/(d_s+24))+(0.105+0.114/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_birch_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-5.001+9.284*(d_s/(d_s+12))+1.143*log(h)+(0.003+0.005/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_birch_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-5.449+9.967*(d_s/(d_s+12))+2.894*(h/(h+20))+(0.011+0.044/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_birch_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-4.279+14.731*(d_s/(d_s+16))-3.139*(h/(h+10))+(0.035+0.071/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_foliage_birch_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-29.566+33.372*(d_s/(d_s+2))+(0.000+0.077/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_birch_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-7.742+11.362*(d_s/(d_s+16)))*2.245;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_birch_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.662+10.329*(d_s/(d_s+12))+3.411*(h/(h+22))+(0.001+0.007/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_birch_Repola_Ojansuu (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.677+11.537*(d_s/(d_s+26))+(0.021+0.046/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_birch_Repola_Ojansuu (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-3.183+7.204*(d_s/(d_s+22))+0.892*log(h)+(0.047+0.027/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_wood_without_bark_pine_Repola_Ojansuu (double d, double a, double TS,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = 373.61-98.272*d/a+0.066*TS;
	
	//Fix if not realistic value
	if (res<300)
	{
	        res = 300;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_pine_Repola_Ojansuu (double d, double a, double TS,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = 378.39-78.829*d/a+0.039*TS;
	
	//Fix if not realistic value
	if (res<300)
	{
	        res = 300;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_wood_without_bark_spruce_Repola_Ojansuu (double d, double a,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = 447.77-0.659*d_s-101.84*d/a;
	
	//Fix if not realistic value
	if (res<300)
	{
	        res = 300;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_spruce_Repola_Ojansuu (double d, double a,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = 442.03-0.904*d_s-82.695*d/a;
	
	//Fix if not realistic value
	if (res<300)
	{
	        res = 300;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_wood_without_bark_birch_Repola_Ojansuu (double d, double a,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (d_s<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "d_s<=0(d_s=",d_s);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = 396.74+37.234*log(d_s)-67.086*d/a;
	
	//Fix if not realistic value
	if (res<400)
	{
	        res = 400;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Density_stem_birch_Repola_Ojansuu (double d, double a,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (a<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "a<=0(a=",a);
	}
	if (d_s<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "d_s<=0(d_s=",d_s);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = 431.43+28.054*log(d_s)-52.203*d/a;

        //Fix if not realistic value
	if (res<400)
	{
	        res = 400;
	}

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_pine_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-3.721+8.103*(d_s/(d_s+14))+5.066*(h/(h+12))+(0.002+0.009/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_pine_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-4.548+7.997*(d_s/(d_s+12))+0.357*log(h)+(0.015+0.061/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_pine_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-6.162+15.075*(d_s/(d_s+12))-2.618*(h/(h+12))+(0.041+0.089/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_needles_pine_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-6.303+14.472*(d_s/(d_s+6))-3.976*(h/(h+1))+(0.109+0.118/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_pine_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;

	*nres = 1;

	double res = exp(-5.201+10.574*(d_s/(d_s+16))+(0.253+0.362/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_pine_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.198+9.547*(d_s/(d_s+12))+3.241*(h/(h+20))+(0.009+0.01/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_pine_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-6.753+12.681*(d_s/(d_s+12))+(0.01+0.044/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_pine_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-5.55+13.408*(d_s/(d_s+15))+(0.000+0.079/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-3.555+8.042*(d_s/(d_s+14))+0.869*log(h)+0.015*h+(0.009+0.009/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-4.548+9.448*(d_s/(d_s+18))+0.436*log(h)+(0.023+0.041/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-4.214+14.508*(d_s/(d_s+13))-3.277*(h/(h+5))+(0.039+0.081/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_needles_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-2.994+12.251*(d_s/(d_s+10))-3.215*(h/(h+1))+(0.107+0.089/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-4.85+7.702*(d_s/(d_s+18))+0.513*log(h)+(0.367+0.352/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_spruce_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;
	
	double res = exp(-1.808+9.482*(d_s/(d_s+20))+0.469*log(h)+(0.006+0.013/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_spruce_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.964+11.73*(d_s/(d_s+26))+(0.065+0.058/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_spruce_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-2.294+10.646*(d_s/(d_s+24))+(0.105+0.114/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_wood_birch_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-4.879+9.651*(d_s/(d_s+12))+1.012*log(h)+(0.003+0.005/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_stem_bark_birch_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-5.401+10.061*(d_s/(d_s+12))+2.657*(h/(h+20))+(0.01+0.044/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_living_branches_birch_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-4.152+15.874*(d_s/(d_s+16))-4.407*(h/(h+10))+(0.027+0.077/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_foliage_birch_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-29.566+33.372*(d_s/(d_s+2))+(0.000+0.077/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_dead_branches_birch_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-8.335+12.402*(d_s/(d_s+16))+(1.115+2.679/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_aboveground_total_birch_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.654+10.582*(d_s/(d_s+12))+3.018*(h/(h+22))+(0.001+0.007/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_birch_Repola (double d,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	*nres = 1;

	double res = exp(-3.574+11.304*(d_s/(d_s+26))+(0.022+0.045/2));

	*modelresult = res * rectFactor;
	return ret;

}


int Biomass_roots_birch_Repola (double d, double h,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double d_s = 2+1.25*d;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (h<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "h<=0(h=",h);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}

	*nres = 1;

	double res = exp(-3.223+6.497*(d_s/(d_s+22))+1.033*log(h)+(0.048+0.027/2));

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stump_bark_JKK (double BM_stem, double BM_stem_bark, double BM_stump,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;
	
	//Check for fatal errors
	char errorStr[200] = "";
	if (BM_stem<=0)
	{
		ret = 0;
		constructErrorMessage (errorStr, "BM_stem<=0(BM_stem=",BM_stem);
	}
	if (ret == 0) {
		strcat(errors, errorStr);
		return 0;
	}


	double proportion = BM_stem_bark/BM_stem;
	
	*nres = 1;

	double res = BM_stump * proportion;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_tree_JKK (double d, double h, double a, double SP, double TS,
						int *nres, struct Biomass_tree *biomass, char *errors,
						int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double BM_branches, BM_foliage;
    double *density = (double *) malloc(1*sizeof(double));
    double *BM_living_branches = (double *) malloc(1*sizeof(double));
    double *BM_needles = (double *) malloc(1*sizeof(double));
    double *BM_dead_branches = (double *) malloc(1*sizeof(double));
    double *BM_leaves = (double *) malloc(1*sizeof(double));
    double *BM_stump = (double *) malloc(1*sizeof(double));
    double *BM_roots = (double *) malloc(1*sizeof(double));
    
    //To avoid problems in biomass calculations when age at breast height is calculated 
    //using models. In that case d is greater than zero and still t_href is greater than age -> a is assign to zero
    //Assign to 1 if less than 1
    if (a<1)
       a=1;
    //Assing a using h value
    if (h>=1.8 && h < 2.1 && a<2)
    	a=2;
    else if (h>=2.1 && h < 2.4 && a<3)
    	a=3;
    else if (h>=2.4 && h < 2.7 && a<4)
    	a=4;
    else if (h>=2.7 && h < 3.0 && a<5)
    	a=5;
    else if (h>=3.0 && h < 3.5 && a<6)
    	a=6;
    else if (h>=3.5 && h < 4.0 && a<7)
    	a=7;
    else if (h>=4.0 && a<8)
    	a=8;
            
	//Calculate biomass of tree
	//Calculate first wood density
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Density_stem_pine_Repola_Ojansuu(d, a, TS, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Density_stem_spruce_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
	}
	//Birches and other deciduous species
	else
	{
		ret = Density_stem_birch_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
	}

	if (ret == 0)
	{
        free(density);
		return ret;
    }
	
	//Calculate biomass of branches
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_living_branches_pine_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_pine_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_pine_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_living_branches_spruce_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_spruce_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_spruce_Repola(d, h, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_living_branches_birch_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_foliage_birch_Repola(d, nres, BM_leaves, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_leaves);
		   return ret;
        }
        ret = Biomass_dead_branches_birch_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
	}
    if (SP==1||SP==2||SP==8)
    {
        BM_branches = *BM_living_branches + *BM_dead_branches;
        BM_foliage = *BM_needles;
    }    
    else
    {
        BM_branches = *BM_living_branches + *BM_dead_branches;
        BM_foliage = *BM_leaves;
    }
	
    //Calculate biomass of stump and roots
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_stump_pine_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
       ret = Biomass_roots_pine_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
          	free(BM_roots);
		return ret;
        	}
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_stump_spruce_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stump);
		   return ret;
        }
       ret = Biomass_roots_spruce_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_roots);
		   return ret;
        }
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_stump_birch_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stump);
		   return ret;
        }
        ret = Biomass_roots_birch_Repola(d, h, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_roots);
		   return ret;
        }
	}
    
		   
	*nres = 1;
	
	biomass[0].density=*density;
	biomass[0].BM_stump=*BM_stump;
	biomass[0].BM_roots=*BM_roots;
	biomass[0].BM_branches=BM_branches;
	biomass[0].BM_foliage=BM_foliage;
	
	free(density);
	free(BM_living_branches);
    free(BM_needles);
	free(BM_dead_branches);
	free(BM_leaves);
    free(BM_stump);
    free(BM_roots);
	
	return ret;

}

int Biomass_tree_Yasso_JKK (double d, double h, double a, double SP, double TS,
						int *nres, struct Biomass_tree_Yasso *biomass, char *errors,
						int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double BM_branches, BM_foliage;
    double *density = (double *) malloc(1*sizeof(double));
    double *BM_living_branches = (double *) malloc(1*sizeof(double));
    double *BM_needles = (double *) malloc(1*sizeof(double));
    double *BM_dead_branches = (double *) malloc(1*sizeof(double));
    double *BM_leaves = (double *) malloc(1*sizeof(double));
    double *BM_stump = (double *) malloc(1*sizeof(double));
    double *BM_roots = (double *) malloc(1*sizeof(double));
    double *BM_stem_bark = (double *) malloc(1*sizeof(double));
    
    //To avoid problems in biomass calculations when age at breast height is calculated 
    //using models. In that case d is greater than zero and still t_href is greater than age -> a is assign to zero 
    if (a==0)
       a=1;
    //Assing a using h value
    if (h>=1.8 && h < 2.1 && a<2)
    	a=2;
    else if (h>=2.1 && h < 2.4 && a<3)
    	a=3;
    else if (h>=2.4 && h < 2.7 && a<4)
    	a=4;
    else if (h>=2.7 && h < 3.0 && a<5)
    	a=5;
    else if (h>=3.0 && h < 3.5 && a<6)
    	a=6;
    else if (h>=3.5 && h < 4.0 && a<7)
    	a=7;
    else if (h>=4.0 && a<8)
    	a=8;
            
	//Calculate biomass of tree
	//Calculate first wood density
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Density_stem_pine_Repola_Ojansuu(d, a, TS, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
			return ret;
	    	}
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Density_stem_spruce_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
	    		return ret;
	    	}
	}
	//Birches and other deciduous species
	else
	{
		ret = Density_stem_birch_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
			return ret;
	    	}
	}
	
	//Calculate biomass of branches and stem bark
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_living_branches_pine_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_pine_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_pine_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_pine_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_living_branches_spruce_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_spruce_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_spruce_Repola(d, h, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_spruce_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_living_branches_birch_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_foliage_birch_Repola(d, nres, BM_leaves, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_leaves);
		   return ret;
        }
        ret = Biomass_dead_branches_birch_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_birch_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
        if (SP==1||SP==2||SP==8)
        {
            BM_branches = *BM_living_branches + *BM_dead_branches;
            BM_foliage = *BM_needles;
        }    
        else
        {
            BM_branches = *BM_living_branches + *BM_dead_branches;
            BM_foliage = *BM_leaves;
        }
	
        //Calculate biomass of stump and roots
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_stump_pine_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
       ret = Biomass_roots_pine_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
          	free(BM_roots);
		return ret;
        	}
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_stump_spruce_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
       ret = Biomass_roots_spruce_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_roots);
		return ret;
        	}
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_stump_birch_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
        ret = Biomass_roots_birch_Repola(d, h, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_roots);
		return ret;
        	}
	}
    
    	//fine roots based on Carbon sink of Finland's forests,Liski et al 2006
    	//Scots pine and other conifers
    	double BM_fine_roots = 0;
	if (SP==1||SP==8)
	{
		BM_fine_roots = 0.5 * BM_foliage;
	}
	//Norway spruce
	else if (SP==2)
	{
		BM_fine_roots = 0.3 * BM_foliage;
	}
	//Birches and other deciduous species
	else
	{
		BM_fine_roots = 0.5 * BM_foliage;
	}
		   
	*nres = 1;
	
	biomass[0].density=*density;
	biomass[0].BM_stump=*BM_stump;
	biomass[0].BM_roots=*BM_roots;
	biomass[0].BM_branches=BM_branches;
	biomass[0].BM_foliage=BM_foliage;
	biomass[0].BM_fine_roots=BM_fine_roots;
	biomass[0].BM_stem_bark=*BM_stem_bark;	
	
	free(density);
	free(BM_living_branches);
    	free(BM_needles);
	free(BM_dead_branches);
	free(BM_leaves);
    	free(BM_stump);
    	free(BM_roots);
    	free(BM_stem_bark);
	
	return ret;

}

int Biomass_stratum_Yasso_JKK (double d, double h, double a, double SP, double TS,
						int *nres, struct Biomass_tree_Yasso *biomass, char *errors,
						int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double BM_branches, BM_foliage;
    double *density = (double *) malloc(1*sizeof(double));
    double *BM_living_branches = (double *) malloc(1*sizeof(double));
    double *BM_needles = (double *) malloc(1*sizeof(double));
    double *BM_dead_branches = (double *) malloc(1*sizeof(double));
    double *BM_leaves = (double *) malloc(1*sizeof(double));
    double *BM_stump = (double *) malloc(1*sizeof(double));
    double *BM_roots = (double *) malloc(1*sizeof(double));
    double *BM_stem_bark = (double *) malloc(1*sizeof(double));
    
    //To avoid problems in biomass calculations when age at breast height is calculated 
    //using models. In that case d is greater than zero and still t_href is greater than age -> a is assign to zero 
    if (a==0)
       a=1;
            
	//Calculate biomass of tree
	//Calculate first wood density
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Density_stem_pine_Repola_Ojansuu(d, a, TS, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
			return ret;
	    	}
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Density_stem_spruce_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
	    		return ret;
	    	}
	}
	//Birches and other deciduous species
	else
	{
		ret = Density_stem_birch_Repola_Ojansuu(d, a, nres, density, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
	        	free(density);
			return ret;
	    	}
	}
	
	//Calculate biomass of branches and stem bark
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_living_branches_pine_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_pine_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_pine_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_pine_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_living_branches_spruce_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_needles_spruce_Repola(d, h, nres, BM_needles, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_needles);
		   return ret;
        }
        ret = Biomass_dead_branches_spruce_Repola(d, h, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_spruce_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_living_branches_birch_Repola(d, h, nres, BM_living_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_living_branches);
		   return ret;
        }
        ret = Biomass_foliage_birch_Repola(d, nres, BM_leaves, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_leaves);
		   return ret;
        }
        ret = Biomass_dead_branches_birch_Repola(d, nres, BM_dead_branches, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_dead_branches);
		   return ret;
        }
        ret = Biomass_stem_bark_birch_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
        if (SP==1||SP==2||SP==8)
        {
            BM_branches = *BM_living_branches + *BM_dead_branches;
            BM_foliage = *BM_needles;
        }    
        else
        {
            BM_branches = *BM_living_branches + *BM_dead_branches;
            BM_foliage = *BM_leaves;
        }
	
        //Calculate biomass of stump and roots
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
		ret = Biomass_stump_pine_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
       ret = Biomass_roots_pine_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
          	free(BM_roots);
		return ret;
        	}
	}
	//Norway spruce
	else if (SP==2)
	{
		ret = Biomass_stump_spruce_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
       ret = Biomass_roots_spruce_Repola(d, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_roots);
		return ret;
        	}
	}
	//Birches and other deciduous species
	else
	{
		ret = Biomass_stump_birch_Repola(d, nres, BM_stump, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_stump);
		return ret;
        	}
        ret = Biomass_roots_birch_Repola(d, h, nres, BM_roots, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           	free(BM_roots);
		return ret;
        	}
	}
    
    	//fine roots based on Carbon sink of Finland's forests,Liski et al 2006
    	//Scots pine and other conifers
    	double BM_fine_roots = 0;
	if (SP==1||SP==8)
	{
		BM_fine_roots = 0.5 * BM_foliage;
	}
	//Norway spruce
	else if (SP==2)
	{
		BM_fine_roots = 0.3 * BM_foliage;
	}
	//Birches and other deciduous species
	else
	{
		BM_fine_roots = 0.5 * BM_foliage;
	}
		   
	*nres = 1;
	
	biomass[0].density=*density;
	biomass[0].BM_stump=*BM_stump;
	biomass[0].BM_roots=*BM_roots;
	biomass[0].BM_branches=BM_branches;
	biomass[0].BM_foliage=BM_foliage;
	biomass[0].BM_fine_roots=BM_fine_roots;
	biomass[0].BM_stem_bark=*BM_stem_bark;	
	
	free(density);
	free(BM_living_branches);
    	free(BM_needles);
	free(BM_dead_branches);
	free(BM_leaves);
    	free(BM_stump);
    	free(BM_roots);
    	free(BM_stem_bark);
	
	return ret;

}

int Biomass_stump_bark_stratum_JKK (double BM_stem, double BM_stem_bark, double BM_stump,
					   int *nres, double *modelresult, char *errors,
					   int errorCheckMode, double allowedRiskLevel, double rectFactor) {

	int ret = 1;

	double proportion = BM_stem_bark/BM_stem;
	
	*nres = 1;

	double res = BM_stump * proportion;

	*modelresult = res * rectFactor;
	return ret;

}

int Biomass_stem_bark_JKK (double d, double h, double SP,
                        int *nres, double *modelresult, char *errors,
			int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double *BM_stem_bark = (double *) malloc(1*sizeof(double));
    
	//Calculate biomass of tree
	
	//Calculate biomass of stem bark
	//Scots pine and other conifers
	if (SP==1||SP==8)
	{
        ret = Biomass_stem_bark_pine_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Norway spruce
	else if (SP==2)
	{
        ret = Biomass_stem_bark_spruce_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
	//Birches and other deciduous species
	else
        {
        ret = Biomass_stem_bark_birch_Repola(d, h, nres, BM_stem_bark, errors, errorCheckMode, allowedRiskLevel, 1);
		if (ret == 0)
		{
           free(BM_stem_bark);
		   return ret;
        }
	}
		   
	*nres = 1;
	
	*modelresult=*BM_stem_bark;	
	
    	free(BM_stem_bark);
	
	return ret;

}