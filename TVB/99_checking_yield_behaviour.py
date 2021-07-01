import itertools

def sample_parameter_space_cartesian(path_assignments):
    """
    Samples the parameter space systematically based on explicit values for each dimension (parameter).
    :param path_assignments: a list of (param_name, [param_values])
    >>> list(sample_parameter_space_cartesian([('a', [1, 2]), ('b', [3, 4])]))
    [{'a': 1, 'b': 3}, {'a': 1, 'b': 4}, {'a': 2, 'b': 3}, {'a': 2, 'b': 4}]
    """
    # 'transpose' path_assignments
    paths, values = list(zip(*path_assignments))
    print(paths)
    print(values)
    # cartesian product of value assignments
    for value_assignment in itertools.product(*values):
        yield dict(list(zip(paths, value_assignment)))


def run_yield_proba(to_be_printed=None):
    print(to_be_printed)

def main_proba():
    exploration_settings = [
        ('model.tau', [0.0, 1.0]),
        ('model.b', [-5.0, 15.0]),
        ('model.d', [0.0, 0.5, 1.0]),
        # ('coupling.a', [1,3])  # you can also use non-model parameter dimensions like this
    ]
    for current_yield_value in sample_parameter_space_cartesian(exploration_settings):
        print(current_yield_value)

if __name__ == '__main__':
    main_proba()
