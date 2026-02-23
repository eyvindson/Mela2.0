//////////////////////////////////////////////////////////////////////////////
//
//  BiomassmodelLibrary.h
//
//	Biomass model library - Header file
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

struct Biomass_tree {
	double density;
	double BM_stump;
	double BM_roots;
	double BM_branches;
	double BM_foliage;
};

struct Biomass_tree_Yasso {
	double density;
	double BM_stump;
	double BM_roots;
	double BM_branches;
	double BM_foliage;
	double BM_fine_roots;
	double BM_stem_bark;
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

DLLEXPORT int Biomass_stem_pine_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_bark_of_stem_pine_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_with_needles_pine_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_pine_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_pine_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_little_roots_pine_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_big_roots_pine_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_spruce_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_bark_of_stem_spruce_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_with_needles_spruce_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_spruce_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_spruce_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_little_roots_spruce_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_big_roots_spruce_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_birch_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_bark_of_stem_birch_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_without_leaves_birch_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_foliage_birch_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_birch_Marklund (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_birch_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_little_roots_birch_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_big_roots_birch_Marklund (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_and_roots_pine_Petersson_Stohl (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_and_roots_spruce_Petersson_Stohl (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_and_roots_birch_Petersson_Stohl (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_pine_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_pine_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_pine_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_needles_pine_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_pine_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_pine_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_pine_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_pine_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_needles_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_spruce_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_spruce_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_spruce_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_birch_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_birch_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_birch_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_foliage_birch_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_birch_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_birch_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_birch_Repola_Ojansuu (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_birch_Repola_Ojansuu (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_wood_without_bark_pine_Repola_Ojansuu (double d, double a, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_pine_Repola_Ojansuu (double d, double a, double TS, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_wood_without_bark_spruce_Repola_Ojansuu (double d, double a, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_spruce_Repola_Ojansuu (double d, double a, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_wood_without_bark_birch_Repola_Ojansuu (double d, double a, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Density_stem_birch_Repola_Ojansuu (double d, double a, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_pine_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_pine_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_pine_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_needles_pine_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_pine_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_pine_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_pine_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_pine_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_needles_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_spruce_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_spruce_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_spruce_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_wood_birch_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_birch_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_living_branches_birch_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_foliage_birch_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_dead_branches_birch_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_aboveground_total_birch_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_birch_Repola (double d, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_roots_birch_Repola (double d, double h, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_bark_JKK (double BM_stem, double BM_stem_bark, double BM_stump, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_tree_JKK (double d, double h, double a, double SP, double TS, int *nres, struct Biomass_tree *biomass, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_tree_Yasso_JKK (double d, double h, double a, double SP, double TS, int *nres, struct Biomass_tree_Yasso *biomass, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stem_bark_JKK (double d, double h, double SP, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stratum_Yasso_JKK (double d, double h, double a, double SP, double TS, int *nres, struct Biomass_tree_Yasso *biomass, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Biomass_stump_bark_stratum_JKK (double BM_stem, double BM_stem_bark, double BM_stump, int *nres, double *modelresult, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);

#ifdef __cplusplus
}
#endif