import numpy as np
import itertools
import tvb.simulator.models as tvb_simulator_models
import tvb.datatypes.connectivity as tvb_datatypes_connectivity
import tvb.simulator.integrators as tvb_simulator_integrators
import tvb.simulator.simulator as tvb_simulator_simulator
import tvb.simulator.coupling as tvb_simulator_coupling
import tvb.simulator.monitors as tvb_simulator_monitors

TVB_SIMULATION_LENGTH = 10


def tvb_simulation_01():
    '''
        source: https://github.com/the-virtual-brain/tvb-root/blob/master/scientific_library/tvb/tests/validate_model_parameters.py
        source: https://github.com/the-virtual-brain/tvb-root/blob/master/scientific_library/tvb/tests/validate_model_parameters.py
    '''
    tvb_model_2d_oscillator = tvb_simulator_models.Generic2dOscillator()
    # tvb_white_matter = tvb_datatypes_connectivity.Connectivity(load_default=True)
    # tvb_white_matter = tvb_datatypes_connectivity.Connectivity()
    tvb_white_matter = tvb_datatypes_connectivity.Connectivity.from_file()

    """
    source: http://docs.thevirtualbrain.org/_modules/tvb/simulator/integrators.html
    It is a simple example of a predictor-corrector method. It is also known as
    modified trapezoidal method, which uses the Euler method as its predictor.
    And it is also a implicit integration scheme.

    """
    tvb_integrator = tvb_simulator_integrators.HeunDeterministic(dt=2 ** -4)

    tvb_simulator = tvb_simulator_simulator.Simulator(
        model=tvb_model_2d_oscillator,
        connectivity=tvb_white_matter,
        coupling=tvb_simulator_coupling.Linear(a=np.array([0.0126])), #  (a=0.0126),
        integrator=tvb_integrator,
        monitors=[tvb_simulator_monitors.Raw()],
    )

    exploration_settings = [
        ('model.tau', [0.0, 1.0]),
        ('model.b', [-5.0, 15.0]),
        ('model.d', [0.0, 0.5, 1.0]),
        # ('coupling.a', [1,3])  # you can also use non-model parameter dimensions like this
    ]


    '''
    tvb.simulator.lab.run_exploration(
        tvb_simulator,
        simulation_length=10,
        parameters=sample_parameter_space_cartesian(exploration_settings)
    )
    '''

    # transposing
    paths, values = list(zip(*exploration_settings))
    print('paths={}'.format(paths))
    print('values={}'.format(values))

    # cartesian product, equivalent to a nested for-loop
    for value_assignment in itertools.product(*values):
        # yield dict(list(zip(paths, value_assignment)))
        parameters = dict(list(zip(paths, value_assignment)))
        print(parameters)

        for curr_key, curr_val in parameters.items():
            # code = 'import numpy as np; sim.{} = np.array([val])'.format(curr_key)
            code = 'sim.{} = np.array([val])'.format(curr_key)
            print(code)
            # exec (code, {'sim': tvb_simulator, 'val': curr_val})
            exec (code, {'__builtins__': None, 'np': np}, {'sim': tvb_simulator, 'val': curr_val})
            #tvb_simulator.model.tau = np.array([curr_val])
            #tvb_simulator.model.b = np.array([curr_val])
            #tvb_simulator.model.d = np.array([curr_val])

            tvb_simulator.configure()
            try:
                for traw in tvb_simulator(simulation_length=TVB_SIMULATION_LENGTH):
                    traw = traw[0]
                    state = traw[1]
                    if not np.all(np.isfinite(state)):
                        raise FloatingPointError('infinities generated outside numpy')
                print('TVB Simulation OK')
            except FloatingPointError:
                print('Wrong result from TVB Simulation')


if __name__ == '__main__':
    tvb_simulation_01()
