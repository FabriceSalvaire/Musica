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

# Fixme:
#   improve formater
#   code dumper, register class

####################################################################################################

import logging
import types
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

__all__ = [
    'XmlObjectifierFactory',
    'XmlObjectifierLeaf',
    'XmlObjectifierNode',
    ]

####################################################################################################

class XmlObjectifierAbc:

    _logger = _module_logger.getChild('XmlObjectifierAbc')

    ##############################################

    @staticmethod
    def populate_class(namespace):

        namespace['__id__'] = 0
        namespace['__attribute_names__'] = set()
        namespace['__attribute_map__'] = {}

    ##############################################

    @classmethod
    def get_id(cls):

        _id = cls.__id__
        cls.__id__ += 1
        # name = cls.__name__.lower()
        name = cls.pythonify_name(cls.__tag__) # Fixme: cache
        return '{}_{}'.format(name, _id)

    ##############################################

    @classmethod
    def register_attribute(cls, name):

        py_name = cls.pythonify_name(name)
        cls.__attribute_names__.add(py_name)
        cls.__attribute_map__[name] = py_name
        cls.__attribute_map__[py_name] = name
        return py_name

    ##############################################

    @classmethod
    def class_to_python(cls):

        py_code = '''
class {}({}):
    __tag__ = '{}'
    __id__ = 0
    __attribute_names__ = {}
    __attribute_map__ = {}
'''
        return py_code.rstrip().format(
            cls.__name__,
            cls.__mro__[1].__name__,
            cls.__tag__,
            '{' + ', '.join("'{}'".format(name) for name in cls.__attribute_names__) + '}',
            '{' + ', '.join(["'{}':'{}'".format(name, value) for name, value in cls.__attribute_map__.items()]) + '}',
        )

    ##############################################

    @staticmethod
    def pythonify_name(name):

        return name.replace('-', '_')

    ##############################################

    @staticmethod
    def to_python_value(value):

        if isinstance(value, str):
            try:
                if '.' in value or 'e' in value.lower():
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return value
        else:
            return value

    ##############################################

    @staticmethod
    def value_to_python_code(value):

        py_code = str(value)
        if not isinstance(value, (int, float)):
            py_code = "'" + py_code + "'"
        return py_code

    ##############################################

    def __init__(self, **kwargs):

        self._id = self.get_id()

        for name, value in kwargs.items():
            self.set_attribute(name, value)

    ##############################################

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def instance_id(self):
        return self._id

    ##############################################

    def __repr__(self):

        return '{} {}'.format(self.__class__.__name__, self.instance_id)

    ##############################################

    def set_attribute(self, name, value):

        py_name = self.register_attribute(name)

        value = self.to_python_value(value)
        self._logger.info("{} {} = {} {}".format(self.__class__.__name__, name, value, type(value)))

        setattr(self, py_name, value)

    ##############################################

    def _attributes(self):

        _attrib = {name:getattr(self, name, None)
                  for name in self.__attribute_names__
                  if hasattr(self, name)}
        return {name:value for name, value in _attrib.items() if value is not None}

    ##############################################

    def to_dom(self):

        attributes = {self.__attribute_map__[name]:str(value)
                      for name, value in self._attributes().items()}
        return Element(self.__tag__, attributes)

    ##############################################

    def to_xml(self):

        return ElementTree.tostring(self.to_dom(), encoding='utf-8')

    ##############################################

    def attributes_to_python(self):

        kwarg = self._attributes()
        kwarg_string = ', '.join('{}={}'.format(name, self.value_to_python_code(value))
                                 for name, value in sorted(kwarg.items(), key=lambda x: x[0]))
        return kwarg_string

    ##############################################

    def to_python(self, anonymous=False):

        return '{} = {}({})\n'.format(self.instance_id, self.class_name, self.attributes_to_python())

####################################################################################################

class XmlObjectifierNode(XmlObjectifierAbc):

    _logger = _module_logger.getChild('XmlObjectifierNode')

    ##############################################

    @staticmethod
    def populate_class(namespace):

        XmlObjectifierAbc.populate_class(namespace)
        namespace['__child_names__'] = set()

    ##############################################

    @classmethod
    def register_child(cls, name):

        if name not in cls.__child_names__:
            cls.__child_names__.add(name)
            # cls._add_getter(name)
            # Fixme: getter name
            setattr(cls, name, property(lambda self: self._get_child_by_name(name)))

    ##############################################

    # @classmethod
    # def _add_getter(cls, name):

    ##############################################

    @classmethod
    def class_to_python(cls):

        py_code = super().class_to_python()
        _py_code = '''
    __child_names__ = {}
'''

        return py_code + _py_code.rstrip().format(
            '{' + ', '.join("'{}'".format(name) for name in cls.__child_names__) + '}',
        )

    ##############################################

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self._childs = []
        self._child_map = {name:[] for name in self.__child_names__}

    ##############################################

    def __iter__(self):

        return iter(self._childs)

    ##############################################

    def _get_child_by_name(self, name):

        return self._child_map[name]

    ##############################################

    def append(self, child):

        name = child.__class__.__name__
        if name not in self._child_map:
            self.register_child(name)
            self._child_map[name] = []

        self._childs.append(child)
        self._child_map[name].append(child)

    ##############################################

    def to_dom(self):

        element = super().to_dom()
        for child in self._childs:
            element.append(child.to_dom())

        return element

    ##############################################

    def to_python(self, anonymous=False):

        py_code = super().to_python()
        for child in self._childs:
            if isinstance(child, XmlObjectifierLeaf):
                py_code += '{}.append({})\n'.format(self.instance_id, child.to_python(True))
            else:
                py_code += child.to_python()
                py_code += '{}.append({})\n'.format(self.instance_id, child.instance_id)
        return py_code

####################################################################################################

class XmlObjectifierLeaf(XmlObjectifierAbc):

    _logger = _module_logger.getChild('XmlObjectifierLeaf')

    ##############################################

    @staticmethod
    def populate_class(namespace):

        XmlObjectifierAbc.populate_class(namespace)

    ##############################################

    def __init__(self, text=None, **kwargs):

        super().__init__(**kwargs)
        self._text = text

    ##############################################

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    ##############################################

    def to_dom(self):

        element = super().to_dom()
        if self._text is not None:
            element.text = str(self._text)

        return element

    ##############################################

    def to_python(self, anonymous=False):

        # py_code = super().to_python()

        args = []
        if self._text is not None:
            text = str(self._text)
            if not isinstance(self._text, (int, float)):
                text = "'" + text + "'"
            # py_code += '{}.text = {}\n'.format(self.instance_id, text)
            args.append(text)

        attributes = self.attributes_to_python()
        if attributes:
            args.append(attributes)

        py_source = '{}({})'.format(self.class_name, ', '.join(args))

        if anonymous:
            return py_source
        else:
            return '{} = {}\n'.format(self.instance_id, py_source)

####################################################################################################

class XmlObjectifierFactory:

    _logger = _module_logger.getChild('XmlObjectifierFactory')

    ##############################################

    def __init__(self):

        self._classes = {}

    ##############################################

    def parse(self, file_path):

        tree = ElementTree.parse(file_path)
        root = tree.getroot()

        return self._process_element(root)

    ##############################################

    def _get_classe(self, element):

        name = element.tag
        py_name = ''.join([part.title() for part in name.split('-')])
        if py_name not in self._classes:
            # Fixme:
            # if element.text is not None:
            if len(element):
                base_class = XmlObjectifierNode
            else:
                base_class = XmlObjectifierLeaf
            self._logger.info('Create class {} {}'.format(py_name, base_class))
            cls = types.new_class(py_name,
                                  bases=(base_class,),
                                  kwds=None,
                                  exec_body=XmlObjectifierNode.populate_class)
            cls.__tag__ = name
            self._classes[py_name] = cls
        else:
            cls = self._classes[py_name]

        return cls

    ##############################################

    def __getitem__(self, element):

        return self._get_classe(element)

    ##############################################

    def __iter__(self):
        return iter(self._classes.values())

    ##############################################

    def _process_element(self, element):

        self._logger.info('{0.tag} {0.text}'.format(element))

        element_cls = self[element]
        py_element = element_cls()
        for name, value in element.attrib.items():
            py_element.set_attribute(name, value)
        if element.text is not None:
            py_element.text = XmlObjectifierAbc.to_python_value(element.text)
        for subelement in element:
            py_subelement = self._process_element(subelement)
            py_element.append(py_subelement)

        return py_element
