// Copyright (c) 2007 Simosol Oy. Distributed under the GNU General Public License 2.0.

//////////////////////////////////////////////////////////////////////////////
//
//  DistributiondeadtreemodelLibrary.cpp
//
//    DistributiondeadtreeModels - Source file
//
//    Here are the conventional calls of the functions

#include <stdio.h>
#include "DistributiondeadtreemodelLibrary.h"
#include "SimoUtils.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

double * get_dead_tree_values (double sp, double snag, double d, double since_death, double SC)
{
	// Returns dead tree's stem number, volume, density and above ground biomass based on key
	// Key is combination of species, diameter class, snag and since death
	//
	int i, j, nrows;
	//	Create array for geographical ingormations
	double * dead_val = (double *) malloc(4 * sizeof(double));
	int found = 0;  // Indicates if the right row was found
	if (SC < 4) {
	    nrows = 56;  // Number of rows in the array
	    //NB sp, snag, d, since_death, n, v, density and BM_aboveground
	    double table[56][8] = {{1,0,12.5,5,0.0234,0.002,396.09,1.06},
				{1,0,12.5,15,0.0305,0.0026,396.09,1.39},
				{1,0,12.5,25,0.015,0.0013,396.09,0.68},
				{1,0,12.5,35,0.0045,0.0004,396.09,0.2},
				{1,0,17.5,5,0.0043,0.0008,396.21,0.41},
				{1,0,17.5,15,0.0066,0.0011,396.08,0.6},
				{1,0,17.5,25,0.0057,0.001,395.98,0.51},
				{1,0,17.5,35,0.0027,0.0004,395.72,0.23},
				{1,0,22.5,5,0.0052,0.0016,397.98,0.85},
				{1,0,22.5,15,0.0041,0.0013,397.83,0.66},
				{1,1,17.5,5,0.001,0.0002,396.43,0.1},
				{1,1,22.5,5,0.0015,0.0006,400.5,0.3},
				{1,1,27.5,5,0.002,0.0011,398.68,0.56},
				{2,0,7.5,5,0.0492,0.0014,404.86,1},
				{2,0,7.5,15,0.0542,0.0016,404.86,1.1},
				{2,0,7.5,25,0.0258,0.0008,404.86,0.52},
				{2,0,12.5,5,0.8207,0.0536,397.97,34.9},
				{2,0,12.5,15,2.1054,0.1376,397.97,89.53},
				{2,0,12.5,25,2.4266,0.1586,397.97,103.19},
				{2,0,17.5,5,1.1212,0.2133,389.71,130.25},
				{2,0,17.5,15,2.3301,0.4209,389.41,257.95},
				{2,0,17.5,25,2.3074,0.4158,389.39,254.87},
				{2,0,22.5,5,0.6891,0.2045,385.55,121.57},
				{2,0,22.5,15,0.592,0.1755,384.48,104.4},
				{2,0,22.5,25,0.3629,0.1074,384.11,63.94},
				{2,0,27.5,5,0.2042,0.0975,379.36,56.18},
				{2,0,27.5,15,0.0865,0.0416,376.6,24},
				{2,0,27.5,25,0.0672,0.0322,376.5,18.57},
				{2,0,32.5,5,0.0518,0.0392,370.64,21.85},
				{2,0,32.5,15,0.0117,0.0086,367.99,4.83},
				{2,0,32.5,25,0.0043,0.0031,367.08,1.73},
				{2,1,12.5,5,0.2409,0.0157,397.97,10.24},
				{2,1,12.5,15,0.4817,0.0315,397.97,20.49},
				{2,1,12.5,25,0.3212,0.021,397.97,13.66},
				{2,1,17.5,5,0.0768,0.0172,390.59,10.4},
				{2,1,22.5,5,2.6473,0.849,387.39,504.14},
				{2,1,22.5,15,1.4798,0.4485,386.9,266.81},
				{2,1,27.5,5,0.3731,0.18,380.87,103.75},
				{2,1,27.5,25,0.0299,0.0144,378.61,8.3},
				{2,1,32.5,15,0.0116,0.0088,369.99,4.88},
				{3,0,12.5,5,0.0808,0.0094,494.65,6.1},
				{3,0,12.5,15,0.1019,0.0103,494.52,6.69},
				{3,0,17.5,5,0.1856,0.0291,500.9,19.27},
				{3,0,17.5,15,0.1719,0.0263,500.31,17.35},
				{3,0,22.5,5,0.0287,0.0118,505.18,7.93},
				{3,0,22.5,15,0.0407,0.0115,504.99,7.7},
				{3,0,27.5,5,0.0079,0.0034,508.45,2.34},
				{3,0,27.5,15,0.0078,0.0034,508.32,2.3},
				{3,1,12.5,15,0.0115,0.001,495.25,0.67},
				{3,1,17.5,5,0.0196,0.0036,506.07,2.42},
				{3,1,17.5,15,0.0639,0.01,501.15,6.64},
				{3,1,22.5,5,0.0373,0.0112,508.68,7.46},
				{3,1,22.5,15,0.0189,0.0054,507.23,3.59},
				{3,1,27.5,5,0.0249,0.012,511.19,8.09},
				{3,1,27.5,15,0.0084,0.0039,510.1,2.65},
				{3,1,32.5,5,0.0026,0.0017,513.53,1.13}};
	    for (i=0; i<nrows; i++) {
		if (table[i][0] == sp && table[i][1] == snag && table[i][2] == d && table[i][3] == since_death) {
			for (j=0; j<4; j++) {
				dead_val[j] = table[i][j+4];
			}
			found = 1;
			break;
		}
	    }
	    if (found == 0) {
		dead_val[0] = 0.;
		dead_val[1] = 0.;
		dead_val[2] = 0.;
		dead_val[3] = 0.;
	    }
	}
	else {
	    nrows = 27;  // Number of rows in the array
	    //NB sp, snag, d, since_death, n, v, density and BM_aboveground
	    double table[27][8] = {{1,0,7.5,5,0.0492,0.0014,404.86,1},
				{1,0,7.5,15,0.0542,0.0016,404.86,1.1},
				{1,0,7.5,25,0.0258,0.0008,404.86,0.52},
				{1,0,12.5,5,0.8207,0.0536,397.97,34.9},
				{1,0,12.5,15,2.1054,0.1376,397.97,89.53},
				{1,0,12.5,25,2.4266,0.1586,397.97,103.19},
				{1,0,17.5,5,1.1212,0.2133,389.71,130.25},
				{1,0,17.5,15,2.3301,0.4209,389.41,257.95},
				{1,0,17.5,25,2.3074,0.4158,389.39,254.87},
				{1,0,22.5,5,0.6891,0.2045,385.55,121.57},
				{1,0,22.5,15,0.592,0.1755,384.48,104.4},
				{1,0,22.5,25,0.3629,0.1074,384.11,63.94},
				{1,0,27.5,5,0.2042,0.0975,379.36,56.18},
				{1,0,27.5,15,0.0865,0.0416,376.6,24},
				{1,0,27.5,25,0.0672,0.0322,376.5,18.57},
				{1,0,32.5,5,0.0518,0.0392,370.64,21.85},
				{1,0,32.5,15,0.0117,0.0086,367.99,4.83},
				{1,0,32.5,25,0.0043,0.0031,367.08,1.73},
				{1,1,12.5,5,0.2409,0.0157,397.97,10.24},
				{1,1,12.5,15,0.4817,0.0315,397.97,20.49},
				{1,1,12.5,25,0.3212,0.021,397.97,13.66},
				{1,1,17.5,5,0.0768,0.0172,390.59,10.4},
				{1,1,22.5,5,2.6473,0.849,387.39,504.14},
				{1,1,22.5,15,1.4798,0.4485,386.9,266.81},
				{1,1,27.5,5,0.3731,0.18,380.87,103.75},
				{1,1,27.5,25,0.0299,0.0144,378.61,8.3},
				{1,1,32.5,15,0.0116,0.0088,369.99,4.88}};
	    for (i=0; i<nrows; i++) {
		if (table[i][0] == sp && table[i][1] == snag && table[i][2] == d && table[i][3] == since_death) {
			for (j=0; j<4; j++) {
				dead_val[j] = table[i][j+4];
			}
			found = 1;
			break;
		}
	    }
	    if (found == 0) {
		dead_val[0] = 0.;
		dead_val[1] = 0.;
		dead_val[2] = 0.;
		dead_val[3] = 0.;
	    }
	}

	return dead_val;
}

int Dead_tree_empty_distribution(double d_class_width, double max_d, double since_death_class_width,
                                 double max_since_death, double max_class_count, int *nres, struct deadtreeclass *dist,
                                 char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor)

{
    int ret;
    int ind, h, i, j, k;
    double sp, d_classes, sd_classes, class_count, my_d, my_sd;
    char errorStr[100] = "";

    ret = 1;


    //Check for fatal errors
    if (d_class_width<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "d_class_width<=0(d_class_width=",d_class_width);
    }
    if (max_d<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "max_d<=0(max_d=",max_d);
    }
    if (since_death_class_width<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "since_death_class_width<=0(since_death_class_width=",since_death_class_width);
    }
    if (max_since_death<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "max_since_death<=0(max_since_death=",max_since_death);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    // how many diameter-since death-snag-classes, and does that exceed the max limit set for simulator
    d_classes = ceil(max_d / d_class_width);
    sd_classes = ceil(max_since_death / since_death_class_width);
    class_count = 3. * d_classes * sd_classes * 2.;
    if (class_count>max_class_count)
    {
        constructErrorMessage (errorStr, "max_class_count exceeded(class_count=",class_count);
        strcat(errors, errorStr);
        return 0;
    }

    ind = 0;
    my_d = 0.;
    my_sd = 0.;
    for (h=0; h <= 2; h++) {
        if (h == 0) {
            sp = 1.;
        }
        else if (h == 1) {
            sp = 2.;
        }
        else {
            sp = 3.;
        }
        for (i=0; i < d_classes; i++) {
            if (i == 0) {    // first class
                my_d = d_class_width / 2.;
            }
            else {
                my_d += d_class_width;
            }
            for (j=0; j < sd_classes; j++)  {
                if (j == 0) {    // first class
                    my_sd = since_death_class_width / 2.;
                }
                else {
                    my_sd += since_death_class_width;
                }
                for (k=0; k < 2; k++)  { // snag classes
                    dist[ind].sp = sp;
                    dist[ind].d = my_d;
                    dist[ind].since_death = my_sd;
                    dist[ind].snag = k;
                    dist[ind].decay_class = 0.;
                    dist[ind].n = 0.;
                    dist[ind].v = 0.;
                    dist[ind].density = 0.;
                    dist[ind].bm_aboveground_total = 0.;
                    dist[ind].v_ad = 0.;
                    dist[ind].density_ad = 0.;
                    dist[ind].bm_total_ad = 0.;
                    ind += 1;
                }
            }
        }
    }

    *nres = class_count;

    return ret;
}

int Dead_tree_distribution_with_init_values(double d_class_width, double max_d, double since_death_class_width,
                                 double max_since_death, double max_class_count, double SC, int *nres, struct deadtreeclass *dist,
                                 char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor)

{
    int ret;
    int ind, h, i, j, k;
    double sp, d_classes, sd_classes, class_count, my_d, my_sd;
    char errorStr[100] = "";

    ret = 1;


    //Check for fatal errors
    if (d_class_width<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "d_class_width<=0(d_class_width=",d_class_width);
    }
    if (max_d<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "max_d<=0(max_d=",max_d);
    }
    if (since_death_class_width<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "since_death_class_width<=0(since_death_class_width=",since_death_class_width);
    }
    if (max_since_death<=0)
    {
        ret = 0;
        constructErrorMessage (errorStr, "max_since_death<=0(max_since_death=",max_since_death);
    }
    if (ret == 0) {
        strcat(errors, errorStr);
        return 0;
    }

    // how many diameter-since death-snag-classes, and does that exceed the max limit set for simulator
    d_classes = ceil(max_d / d_class_width);
    sd_classes = ceil(max_since_death / since_death_class_width);
    class_count = 3. * d_classes * sd_classes * 2.;
    if (class_count>max_class_count)
    {
        constructErrorMessage (errorStr, "max_class_count exceeded(class_count=",class_count);
        strcat(errors, errorStr);
        return 0;
    }

    ind = 0;
    my_d = 0.;
    my_sd = 0.;
    for (h=0; h <= 2; h++) {
        if (h == 0) {
            sp = 1.;
        }
        else if (h == 1) {
            sp = 2.;
        }
        else {
            sp = 3.;
        }
        for (i=0; i < d_classes; i++) {
            if (i == 0) {    // first class
                my_d = d_class_width / 2.;
            }
            else {
                my_d += d_class_width;
            }
            for (j=0; j < sd_classes; j++)  {
                if (j == 0) {    // first class
                    my_sd = since_death_class_width / 2.;
                }
                else {
                    my_sd += since_death_class_width;
                }
                for (k=0; k < 2; k++)  { // snag classes
                    double * dead_val = get_dead_tree_values(sp,k,my_d,my_sd,SC);	
                    dist[ind].sp = sp;
                    dist[ind].d = my_d;
                    dist[ind].since_death = my_sd;
                    dist[ind].snag = k;
                    dist[ind].decay_class = 0.;
                    dist[ind].n = dead_val[0];
                    dist[ind].v = dead_val[1];
                    dist[ind].density = dead_val[2];
                    dist[ind].bm_aboveground_total = dead_val[3];
                    dist[ind].v_ad = 0.;
                    dist[ind].density_ad = 0.;
                    dist[ind].bm_total_ad = 0.;
                    ind += 1;
                    free(dead_val);  // Free dynamically allocated memory
                }
            }
        }
    }

    *nres = class_count;

    return ret;
}

