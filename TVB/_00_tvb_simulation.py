import numpy as np

OUTPUT_PATH = '.'
BEGIN = 0.0
END = 1000.0

param_co_simulation = {
    # boolean for check if there are or not co-simulation
    'co-simulation': False,
    # number of MPI process for nest
    # select if nest is use or not
    'nb_MPI_nest': 1,
    # save or not nest( result with MPI )
    'record_MPI': False,
    # id of region simulate by nest
    'id_region_nest': [],
    # time of synchronization between node
    'synchronization': 0.,  # Todo compute with the min of delay
    # level of log : debug 0, info 1, warning 2, error 3, critical 4
    'level_log': 1,
    # if running in cluster:
    'cluster': False
}

# parameter_test.param_co_simulation['nb_MPI_nest']=0
param_co_simulation['nb_MPI_nest'] = 0

# run_exploration_2D(path,
#                    parameter_test,
#                   {'g':np.arange(0.0, 1.0, 0.5),
#                    'mean_I_ext': np.arange(0.0, 100.0, 50.0)}, begin, end)

simulation_2D_variables_dict = {'g': np.arange(0.0, 1.0, 0.5),
                                'mean_I_ext': np.arange(0.0, 100.0, 50.0)}

for g_value in simulation_2D_variables_dict['g']:
    print('>g={}'.format(g_value))
    for mean_I_ext_value in simulation_2D_variables_dict['mean_I_ext']:
        print('>>mean_I_ext={}'.format(mean_I_ext_value))

        # run_exploration( results_path,
        #                  parameter_default,
        #                  {name_variable_1:variable_1,
        #                   name_variable_2:variable_2},
        #                   begin,end)
        #   # parameters = generate_parameter(parameter_default,
        #   #                                 results_path,
        #   #                                 dict_variable)


