####################################################################################################
#
# How to Start
#
####################################################################################################

# Set the environment
. setenv.sh

# Build
python setup.py build

# Generate Documentation
. tools/generate-rst-api.sh
. tools/generate-rst-examples.sh
