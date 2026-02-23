// Copyright (c) 2007 Simosol Oy. Distributed under the GNU General Public License 2.0.

//////////////////////////////////////////////////////////////////////////////
//
//  NaturalremovalmodelLibrary.cpp
//
//	Natural removal model library - Header file
//
//	Here all model functions must be defined

#if MODE==1
# define DLLEXPORT __declspec (dllexport)
#elif MODE==2
# define DLLEXPORT
#elif MODE==3
# define DLLEXPORT
#endif

#define PI 3.1415926535897932384626433832795029

struct N_maxbg {
	double N_maxbg_Sp;
	double N_maxbg_Ns;
	double N_maxbg_sb;
	double N_maxbg_pb;
	double N_maxbg_oc;
	double N_maxbg_od;
	double N_maxbg_Sp_upper;
	double N_maxbg_Ns_upper;
	double N_maxbg_sb_upper;
	double N_maxbg_pb_upper;
	double N_maxbg_oc_upper;
	double N_maxbg_od_upper;
	double N_maxbg_Sp_under;
	double N_maxbg_Ns_under;
	double N_maxbg_sb_under;
	double N_maxbg_pb_under;
	double N_maxbg_oc_under;
	double N_maxbg_od_under;
};

//	Conventional function declarations used when the library is linked
//	using the .LIB file / tjp 4.5.2005

//  All the model calls follow the same rules for the input parameters. Each
//  model is called with the actual model parameters, plus a set of pointers
//  which the model function sets to contain the number of results, the
//  actual modelresult, warnings and errors. The last three parameters
//  are the error checking mode, allowed risk level and the rectification
//  factor for the model. This way the models can be called easily from python
//  and C/C++ implementation. / AM 2.9.2005

//Undecorate C++ functions
#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int Mimimum_growing_space_pine_Hynynenym (double d_s, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Mimimum_growing_space_spruce_Hynynenym (double d_s, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Mimimum_growing_space_white_birch_Hynynenym (double d_s, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Mimimum_growing_space_pubescent_birch_Hynynenym (double d_s, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_due_to_competition_pine_Hynynenym (double d, double BA, double BA_L, double SC, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_due_to_competition_spruce_Hynynenym (double d, double BA, double BA_L, double SC, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_due_to_competition_deciduous_Hynynenym (double d, double RDFL, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_due_to_aging_Hynynenym (double age, double sp, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_Hynynenym (double p_comp5, double p_old5, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_live_JKK (double p_tot5, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_peatland_pine_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_peatland_spruce_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_white_birch_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_pubescent_birch_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_pine_Hynynenym (double D_gs, double SI_50, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_spruce_Hynynenym (double D_gs, double SI_50, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_young_stand_pine_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_young_stand_spruce_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_young_stand_white_birch_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_young_stand_pubescent_birch_Hynynenym (double D_gs, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Scale_factor_N_over_5000 (double BA, double D_gM, double SP, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Scale_factor_N_between_2000_and_5000 (double BA, double D_gM, double N, double SP, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_in_mixed_stand_pine_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_in_mixed_stand_white_birch_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_in_mixed_stand_pubescent_birch_Hynynenym (double Upper_st, double N_max_Sp, double N_max_Ns, double N_max_pb, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_before_growing_Hynynenym (double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, double N_max_Sp_upper, double N_max_Ns_upper, double N_max_sb_upper, double N_max_pb_upper, double N_max_oc_upper, double N_max_od_upper, double N_max_Sp_under, double N_max_Ns_under, double N_max_sb_under, double N_max_pb_under, double N_max_oc_under, double N_max_od_under, int *nres, struct N_maxbg *n_maxbg, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_reduction_in_stem_number_Hynynenym (double SP, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, double N_maxbg_Sp, double N_maxbg_Ns, double N_maxbg_sb, double N_maxbg_pb, double N_maxbg_oc, double N_maxbg_od, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Adjust_maximum_allowable_stem_number_pine_Hynynenym (double N, double Delta_Nmax, double SP, double N_Sp, double N_max_Sp, double N_oc, double N_max_oc, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Adjust_maximum_allowable_stem_number_spruce_Hynynenym (double N, double Delta_Nmax, double N_Ns, double N_max_Ns, int *nres, double *modelresult, char *errors,	int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Adjust_maximum_allowable_stem_number_white_birch_Hynynenym (double N, double Delta_Nmax, double N_sb, double N_max_sb, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Adjust_maximum_allowable_stem_number_pubescent_birch_Hynynenym (double SP, double N, double Delta_Nmax, double N_pb, double N_max_pb, double N_od, double N_max_od, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Minimum_growing_space_JKK (double d_s, double SP,	int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Tree_survival_JKK (double d, double age, double SP, double BA, double BA_L, double RDF_L, double SC, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_JKK (double D_gs, double SP, double SI_50, double PEAT, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Maximum_allowable_stem_number_in_mixed_forest_JKK (double SP, double Upper_st, double Two_st, double N_stratum, double N_upper, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, double RDF, double RDF_up, double RDF_Sp, double RDF_Ns, double RDF_sb, double RDF_pb, double RDFSp_up, double RDFNs_up, double RDFsb_up, double RDFpb_up, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Scale_factor_JKK (double N, double SP, double BA, double D_gM, double Upper_st, double Two_st, double N_max_Sp, double N_max_Ns, double N_max_sb, double N_max_pb, double N_max_oc, double N_max_od, double N_max_Sp_upper, double N_max_Ns_upper, double N_max_sb_upper, double N_max_pb_upper, double N_max_oc_upper, double N_max_od_upper, double N_max_Sp_under, double N_max_Ns_under, double N_max_sb_under, double N_max_pb_under, double N_max_oc_under, double N_max_od_under, double N_maxbg_Sp, double N_maxbg_Ns, double N_maxbg_sb, double N_maxbg_pb, double N_maxbg_oc, double N_maxbg_od, double N_maxbg_Sp_upper, double N_maxbg_Ns_upper, double N_maxbg_sb_upper, double N_maxbg_pb_upper, double N_maxbg_oc_upper, double N_maxbg_od_upper, double N_maxbg_Sp_under, double N_maxbg_Ns_under, double N_maxbg_sb_under, double N_maxbg_pb_under, double N_maxbg_oc_under, double N_maxbg_od_under, double N_Sp, double N_Ns, double N_sb, double N_pb, double N_oc, double N_od, double N_Sp_upper, double N_Ns_upper, double N_sb_upper, double N_pb_upper, double N_oc_upper, double N_od_upper, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Tree_survival_urban_area_forest_JKK (double d, double age, double SP, double BA, double BA_L, double RDF_L, double SC, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Probability_a_tree_to_die_due_to_aging_urban_area_forest_Hynynenym (double age, double sp, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);

#ifdef __cplusplus
}
#endif