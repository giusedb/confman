# Configuration Manager for Python apps

## Configuration made easy

## Usage and command line

```shell
$ myapp --help

Usage: myapp [OPTIONS] COMMAND [ARGS]...

Options:
  -C, --conf-dir TEXT  configuration directory: [~/.config/dbtools]
  --help               Show this message and exit.

Commands:
  config  Read or modify configuration files.
  ...
  ...
```

### Get configs on the spot 


```shell
Usage: myapp config [OPTIONS] COMMAND [ARGS]...

  Read or modify configuration files.

Options:
  --help  Show this message and exit.

Commands:
  get   Print out configuration information.
  load  Load a full configuration storage from `path_to_json` file.
  set   Set a single value on a configuration storage
```

