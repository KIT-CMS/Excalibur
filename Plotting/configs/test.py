import itertools


def test_get_n_dim_weights(binning_dict):
    weights_list = []
    for quantity in binning_dict.keys():
        quantity_weights_list = []
        for bin_index in range(len(binning_dict[quantity])-1):
            quantity_weights_list += [str(quantity) + '>' + str(binning_dict[quantity][bin_index]) + '&&' +
                                      str(quantity) + '<' + str(binning_dict[quantity][bin_index + 1])]
        weights_list += [quantity_weights_list]

    return map('&&'.join, list(itertools.product(*weights_list)))


def test():

    binning_dict = {'zeta': [-5.191, -3.139, -2.964, -2.5, -1.93, -1.305, -0.783, 0., 0.783, 1.305, 1.93, 2.5, 2.964,
                               3.139, 5.191],
                     'zpt': [30, 50, 75, 125, 175, 225, 300, 400, 1000]
        }

    print(get_n_dim_weights(binning_dict))


    binning_dict = {'zeta': [-5.191, -3.139, -2.964, -2.5, -1.93, -1.305, -0.783, 0., 0.783, 1.305, 1.93, 2.5, 2.964, 3.139, 5.191],
                    'zpt': [30, 50, 75, 125, 175, 225, 300, 400, 1000],
                    'alpha': [0.0, 0.1, 0.2, 0.3]
                    }

    print(get_n_dim_weights(binning_dict))


    binning_dict = {'zeta': [-5.191, -3.139, -2.964, -2.5, -1.93, -1.305, -0.783, 0., 0.783, 1.305, 1.93, 2.5, 2.964, 3.139, 5.191]
                    }
    print(get_n_dim_weights(binning_dict))


    binning_dict = {'zeta': [-5.191, -2.5, -1.305, 0., 1.305, 2.5, 5.191],
                    'zpt': [30, 100, 1000]
                    }
    print(get_n_dim_weights(binning_dict))



def merge_dicts_containing_lists_only(dict_one, dict_two):
    return {key: value + dict_two[key] if isinstance(value, (list,)) and isinstance(dict_two[key], (list,)) else None for key, value in dict_one.iteritems()}
