import sys, pathlib

__cwd__ = pathlib.Path(__file__).parents[3] / 'tools' / 'plantuml'
print(__cwd__)
sys.path.append(str(__cwd__))

from plantuml_generator import create_uml_diagram

path_folder = str(pathlib.Path(__file__).parents[0].as_posix())
create_uml_diagram(f'{path_folder}/xlh_ha.txt')
