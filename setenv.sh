export Musica_source_path=${PWD}

source /opt/python-virtual-env/py36/bin/activate
append_to_python_path_if_not ${Musica_source_path}
append_to_python_path_if_not ${Musica_source_path}/tools
