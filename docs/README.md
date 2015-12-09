# Available Topics

## Configuration

### Configs and Config Modifiers

See [config_format.md](config_format.md)

### Config Classes

Several classes are available to use in place of regular configuration. E.g. the JSON file for run can be set as a list of paths (`cfg['JsonFiles']=["path/to/json.txt"]`) or via the RunJSON (`cfg['JsonFiles']=RunJSON("path/to/json.txt"])`).

See [config_classes.md](config_classes.md)

### Caching

Several configuration utilities implicitly cache queries and external resources. This will significantly speed up calculations and calls, but any cache may become stale, dirty or corrupted.

See [config_caches.md](config_caches.md)


## Testing

### Travis

Travis runs automatic tests for every commit. This will validate whether the Artus and Excalibur build and run correctly.

See the [Travis Excalibur builds](https://travis-ci.org/artus-analysis/Excalibur/builds).