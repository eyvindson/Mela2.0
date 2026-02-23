//////////////////////////////////////////////////////////////////////////////
//
//  DistributiondeadtreemodelLibrary.h
//
//    DistributiondeadtreeModels - Header file
//
//    Here all model functions must be defined

#if MODE==1
# define DLLEXPORT __declspec (dllexport)
#elif MODE==2
# define DLLEXPORT
#elif MODE==3
# define DLLEXPORT
#endif

#define PI 3.1415926535897932384626433832795029

struct deadtreeclass {
    double sp;
    double d;
    double since_death;
    double snag;
    double decay_class;
    double n;
    double v;
    double density;
    double bm_aboveground_total;
    double v_ad;
    double density_ad;
    double bm_total_ad;
};

//    Conventional function declarations used when the library is linked
//    using the .LIB file / tjp 4.5.2005

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

DLLEXPORT int Dead_tree_empty_distribution(double d_class_width, double max_d, double since_death_class_width, double max_since_death, double max_class_count, int *nres, struct deadtreeclass *dist, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);
DLLEXPORT int Dead_tree_distribution_with_init_values(double d_class_width, double max_d, double since_death_class_width, double max_since_death, double max_class_count, double SC, int *nres, struct deadtreeclass *dist, char *errors, int errorCheckMode, double allowedRiskLevel, double rectFactor);

#ifdef __cplusplus
}
#endif
