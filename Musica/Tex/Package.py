####################################################################################################
#
# Musica - A Music Theory Package for Python
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

class Package:

    ##############################################

    def __init__(self, name, *args, **kwargs):

        self._name = name
        self._options = {}

        for name in args:
            self.set(name)
        for name, value in kwargs.items():
            self.set(name, value)

    ##############################################

    def clone(self):

        obj = self.__class__(self._name)
        obj._options = dict(self._options)
        return obj

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def options(self):
        return self._options

    ##############################################

    def __contains__(self, name):

        return name in self._options

    ##############################################

    def __getitem__(self, name):

        return self._options[name]

    ##############################################

    def __setitem__(self, name, value):

        self.set_option(name, value)

    ##############################################

    def set(self, name, value=None):

        self._options[name] = value

    ##############################################

    def unset(self, name):

        del self._options[name]

    ##############################################

    def __eq__(self, other):

        return  self._name == other.__name__

    ##############################################

    def merge(self, other):

        if self == other:
            for name, value in other.options.items():
                self.set(name, value)

    ##############################################

    def __str__(self):

        options = []
        for name, value in sorted(self._options.items(), key=lambda x: x[0]):
            if value is not None:
                options.append('{}={}'.format(name, value))
            else:
                options.append(name)
        options = ', '.join(options)

        return r'\usepackage[{}]{{{}}}'.format(options, self._name)

####################################################################################################

class Packages:

    ##############################################

    def __init__(self):

        self._packages = {}

    ##############################################

    def clone(self):

        obj = self.__class__()
        obj._packages = {package.name:package.clone() for package in self._packages.values()}
        return obj

    ##############################################

    def __iter__(self):
        return iter(self._packages.values())

    ##############################################

    def __contains__(self, obj):

        if isinstance(obj, str):
            name = obj
        else:
            name = obj.name

        return name in self._packages

    ##############################################

    def add(self, package):

        if package in self:
            self._packages[package.name].merge(package)
        else:
            self._packages[package.name] = package

    ##############################################

    def merge(self, other):

        for package in other:
            self.add(package)
