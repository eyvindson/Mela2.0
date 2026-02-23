// Copyright (c) 2007 Simosol Oy. Distributed under the GNU General Public License 2.0.

//////////////////////////////////////////////////////////////////////////////
//
//  NaturalremovalmodelLibrary.cpp
//
//    Natural removal model library - Source file
//
//    Here are the conventional calls of the functions

#include <stdio.h>
#include "NaturalremovalmodelLibrary.h"
#include "SimoUtils.h"

#include <math.h>
#include <stdlib.h>
#include <string.h>


int Mimimum_growing_space_pine_Hynynenym (double d_s, int *nres, double *modelresult, char *errors,
                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res =pow(exp(13.9189),-1)*pow(d_s,2.0551);

    //Relative density factor can be calculated by adding ga of every tree in a stand together!

    *modelresult = res * rectFactor;
    return ret;

}


int Mimimum_growing_space_spruce_Hynynenym (double d_s,    int *nres, double *modelresult, char *errors,
                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res =pow(exp(12.6161),-1)*pow(d_s,1.5538);

    //Relative density factor can be calculated by adding ga of every tree in a stand together!

    *modelresult = res * rectFactor;
    return ret;

}


int Mimimum_growing_space_white_birch_Hynynenym (double d_s, int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res =pow(exp(14.1979),-1)*pow(d_s,2.2178);

    //Relative density factor can be calculated by adding ga of every tree in a stand together!

    *modelresult = res * rectFactor;
    return ret;

}


int Mimimum_growing_space_pubescent_birch_Hynynenym (double d_s, int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res =pow(exp(13.1659),-1)*pow(d_s,1.8545);

    //Relative density factor can be calculated by adding ga of every tree in a stand together!

    *modelresult = res * rectFactor;
    return ret;

}



int Probability_a_tree_to_die_due_to_competition_pine_Hynynenym (double d, double BA, double BA_L, double SC,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    double a0, a1, a2, a3;
    int iSC = (int) SC;
    switch (iSC)
    {
        case 1:
            a0 = 3.133;
            a1 = 0.2087;
            a2 = -0.0189;
            a3 = -0.0847;
            break;
        case 2:
            a0 = 3.133;
            a1 = 0.2087;
            a2 = -0.0189;
            a3 = -0.0847;
            break;
        case 3:
            a0 = 2.2388;
            a1 = 0.5089;
            a2 = -0.0303;
            a3 = -0.0794;
            break;
        case 4:
            a0 = 3.9458;
            a1 = 0.1445;
            a2 = -0.0444;
            a3 = -0.069;
            break;
        case 5:
            a0 = 2.9774;
            a1 = 0.3274;
            a2 = 0.0591;
            a3 = -0.1875;
            break;
        case 6:
            a0 = 3.476;
            a1 = 0.0071;
            a2 = 0.1692;
            a3 = -0.1867;
            break;
        case 7:
            a0 = 3.476;
            a1 = 0.0071;
            a2 = 0.1692;
            a3 = -0.1867;
            break;
        case 8:
            a0 = 3.476;
            a1 = 0.0071;
            a2 = 0.1692;
            a3 = -0.1867;
            break;
    };

    //Check for fatal errors
    char errorStr[200] = "";
    if (1+exp(a0+a1*d+a2*BA+a3*BA_L)==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1+exp(a0+a1*d+a2*BA+a3*BA_L)==0(BA=",BA, ",BA_L=",BA_L);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =1/(1+exp(a0+a1*d+a2*BA+a3*BA_L));
    *modelresult = res * rectFactor;
    return ret;

}


int Probability_a_tree_to_die_due_to_competition_spruce_Hynynenym (double d, double BA, double BA_L, double SC,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    double  a0, a1, a2, a3;
    int iSC = (int) SC;
    switch (iSC)
    {
        case 1:
            a0 = 4.3958;
            a1 = 0.2042;
            a2 = 0.0956;
            a3 = -0.199;
            break;
        case 2:
            a0 = 4.3958;
            a1 = 0.2042;
            a2 = 0.0956;
            a3 = -0.199;
            break;
        case 3:
            a0 = 4.3552;
            a1 = 0.094;
            a2 = 0.0867;
            a3 = -0.1637;
            break;
        case 4:
            a0 = 2.891;
            a1 = 0.1772;
            a2 = 0.809;
            a3 = -0.9307;
            break;
        case 5:
            a0 = 1.696;
            a1 = 0.092;
            a2 = -0.0154;
            a3 = 0.5883;
            break;
        case 6:
            a0 = 1.696;
            a1 = 0.092;
            a2 = -0.0154;
            a3 = 0.5883;
            break;
        case 7:
            a0 = 1.696;
            a1 = 0.092;
            a2 = -0.0154;
            a3 = 0.5883;
            break;
        case 8:
            a0 = 1.696;
            a1 = 0.092;
            a2 = -0.0154;
            a3 = 0.5883;
            break;
    };

    //Check for fatal errors
    char errorStr[200] = "";
    if (1+exp(a0+a1*d+a2*BA+a3*BA_L)==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1+exp(a0+a1*d+a2*BA+a3*BA_L)==0(BA=",BA, ",BA_L=",BA_L);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =1/(1+exp(a0+a1*d+a2*BA+a3*BA_L));
    *modelresult = res * rectFactor;
    return ret;

}


int Probability_a_tree_to_die_due_to_competition_deciduous_Hynynenym (double d, double RDF_L,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    double d_s;

    // Diameter at breast height is probably not measured. It can be estimated using Laasasenaho's model!
    d_s=2+1.25*d;  // Laasasenaho's model for diameter at stump height!

    //Check for fatal errors
    char errorStr[200] = "";
    if (1+exp(3.014+0.1015*d_s-9.313*RDF_L+0.4073*d_s*RDF_L)==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1+exp(3.014+0.1015*d_s-9.313*RDF_L+0.4073*d_s*RDF_L)==0(d_s=",d_s, ",RDF_L=",RDF_L);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =1/(1+exp(3.014+0.1015*d_s-9.313*RDF_L+0.4073*d_s*RDF_L));
    *modelresult = res * rectFactor;
    return ret;

}


int Probability_a_tree_to_die_due_to_aging_Hynynenym (double age, double sp, double TS,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    double age_max, age_max1200, age_max800, c1;
    int isp = (int) sp;
    switch (isp)
    {
        case 1:
            age_max1200 = 450;
            age_max800 = 750;
            break;
        case 2:
            age_max1200 = 350;
            age_max800 = 450;
            break;
        case 3:
            age_max1200 = 200;
            age_max800 = 300;
            break;
        case 4:
            age_max1200 = 150;
            age_max800 = 225;
            break;
        case 5:
            age_max1200 = 180;
            age_max800 = 270;
            break;
        case 6:
            age_max1200 = 100;
            age_max800 = 150;
            break;
        case 7:
            age_max1200 = 150;
            age_max800 = 225;
            break;
        case 8:
            age_max1200 = 350;
            age_max800 = 400;
            break;
        case 9:
            age_max1200 = 80;
            age_max800 = 120;
            break;
    };

    if(TS>1200) {
        age_max=age_max1200;
    }
    else
    {
        if(TS<800) {
            age_max=age_max800;
        } else {
            c1=age_max800-age_max1200;
            age_max=age_max800-c1/400*(TS-800);
        }
    }


    //Check for fatal errors
    char errorStr[200] = "";
    if (0.82*age_max==0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "0.82*age_max==0(age_max=",age_max);
    }
    if (1+exp(-10+10*((age+5)/(0.82*age_max)))==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1+exp(-10+10*((age+5)/(0.82*age_max)))==0(age=",age, ",age_max=",age_max);
    }
    if (1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max))))==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max))))==0(age=",age, ",age_max=",age_max);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =((exp(-10+10*((age+5)/(0.82*age_max)))/(1+exp(-10+10*((age+5)/(0.82*age_max)))))-
        exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max)))))/
        (1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max)))));
    *modelresult = res * rectFactor;
    return ret;

}

int Probability_a_tree_to_die_due_to_aging_urban_area_forest_Hynynenym (double age, double sp, double TS,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    double age_max, age_max1200, age_max800, c1;
    int isp = (int) sp;
    switch (isp)
    {
        case 1:
            age_max1200 = 200;
            age_max800 = 250;
            break;
        case 2:
            age_max1200 = 180;
            age_max800 = 220;
            break;
        case 3:
            age_max1200 = 140;
            age_max800 = 160;
            break;
        case 4:
            age_max1200 = 110;
            age_max800 = 130;
            break;
        case 5:
            age_max1200 = 110;
            age_max800 = 130;
            break;
        case 6:
            age_max1200 = 100;
            age_max800 = 120;
            break;
        case 7:
            age_max1200 = 110;
            age_max800 = 130;
            break;
        case 8:
            age_max1200 = 180;
            age_max800 = 220;
            break;
        case 9:
            age_max1200 = 110;
            age_max800 = 130;
            break;
    };

    if(TS>1200) {
        age_max=age_max1200;
    }
    else
    {
        if(TS<800) {
            age_max=age_max800;
        } else {
            c1=age_max800-age_max1200;
            age_max=age_max800-c1/400*(TS-800);
        }
    }


    //Check for fatal errors
    char errorStr[200] = "";
    if (0.82*age_max==0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "0.82*age_max==0(age_max=",age_max);
    }
    if (1+exp(-10+10*((age+5)/(0.82*age_max)))==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1+exp(-10+10*((age+5)/(0.82*age_max)))==0(age=",age, ",age_max=",age_max);
    }
    if (1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max))))==0)
    {
        ret = 0;
        constructErrorMessage2val (errorStr, "1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max))))==0(age=",age, ",age_max=",age_max);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =((exp(-10+10*((age+5)/(0.82*age_max)))/(1+exp(-10+10*((age+5)/(0.82*age_max)))))-
        exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max)))))/
        (1-exp(-10+10*((age)/(0.82*age_max)))/(1+exp(-10+10*((age)/(0.82*age_max)))));
    *modelresult = res * rectFactor;
    return ret;

}

int Probability_a_tree_to_die_Hynynenym (double p_comp5, double p_old5,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res = 1-(1-p_comp5)*(1-p_old5);
    *modelresult = res * rectFactor;
    return ret;

}

int Probability_a_tree_to_live_JKK (double p_tot5,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    *nres = 1;
    double res = 1-p_tot5;
    *modelresult = res * rectFactor;
    return ret;

}

int Maximum_allowable_stem_number_peatland_pine_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(13.9189-2.0551*log(D_gs)+(pow(0.202,2)+pow(0.078,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_peatland_spruce_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(12.6161-1.5538*log(D_gs)+(pow(0.087,2)+pow(0.056,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_white_birch_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(14.1979-2.2178*log(D_gs)+(pow(0.16,2)+pow(0.106,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_pubescent_birch_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(13.1659-1.8545*log(D_gs)+(pow(0.156,2)+pow(0.04,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_pine_Hynynenym (double D_gs, double SI_50,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (SI_50<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "SI_50<=0(SI_50=",SI_50);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(12.3758+0.571*log(SI_50)-2.067*log(D_gs)+(pow(0.158,2)+pow(0.078,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_spruce_Hynynenym (double D_gs, double SI_50,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (SI_50<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "SI_50<=0(SI_50=",SI_50);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =exp(11.8686+0.2919*log(SI_50)-1.5928*log(D_gs)+(pow(0.76,2)+pow(0.056,2))/2);
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_young_stand_pine_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =21003.09-1177.36*D_gs+(pow(0.202,2)+pow(0.078,2))/2;
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_young_stand_spruce_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =16284.79-825.68*D_gs+(pow(0.087,2)+pow(0.056,2))/2;
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_young_stand_white_birch_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =19418.66-1115.32*D_gs+(pow(0.16,2)+pow(0.106,2))/2;
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_young_stand_pubescent_birch_Hynynenym (double D_gs,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    //Check for fatal errors
    char errorStr[200] = "";
    if (D_gs<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "D_gs<=0(D_gs=",D_gs);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    *nres = 1;
    double res =15055.60-815.11*D_gs+(pow(0.156,2)+pow(0.04,2))/2;
    *modelresult = res * rectFactor;
    return ret;

}


int Maximum_allowable_stem_number_before_growing_Hynynenym (double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb,
                                    double N_max_oc, double N_max_od, double N_max_Sp_upper, double N_max_Ns_upper, double N_max_sb_upper, double N_max_pb_upper,
                                    double N_max_oc_upper, double N_max_od_upper, double N_max_Sp_under, double N_max_Ns_under, double N_max_sb_under, double N_max_pb_under,
                                    double N_max_oc_under, double N_max_od_under, int *nres, struct N_maxbg *n_maxbg, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;


    n_maxbg[0].N_maxbg_Sp = N_max_Sp;
    n_maxbg[0].N_maxbg_Ns = N_max_Ns;
    n_maxbg[0].N_maxbg_sb = N_max_sb;
    n_maxbg[0].N_maxbg_pb = N_max_pb;
    n_maxbg[0].N_maxbg_oc = N_max_oc;
    n_maxbg[0].N_maxbg_od = N_max_od;
    n_maxbg[0].N_maxbg_Sp_upper = N_max_Sp_upper;
    n_maxbg[0].N_maxbg_Ns_upper = N_max_Ns_upper;
    n_maxbg[0].N_maxbg_sb_upper = N_max_sb_upper;
    n_maxbg[0].N_maxbg_pb_upper = N_max_pb_upper;
    n_maxbg[0].N_maxbg_oc_upper = N_max_oc_upper;
    n_maxbg[0].N_maxbg_od_upper = N_max_od_upper;
    n_maxbg[0].N_maxbg_Sp_under = N_max_Sp_under;
    n_maxbg[0].N_maxbg_Ns_under = N_max_Ns_under;
    n_maxbg[0].N_maxbg_sb_under = N_max_sb_under;
    n_maxbg[0].N_maxbg_pb_under = N_max_pb_under;
    n_maxbg[0].N_maxbg_oc_under = N_max_oc_under;
    n_maxbg[0].N_maxbg_od_under = N_max_od_under;

    *nres = 1;
    return ret;

}


int Maximum_allowable_reduction_in_stem_number_Hynynenym (double SP, double N_max_Sp, double N_max_Ns, double N_max_sb,
                                    double N_max_pb, double N_max_oc, double N_max_od, double N_maxbg_Sp, double N_maxbg_Ns,
                                    double N_maxbg_sb, double N_maxbg_pb, double N_maxbg_oc, double N_maxbg_od,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;

    double N_max, N_maxbg;

    if(SP==1)
    {
        N_max = N_max_Sp;
        N_maxbg = N_maxbg_Sp;
    }
    else if(SP==2)
    {
        N_max=N_max_Ns;
        N_maxbg = N_maxbg_Ns;
    }
    else if(SP==3)
    {
        N_max=N_max_sb;
        N_maxbg = N_maxbg_sb;
    }
    else if(SP==4)
    {
        N_max=N_max_pb;
        N_maxbg = N_maxbg_pb;
    }
    else if (SP==8)
    {
        N_max=N_max_oc;
        N_maxbg = N_maxbg_oc;
    }
    //(SP==5||SP==6||SP==7||SP==9)
    else
    {
        N_max=N_max_od;
        N_maxbg = N_maxbg_od;
    }

    //OBS!! maximum reduction (1,5*reduction of mean diameter) is initially defined for 5 years period.
    //For simulation period of 1 year it should be then 1,085 (1,085^5=1,5)
    *nres = 1;
    double res;
    double result=(N_maxbg-N_max)*1.085;
    if (result<0.0001)
        res = 0;
    else
        res = result;

    *modelresult = res * rectFactor;
    return ret;

}


int Adjust_maximum_allowable_stem_number_pine_Hynynenym (double N, double Delta_Nmax, double SP, double N_Sp, double N_max_Sp,
                                    double N_oc, double N_max_oc,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;

    double reduction, N_x, N_max_x;

    if (SP==1)
    {
        N_x = N_Sp;
        N_max_x = N_max_Sp;
    }
    else if (SP==8)
    {
        N_x = N_oc;
        N_max_x = N_max_oc;
    }

    *nres = 1;

    double res;
    reduction=N_x-N_max_x;
    if(reduction>Delta_Nmax)
    {
        res =N*((N_x-Delta_Nmax)/N_x);
    }
    else
        res =N*(N_max_x/N_x);

    *modelresult = res * rectFactor;
    return ret;

}


int Adjust_maximum_allowable_stem_number_spruce_Hynynenym (double N, double Delta_Nmax, double N_Ns, double N_max_Ns,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;

    double reduction;

    *nres = 1;

    double res;
    reduction=N_Ns-N_max_Ns;
    if(reduction>Delta_Nmax)
    {
        res =N*((N_Ns-Delta_Nmax)/N_Ns);
    }
    else
        res =N*(N_max_Ns/N_Ns);

    *modelresult = res * rectFactor;
    return ret;

}


int Adjust_maximum_allowable_stem_number_white_birch_Hynynenym (double N, double Delta_Nmax, double N_sb, double N_max_sb,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;

    double reduction;

    *nres = 1;

    double res;
    reduction=N_sb-N_max_sb;
    if(reduction>Delta_Nmax)
    {
        res =N*((N_sb-Delta_Nmax)/N_sb);
    }
    else
        res =N*(N_max_sb/N_sb);

    *modelresult = res * rectFactor;
    return ret;

}


int Adjust_maximum_allowable_stem_number_pubescent_birch_Hynynenym (double SP, double N, double Delta_Nmax,
                                    double N_pb, double N_max_pb, double N_od, double N_max_od,
                                    int *nres, double *modelresult, char *errors,
                                    int errorCheckMode, double allowedRiskLevel, double rectFactor) {
    int ret = 1;

    double reduction, N_x, N_max_x;

    if (SP==4)
    {
        N_x = N_pb;
        N_max_x = N_max_pb;
    }
    else if (SP==5||SP==6||SP==7||SP==9)
    {
        N_x = N_od;
        N_max_x = N_max_od;
    }

    *nres = 1;

    double res;
    reduction=N_x-N_max_x;
    if(reduction>Delta_Nmax)
    {
        res =N*((N_x-Delta_Nmax)/N_x);
    }
    else
        res =N*(N_max_x/N_x);

    *modelresult = res * rectFactor;
    return ret;

}

int Scale_factor_N_over_5000 (double BA, double D_gM, double SP, double N_max_Sp, double N_max_Ns,
                        double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {

    int ret = 1;
    double BA_max, N_max;

    if(SP==1)
        N_max=N_max_Sp;
    else if(SP==2)
        N_max=N_max_Ns;
    else if(SP==3)
        N_max=N_max_sb;
    else if(SP==4)
        N_max=N_max_pb;
    else if(SP==8)
        N_max=N_max_oc;
    //(SP==5||SP==6||SP==7||SP==9)
    else
        N_max=N_max_od;


    //Check for fatal errors
    char errorStr[100] = "";
    if (BA == 0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "BA=0(BA=",BA);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    BA_max=N_max*PI*pow(D_gM/200,2);

    *nres = 1;

    *modelresult =BA_max/BA;
    return ret;

}


int Scale_factor_N_between_2000_and_5000 (double BA, double D_gM,  double N, double SP, double N_max_Sp,
                        double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {

    int ret = 1;
    double BA_max, weight, N_max;

    if(SP==1)
        N_max=N_max_Sp;
    else if(SP==2)
        N_max=N_max_Ns;
    else if(SP==3)
        N_max=N_max_sb;
    else if(SP==4)
        N_max=N_max_pb;
    else if(SP==8)
        N_max=N_max_oc;
    //(SP==5||SP==6||SP==7||SP==9)
    else
        N_max=N_max_od;


    //Check for fatal errors
    char errorStr[100] = "";
    if (BA == 0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "BA=0(BA=",BA);
    }
    if (N == 0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "N=0(N=",N);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    BA_max = N_max * PI * pow(D_gM / 200, 2);
    weight = 1 / 3 * (N / 1000) - 2 / 3;

    *nres = 1;

    *modelresult = weight * BA_max / BA + (1 - weight) * (N_max / N);
    return ret;

}


int Maximum_allowable_stem_number_in_mixed_stand_pine_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns,
                        double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb, double RDF_pb,
                        double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {

    int ret = 1;

   //Check for fatal errors
    char errorStr[100] = "";
    if (Upper_st==0&&RDF<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF<=0(RDF=",RDF);
    }
    if (Upper_st==1&&RDF_up<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF_up<=0(RDF_up=",RDF_up);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    if(Upper_st==1)
    {
        RDF=RDF_up;
        RDF_Sp=RDFSp_up;
        RDF_Ns=RDFNs_up;
        RDF_sb=RDFsb_up;
        RDF_pb=RDFpb_up;
    }

    *nres = 1;

    *modelresult =((RDF_Sp+RDF_sb+RDF_pb)/RDF)*N_max_Sp+(RDF_Ns/RDF)*N_max_Ns;
    return ret;

}


int Maximum_allowable_stem_number_in_mixed_stand_white_birch_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns,
                        double N_max_sb, double N_max_pb, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns,
                        double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {

    int ret = 1;

    //Check for fatal errors
    char errorStr[100] = "";
    if (Upper_st==0&&RDF<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF<=0(RDF=",RDF);
    }
    if (Upper_st==1&&RDF_up<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF_up<=0(RDF_up=",RDF_up);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    if(Upper_st==1)
    {
        RDF=RDF_up;
        RDF_Sp=RDFSp_up;
        RDF_Ns=RDFNs_up;
        RDF_sb=RDFsb_up;
        RDF_pb=RDFpb_up;
    }

    *nres = 1;

    *modelresult =(RDF_Sp/RDF)*N_max_Sp+(RDF_Ns/RDF)*N_max_Ns+(RDF_sb/RDF)*N_max_sb+(RDF_pb/RDF)*N_max_pb;
    return ret;

}


int Maximum_allowable_stem_number_in_mixed_stand_pubescent_birch_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns,
                        double N_max_pb, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb,
                        double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor) {

    int ret = 1;

    //Check for fatal errors
    char errorStr[100] = "";
    if (Upper_st==0&&RDF<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF<=0(RDF=",RDF);
    }
    if (Upper_st==1&&RDF_up<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "RDF_up<=0(RDF_up=",RDF_up);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    if(Upper_st==1)
    {
        RDF=RDF_up;
        RDF_Sp=RDFSp_up;
        RDF_Ns=RDFNs_up;
        RDF_sb=RDFsb_up;
        RDF_pb=RDFpb_up;
    }

    *nres = 1;

    *modelresult =(RDF_Sp/RDF)*N_max_Sp+(RDF_Ns/RDF)*N_max_Ns+((RDF_sb+RDF_pb)/RDF)*N_max_pb;
    return ret;

}

int Minimum_growing_space_JKK (double d_s, double SP,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    //Calculate minimum growing space
    //Scots pine and other conifers
    if (SP==1||SP==8)
    {
        ret = Mimimum_growing_space_pine_Hynynenym(d_s, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Norway spruce
    else if (SP==2)
    {
        ret = Mimimum_growing_space_spruce_Hynynenym(d_s, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Silver birch
    else if (SP==3)
    {
        ret = Mimimum_growing_space_white_birch_Hynynenym(d_s, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Other deciduous species
    else
    {
        ret = Mimimum_growing_space_pubescent_birch_Hynynenym(d_s, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }

    *nres = 1;
    return ret;

}

int Tree_survival_JKK (double d, double age, double SP, double BA, double BA_L,
                        double RDF_L, double SC, double TS,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double p_comp5, p_old5, p_tot5;
    //Calculate probability tree to die due to competition
    //Scots pine and other conifers
    if (SP==1||SP==8)
    {
        ret = Probability_a_tree_to_die_due_to_competition_pine_Hynynenym(d, BA, BA_L, SC, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Norway spruce
    else if (SP==2)
    {
        ret = Probability_a_tree_to_die_due_to_competition_spruce_Hynynenym(d, BA, BA_L, SC, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Birches and other deciduous species
    else
    {
        ret = Probability_a_tree_to_die_due_to_competition_deciduous_Hynynenym(d, RDF_L, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    p_comp5 = *modelresult;

    if (ret == 0)
        return ret;

    //Calculate probability tree to die due to aging
    ret = Probability_a_tree_to_die_due_to_aging_Hynynenym(age, SP, TS, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    p_old5 = *modelresult;

    if (ret == 0)
        return ret;

    //Calculate total probability tree to die
    ret = Probability_a_tree_to_die_Hynynenym(p_comp5, p_old5, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, rectFactor);
    p_tot5 = *modelresult;
    if (ret == 0)
        return ret;

    //Calculate tree's probability to survive
    ret = Probability_a_tree_to_live_JKK(p_tot5, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);

    *nres = 1;
    return ret;

}

int Tree_survival_urban_area_forest_JKK (double d, double age, double SP, double BA, double BA_L,
                        double RDF_L, double SC, double TS,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double p_comp5, p_old5, p_tot5;
    //Calculate probability tree to die due to competition
    //Scots pine and other conifers
    if (SP==1||SP==8)
    {
        ret = Probability_a_tree_to_die_due_to_competition_pine_Hynynenym(d, BA, BA_L, SC, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Norway spruce
    else if (SP==2)
    {
        ret = Probability_a_tree_to_die_due_to_competition_spruce_Hynynenym(d, BA, BA_L, SC, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    //Birches and other deciduous species
    else
    {
        ret = Probability_a_tree_to_die_due_to_competition_deciduous_Hynynenym(d, RDF_L, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }
    p_comp5 = *modelresult;

    if (ret == 0)
        return ret;

    //Calculate probability tree to die due to aging
    ret = Probability_a_tree_to_die_due_to_aging_urban_area_forest_Hynynenym(age, SP, TS, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    p_old5 = *modelresult;

    if (ret == 0)
        return ret;

    //Calculate total probability tree to die
    ret = Probability_a_tree_to_die_Hynynenym(p_comp5, p_old5, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, rectFactor);
    p_tot5 = *modelresult;
    if (ret == 0)
        return ret;

    //Calculate tree's probability to survive
    ret = Probability_a_tree_to_live_JKK(p_tot5, nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);

    *nres = 1;
    return ret;

}

int Maximum_allowable_stem_number_JKK (double D_gs, double SP, double SI_50, double PEAT,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    //Calculate maximum allowable stem number to stratum
    //Old stands on mineral soils
    if (D_gs>12)
    {
        //Mineral soil
        if (PEAT==0)
        {
            //Scots pine and other conifers
            if (SP==1||SP==8)
            {
                ret = Maximum_allowable_stem_number_pine_Hynynenym(D_gs, SI_50,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Norway spruce
            else if (SP==2)
            {
                ret = Maximum_allowable_stem_number_spruce_Hynynenym(D_gs, SI_50,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Silver birch
            else if (SP==3)
            {
                ret = Maximum_allowable_stem_number_white_birch_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Other deciduous species
            else
            {
                ret = Maximum_allowable_stem_number_pubescent_birch_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }

            if (ret == 0)
                return ret;

        }
        //Peatland
        else
        {
            //Scots pine and other conifers
            if (SP==1||SP==8)
            {
                ret = Maximum_allowable_stem_number_peatland_pine_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Norway spruce
            else if (SP==2)
            {
                ret = Maximum_allowable_stem_number_peatland_spruce_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Silver birch
            else if (SP==3)
            {
                ret = Maximum_allowable_stem_number_white_birch_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            //Other deciduous species
            else
            {
                ret = Maximum_allowable_stem_number_pubescent_birch_Hynynenym(D_gs,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }

            if (ret == 0)
                return ret;

        }
    }
    //Young stands (D_gs<=12)
    else
    {
        //Scots pine and other conifers
        if (SP==1||SP==8)
        {
            ret = Maximum_allowable_stem_number_young_stand_pine_Hynynenym(D_gs,
                    nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        }
        //Norway spruce
        else if (SP==2)
        {
            ret = Maximum_allowable_stem_number_young_stand_spruce_Hynynenym(D_gs,
                    nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        }
        //Silver birch
        else if (SP==3)
        {
            ret = Maximum_allowable_stem_number_young_stand_white_birch_Hynynenym(D_gs,
                    nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        }
        //Other deciduous species
        else
        {
            ret = Maximum_allowable_stem_number_young_stand_pubescent_birch_Hynynenym(D_gs,
                    nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        }
    }

    *nres = 1;
    return ret;

}

int Maximum_allowable_stem_number_in_mixed_forest_JKK (double SP, double Upper_st, double Two_st, double N_stratum, double N_upper,
                        double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, double RDF, double RDF_up, double RDF_Sp,
                        double RDF_Ns, double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    //Calculate maximum allowable stem number to stratum in mixed forest, number of strata is at least 2
    //Only if species is not spruce - spruce is not affected by any other species
    if (SP==2)
    {
       *modelresult = N_max_Ns;
    }
    else
    {
        //Scots pine and other conifers
        if (SP==1||SP==8)
        {
            if (SP==8)
            {
               N_max_Sp = N_max_oc;
            }
            if (Two_st==0||(Two_st==1&&(Upper_st==0||(N_stratum>2&&N_upper>=2&&Upper_st==1))))
            {
                ret = Maximum_allowable_stem_number_in_mixed_stand_pine_Hynynenym(Upper_st, N_max_Sp, N_max_Ns,
                        RDF, RDF_up, RDF_Sp, RDF_Ns, RDF_sb, RDF_pb, RDFSp_up, RDFNs_up, RDFsb_up, RDFpb_up,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            else
            {
                *modelresult = N_max_Sp;
            }
        }
        //Silver birch
        else if (SP==3)
        {
            if (Two_st==0||(Two_st==1&&(Upper_st==0||(N_stratum>2&&N_upper>=2&&Upper_st==1))))
            {
                 ret = Maximum_allowable_stem_number_in_mixed_stand_white_birch_Hynynenym(Upper_st, N_max_Sp, N_max_Ns,
                        N_max_sb, N_max_pb, RDF, RDF_up, RDF_Sp, RDF_Ns, RDF_sb, RDF_pb, RDFSp_up, RDFNs_up, RDFsb_up, RDFpb_up,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            else
            {
                *modelresult = N_max_sb;
            }
        }
        //Other deciduous species
        else
        {
            if (SP==5||SP==6||SP==7||SP==9)
            {
                N_max_pb = N_max_od;
            }
            if (Two_st==0||(Two_st==1&&(Upper_st==0||(N_stratum>2&&N_upper>=2&&Upper_st==1))))
            {
                ret = Maximum_allowable_stem_number_in_mixed_stand_pubescent_birch_Hynynenym(Upper_st, N_max_Sp, N_max_Ns,
                        N_max_pb, RDF, RDF_up, RDF_Sp, RDF_Ns, RDF_sb, RDF_pb, RDFSp_up, RDFNs_up, RDFsb_up, RDFpb_up,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
            }
            else
            {
                *modelresult = N_max_pb;
            }
        }
    }

    *nres = 1;
    return ret;

}

int Scale_factor_JKK (double N, double SP, double BA, double D_gM, double Upper_st, double Two_st,
                        double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od,
                        double N_max_Sp_upper, double N_max_Ns_upper, double N_max_sb_upper, double N_max_pb_upper, double N_max_oc_upper, double N_max_od_upper,
                        double N_max_Sp_under, double N_max_Ns_under, double N_max_sb_under, double N_max_pb_under, double N_max_oc_under, double N_max_od_under,
                        double N_maxbg_Sp, double N_maxbg_Ns, double N_maxbg_sb, double N_maxbg_pb, double N_maxbg_oc, double N_maxbg_od,
                        double N_maxbg_Sp_upper, double N_maxbg_Ns_upper, double N_maxbg_sb_upper, double N_maxbg_pb_upper, double N_maxbg_oc_upper, double N_maxbg_od_upper,
                        double N_maxbg_Sp_under, double N_maxbg_Ns_under, double N_maxbg_sb_under, double N_maxbg_pb_under, double N_maxbg_oc_under, double N_maxbg_od_under,
                        double N_Sp, double N_Ns, double N_sb, double N_pb, double N_oc, double N_od,
                        double N_Sp_upper, double N_Ns_upper, double N_sb_upper, double N_pb_upper, double N_oc_upper, double N_od_upper,
                        int *nres, double *modelresult, char *errors,
                        int errorCheckMode, double allowedRiskLevel, double rectFactor)
{
    int ret = 1;
    double Delta_Nmax, Nmax;

    //Assign N_max values based on number of storeys and whether the certain stratums belongs to upper storey
    if (Two_st==1&&Upper_st==0)
    {
        N_max_Sp = N_max_Sp_under;
        N_max_Ns = N_max_Ns_under;
        N_max_sb = N_max_sb_under;
        N_max_pb = N_max_pb_under;
        N_max_oc = N_max_oc_under;
        N_max_od = N_max_od_under;
        N_maxbg_Sp = N_maxbg_Sp_under;
        N_maxbg_Ns = N_maxbg_Ns_under;
        N_maxbg_sb = N_maxbg_sb_under;
        N_maxbg_pb = N_maxbg_pb_under;
        N_maxbg_oc = N_maxbg_oc_under;
        N_maxbg_od = N_maxbg_od_under;
    }
    else if (Two_st==1&&Upper_st==1)
    {
        N_max_Sp = N_max_Sp_upper;
        N_max_Ns = N_max_Ns_upper;
        N_max_sb = N_max_sb_upper;
        N_max_pb = N_max_pb_upper;
        N_max_oc = N_max_oc_upper;
        N_max_od = N_max_od_upper;
        N_maxbg_Sp = N_maxbg_Sp_upper;
        N_maxbg_Ns = N_maxbg_Ns_upper;
        N_maxbg_sb = N_maxbg_sb_upper;
        N_maxbg_pb = N_maxbg_pb_upper;
        N_maxbg_oc = N_maxbg_oc_upper;
        N_maxbg_od = N_maxbg_od_upper;
        N_Sp = N_Sp_upper;
        N_Ns = N_Ns_upper;
        N_sb = N_sb_upper;
        N_pb = N_pb_upper;
        N_oc = N_oc_upper;
        N_od = N_od_upper;
    }

    //Calculate maximum allowable reduction in stem number
    ret = Maximum_allowable_reduction_in_stem_number_Hynynenym(SP, N_max_Sp, N_max_Ns, N_max_sb, N_max_pb, N_max_oc, N_max_od,
                        N_maxbg_Sp, N_maxbg_Ns, N_maxbg_sb, N_maxbg_pb, N_maxbg_oc, N_maxbg_od,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    Delta_Nmax = *modelresult;
    if (ret == 0)
        return ret;

    //Check allowable reduction and update maximum allowable stem number if needed
    //Scots pine and other conifers
    if (SP==1)
    {
        ret = Adjust_maximum_allowable_stem_number_pine_Hynynenym(N, Delta_Nmax, SP, N_Sp, N_max_Sp, N_oc, N_max_oc,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_Sp = *modelresult;
    }
    //Norway spruce
    else if (SP==2)
    {
        ret = Adjust_maximum_allowable_stem_number_spruce_Hynynenym(N, Delta_Nmax, N_Ns, N_max_Ns,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_Ns = *modelresult;
    }
    //Silver birch
    else if (SP==3)
    {
        ret = Adjust_maximum_allowable_stem_number_white_birch_Hynynenym(N, Delta_Nmax, N_sb, N_max_sb,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_sb = *modelresult;
    }
    //Downy birch and other deciduous species
    else if (SP==4)
    {
        ret = Adjust_maximum_allowable_stem_number_pubescent_birch_Hynynenym(SP, N, Delta_Nmax, N_pb, N_max_pb, N_od, N_max_od,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_pb = *modelresult;
    }
    else if (SP==8)
    {
        ret = Adjust_maximum_allowable_stem_number_pine_Hynynenym(N, Delta_Nmax, SP, N_Sp, N_max_Sp, N_oc, N_max_oc,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_oc = *modelresult;
    }
    else
    {
        ret = Adjust_maximum_allowable_stem_number_pubescent_birch_Hynynenym(SP, N, Delta_Nmax, N_pb, N_max_pb, N_od, N_max_od,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
        N_max_od = *modelresult;
    }
    Nmax = *modelresult;

    if (ret == 0)
        return ret;

    //Calculate scale factor
    //Number of stems is less than or equal 2000
    if (N<=2000)
    {
        *modelresult = Nmax/N;

    }
    //Number of stems is between 2000 and 5000
    else if (N>2000&&N<=5000)
    {
        ret = Scale_factor_N_between_2000_and_5000(BA, D_gM, N, SP, N_max_Sp, N_max_Ns, N_max_sb, N_max_pb, N_max_oc, N_max_od,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);

    }
    //Number of stems is greater than 5000
    else
    {
        ret = Scale_factor_N_over_5000(BA, D_gM, SP, N_max_Sp, N_max_Ns, N_max_sb, N_max_pb, N_max_oc, N_max_od,
                        nres, modelresult, errors, errorCheckMode, allowedRiskLevel, 1);
    }

    *nres = 1;
    return ret;

}