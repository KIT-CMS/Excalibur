# Config Classes

The python configurations can use several classes which provide advanced functionality in place of fixed config values. Usually, they will handle dynamic dependencies or calculations.

## General Structure

The config classes can be used instead of native python values (e.g. `1`, `"bar"`, `True`).
When the python configuration is written to an Artus JSON, each classes' attribute `artus_value` is written instead of the whole class.
In practically all cases, `artus_value` is actually a python *property* - a function that is implicity called to get the value.
If the value represented by a class is required in the python configuration, it can be explicitly dereferenced with the `resolve` method.

There are no more requirements for config classes. If you want to write your own, any class with an attribute/property named `artus_value` and providing a `resolve` method is valid.

The encoding to JSON is handled/implemented inside `excalibur.py`.

## Available Classes

There are several classes available for configuration.
For more detailed information on specific classes, pelase see their respective documentation.

**InputFiles**

- Provides input file glob depending on current domain (NAF, EKP, ...)

**RunJSON**

- Abstraction of CMS run JSONs with joins and run whitelisting
- Resolves to path to the appropriate base or dynamically created JSON file

**PUWeights**

- Automates calculation of PileUp weights for tuning MC pileup distribution to match data
- Resolves to path to pu weight file
- Should be used in conjunction with `RunJSON` and `InputFiles`


### Deferred Calls/References

The `DeferredCall` and `DeferredAttribute` are attempts to make classes transparent, by providing their referred value on non-class operations.
For example, `mon_mult = DeferredCall(lambda: (datetime.datetime.now().weekday() == 0) + 1)` can be used as `mon_mult * 2`, yielding `4` on mondays and `2` on any other day of the week.
An inherent restriction is that the deferred values are implicitly immutable.
Even if they can be modified (e.g. via `list.append`), a new, unmutated object will be created on the next resolving.

This is the dark domain of dabbling in python's inherent magic.
You shall probably not pass (yet, unless the tests worked out and cleanup has been done).
Ye have been warned.
