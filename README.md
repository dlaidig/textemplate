<!--
SPDX-FileCopyrightText: 2022 Daniel Laidig <daniel@laidig.info>

SPDX-License-Identifier: MIT
-->
# textemplate

Simple tool to render LaTeX templates from json/yaml data

~~~
usage: textemplate [-h] [-p] [-v] [--multi-output] [-o OUT] template data [data ...]

LaTeX template renderer.

positional arguments:
  template           name of the .tex template file
  data               name of the .yaml/.json data files (use "variable::filename" to make the file data available in a specific variable)

options:
  -h, --help         show this help message and exit
  -p, --pdf          create PDFs
  -v, --verbose      enable verbose mode (print parsed data)
  --multi-output     generate multiple output files based on the outputFiles entry in the data
  -o OUT, --out OUT  output filename (default: derived from the last data filename)
~~~
