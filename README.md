# Python CLI Template
Template main purpose is for single file cli capable Python code with minimal imports. As such templates line count was kept as small as possible, but still loosely abides Python style guidelines.

## Usage
General usage example is provided in Template (`template.py`)

### `Commands` dictionary arguments
- First layer key is used to identify command. Key acts as command name. Value must be of type `dictionary`.
 - Second layer consists of these keys:
   - `function` - Function that will be called when specified command is called from cli
   - `comment` - `string` comment  that will be printed when `-h` | `--help` is called
   - `variables` | `toggle` - `dictionary`. `variables` dictionary gets value assigned to it. `toggle` is bool type values:
     - Third layer is for declaring passable variables, other arguments. `dictionary` key is used to identify parameter name.
	   - `arg_offset` - `int` specifies how far out value will be selected
	   - `call` - `list` specifies properties that can be found anywhere in command
	   - `name` - `string` name for property that will be printed when `-h` | `--help` is called
	   - `comment` - `string` comment  that will be printed when `-h` | `--help` is called

### Creating and using functions
When creating functions two variables must be passed:
- Argument array (created from sys.argv) as first value;
- Parsed argument `dictionary` as second value.

Parsed argument `dictionary` follows similar data layout to `commands` dictionary.
First layer keys:
```python
{'variables': {}, 'toggle':{}}
```
Second layer keys depend on user set variables and toggles.
