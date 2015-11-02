# Excalibur Python Configuration Format

Excalibur uses python configuration files, which are converted to Artus' JSON format.
The excalibur configs must follow a specific protocol to create the settings.
In practice, a config is a script creating a `dict` containing various `str` keys to `float`, `int`, `list` and other values specifying settings.

There are two types of configuration files: base and modifiers.
- The base provides the actual foundation of settings. A single base config is always required.
- Modifiers may add, remove or modify settings. They are optional and as many as required may be used.

	excalibur.py base_config [mod_config1[, mod_config2[, ...]]]

## Base Configs

A regular python script which must provide the function

	config() -> dict

The returned `dict` is the basis for the configuration.
It's keys correspond to the names of Artus options and their values are the respective setting to use.

In general, such a configuration should be able to work on its own.
The `configtools` can greatly help reduce code required to be written.

## Modifier Configs

A regular python script which must provide the function

	modify_config(cfg: dict) -> dict

The input `dict ist the previous configuration.
The returned `dict` is used for further configuration.

Usually, such a configuration will not be able to work on its own.

### Modifier Evaluation

Modifiers are applied in the order they are given to Excalibur.
For example,

	excalibur.py my_base run_mod foo_mod

is internally executed as

	foo_mod.modify_config(run_mod.modify_config(my_base.config()))
