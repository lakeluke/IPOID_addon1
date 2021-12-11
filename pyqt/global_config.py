import json
import configparser
import os

global config_params, config_source


def init():
    global config_params, config_source
    config_params = {}
    config_source = ''
    load()


def set_value(section, option, value):
    global config_params
    config_params[section][option] = value


def get_value(section, option, default_value=None):
    global config_params
    try:
        return config_params[section][option]
    except KeyError:
        return default_value


def load_json(json_file):
    with open(json_file, 'r') as f:
        global config_params
        config_params = json.load(f)
        f.close()


def dump_json(json_file='./config_template.json'):
    global config_params
    with open(json_file, 'w') as f:
        json.dump(config_params, f)
        f.close()


def load_conf(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    for section in config.sections():
        config_params[section] = {}
        for option in config.options(section):
            value_str = config.get(section, option)
            if value_str.lower() == 'true':
                value = True
            elif value_str.lower() == 'false':
                value = False
            elif value_str.isnumeric():
                if value_str.find('.') != -1:
                    value = float(value_str)
                else:
                    value = int(value_str)
            else:
                value = value_str
            config_params[section][option] = value


def dump_conf(conf_file='./config_template.ini'):
    global config_params
    config = configparser.ConfigParser()
    for section in config_params.keys():
        config.add_section(section)
        for option, value in config_params[section].items():
            config.set(section, option, str(value))
    with open(conf_file, 'w') as f:
        config.write(f)
        f.close()


def load():
    global config_source
    conf_file = './config.ini'
    json_file = './config.json'
    if os.path.exists(conf_file):
        load_conf(conf_file)
        config_source = 'conf'
    elif os.path.exists(json_file):
        load_json(json_file)
        config_source = 'json'
    else:
        create_default_config(True)
        config_source = 'default'


def create_default_config(create_template_file):
    global config_params
    config_params = {'eyetracker': {'frequency': 60,
                                    'calibration_point_number': 9},
                     'database': {'path': './imgdb'},
                     'data': {'path': './outdata'},
                     'log': {'path': './log'},
                     'image_show':{
                         'last_time': 10,
                         'time_interval': 3
                     },
                     'mode': {'debug': False,
                              'ignore_no_eyetracker': False,
                              'skip_eyetracker_calibration': False,
                              'ignore_eyedata_error': False
                              }
                     }
    if create_template_file:
        dump_conf()
        dump_json()


if __name__ == '__main__':
    init()
    print(config_source)
    print(config_params)
