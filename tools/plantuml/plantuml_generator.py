# Plantuml
# https://plantuml.com/de/state-diagram
# https://real-world-plantuml.com/
# https://dev.to/sakko/how-i-code-not-draw-my-er-diagram-4kc3
# https://nevets.github.io/2019/06/03/plantuml/
# https://plantuml.com/de-dark/ie-diagram
# https://plantuml.com/de/skinparam
# https://plantuml-documentation.readthedocs.io/en/latest/formatting/all-skin-params.html
# https://plantuml.com/es/class-diagram
# https://plantuml.com/command-line


import pathlib
import subprocess
import sys



def create_uml_diagram(path_puml_file: str):
    path_jar = str(pathlib.Path(__file__).parents[0].as_posix())
    program_with_args = [
        'java', '-jar',
        f'{path_jar}/plantuml-gplv2-1.2025.10.jar',
        f'{path_puml_file}',
        '-charset', 'UTF-8',
        '-png']

    print(program_with_args)

    if sys.platform == 'linux':
        process = subprocess.Popen(
            program_with_args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.communicate()
        print(result)

    else:
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.Popen(
            program_with_args,
            creationflags=CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.communicate()
        print(result)
