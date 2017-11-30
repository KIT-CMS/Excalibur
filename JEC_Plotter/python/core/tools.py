
def print_dict_recursive(dct, output_stream=sys.stdout, indent_level=0, indent_width=4, indent_char=' ', filter_func=lambda x: True):
    _max_key_len = max([len(_key) for _key in dct.keys()])
    _key_format = "{{:{0}}}".format(_max_key_len + 5)

    _indent_prefix = indent_char * indent_width * indent_level

    for k, v in dct.iteritems():
        if isinstance(v, dict):
            output_stream.write(_indent_prefix + _key_format.format(k+':') + '\n')
            output_stream.flush()
            print_dict_recursive(v, indent_level=indent_level+1,  indent_width=indent_width, indent_char=indent_char, filter_func=filter_func)
        else:
            if filter_func(v):
                _content = "{}".format(v)
                if '\n' in _content:
                    _content = '\n' + _content
                    _content = _content.replace('\n', '\n{}{}'.format(_indent_prefix, indent_char * indent_width))
                output_stream.write(_indent_prefix + _key_format.format(k+':') + _content + '\n')
                output_stream.flush()