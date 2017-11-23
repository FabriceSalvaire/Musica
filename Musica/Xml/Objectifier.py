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

class SourceCode:

    ##############################################

    def __init__(self, indentation=4):

        self._buffer = ''
        self._indentation = indentation
        self._level = 0

    ##############################################

    def increment_level(self):
        self._level += 1

    def decrement_level(self):
        self._level -= 1

    @property
    def indentation(self):
        return ' '*(self._indentation * self._level)

    ##############################################

    def __iter__(self):
        return iter(self._buffer.split('\n'))

    ##############################################

    def __str__(self):
        return self._buffer

    ##############################################

    def __iadd__(self, codes):

        self._buffer += codes
        return self

    ##############################################

    def append_line(self, codes):

        self._buffer += self.indentation + codes + '\n'

    ##############################################

    def append_lines(self, codes):

        for line in codes.split('\n'):
            self.append_line(line)

    ##############################################

    def close_block(self, decrement=False):

        if decrement:
            self.decrement_level()
        self.append_line(')')

####################################################################################################

class XmlObjectifierMetaclass(type):

    __classes__ = {}

    _logger = _module_logger.getChild('XmlObjectifierMetaclass')

    ##############################################

    def __new__(meta_cls, class_name, base_classes, namespace):

        print(meta_cls, class_name, base_classes, namespace)

        cls = super().__new__(meta_cls, class_name, base_classes, namespace)
        meta_cls.register(cls)

        return cls

    ##############################################

    def __init__(cls, class_name, base_classes, namespace):

        print(cls, class_name, base_classes, namespace)

        type.__init__(cls, class_name, base_classes, namespace)

    ##############################################

    @classmethod
    def register(meta_cls, cls):

        class_name = cls.__name__
        XmlObjectifierMetaclass._logger.info('Register {} for {}'.format(cls, class_name))
        meta_cls.__classes__[class_name] = cls

    ##############################################

    @classmethod
    def get(meta_cls, name):

        return meta_cls.__classes__[name]

####################################################################################################

class XmlObjectifierAbc(metaclass=XmlObjectifierMetaclass):

    _logger = _module_logger.getChild('XmlObjectifierAbc')

    __register_schema__ = False

    ##############################################

    @staticmethod
    def populate_class(namespace):

        namespace['__register_schema__'] = True
        # namespace['__id__'] = 0
        # we must instantiate here so as to update the class and not the base class
        namespace['__attribute_names__'] = set()
        namespace['__attribute_map__'] = {}

    ##############################################

    @classmethod
    def get_id(cls):

        if not hasattr(cls, '__id__'):
            cls.__id__ = 0

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

        class_name = cls.__name__
        base_class = cls.__mro__[1].__name__

        py_code = SourceCode()
        py_code.append_line('class {}({}):'.format(class_name, base_class))
        py_code.increment_level()

        py_code.append_line("__tag__ = '{}'".format(cls.__tag__))

        if cls.__attribute_names__:
            py_code.append_line('__attribute_names__ = (') # python name
            py_code.increment_level()
            for name in sorted(cls.__attribute_names__):
                py_code.append_line("'{}',".format(name))
            py_code.decrement_level()
            py_code.append_line(')')

        attribute_map = [(name, value)
                         for name, value in sorted(cls.__attribute_map__.items(), key=lambda x: x[0])
                         if name != value and name not in cls.__attribute_names__]
        if attribute_map:
            py_code.append_line('__attribute_map__ = {')
            py_code.increment_level()
            for name, value in attribute_map:
                py_code.append_line("'{}':'{}',".format(name, value))
            py_code.decrement_level()
            py_code.append_line('}')

        return py_code

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

        if self.__register_schema__:
            py_name = self.register_attribute(name)
            value = self.to_python_value(value)
            self._logger.info("{} {} = {} {}".format(self.__class__.__name__, name, value, type(value)))
        else:
            py_name = name

        setattr(self, py_name, value)

    ##############################################

    def attributes(self):

        _attrib = {name:getattr(self, name, None)
                  for name in self.__attribute_names__
                  if hasattr(self, name)}
        return {name:value for name, value in _attrib.items() if value is not None}

    ##############################################

    def to_dom(self):

        attributes = {self.__attribute_map__[name]:str(value)
                      for name, value in self.attributes().items()}
        return Element(self.__tag__, attributes)

    ##############################################

    def to_xml(self):

        return ElementTree.tostring(self.to_dom(), encoding='utf-8')

    ##############################################

    def attributes_to_python(self):

        kwarg = self.attributes()
        kwarg_string = ', '.join('{}={}'.format(name, self.value_to_python_code(value))
                                 for name, value in sorted(kwarg.items(), key=lambda x: x[0]))
        return kwarg_string

    ##############################################

    def depth_level(self):
        return 0

    ##############################################

    # def to_python(self, anonymous=False):
    #
    #     py_code = '{}({})'.format(self.class_name, self.attributes_to_python())
    #     if anonymous:
    #         return py_code
    #     else:
    #         return '{} = {}'.format(self.instance_id, py_code)

####################################################################################################

class XmlObjectifierNode(XmlObjectifierAbc):

    _logger = _module_logger.getChild('XmlObjectifierNode')

    __is_root__ = False

    ##############################################

    @staticmethod
    def populate_class(namespace):

        XmlObjectifierAbc.populate_class(namespace)
        # namespace['__is_root__'] = False
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

    @classmethod
    def is_container(cls):

        return cls.__child_names__ and not cls.__attribute_names__

    ##############################################

    # @classmethod
    # def _add_getter(cls, name):

    ##############################################

    @classmethod
    def class_to_python(cls):

        py_code = super().class_to_python()
        if cls.__is_root__:
            py_code.append_line('__is_root__ = True')
        py_code.append_line('__child_names__ = (')
        py_code.increment_level()
        for name in sorted(cls.__child_names__):
            py_code.append_line("'{}',".format(name))
        py_code.decrement_level()
        py_code.append_line(')')

        return py_code

    ##############################################

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs)
        self._childs = []
        self._child_map = {name:[] for name in self.__child_names__}

        for child in args:
            self.append(child)
        for child in kwargs.get('childs', ()):
            self.append(child)

    ##############################################

    def __iter__(self):

        return iter(self._childs)

    ##############################################

    def _get_child_by_name(self, name):

        return self._child_map[name]

    ##############################################

    def _append_child(self, child):

        self._childs.append(child)

        name = child.__class__.__name__
        if name not in self._child_map:
            self._child_map[name] = []
        self._child_map[name].append(child)

        if self.__register_schema__:
            self.register_child(name)

    ##############################################

    def append(self, *childs):

        for child in childs:
            self._append_child(child)

    ##############################################

    def childs_are_leaf(self):

        for cls_name in self._child_map.keys():
            if issubclass(XmlObjectifierMetaclass.get(cls_name), XmlObjectifierNode):
                return False
        return True

    ##############################################

    def depth_level(self):

        depth_level = 0
        for child in self._childs:
            depth_level = max(depth_level, child.depth_level() +1)
        return depth_level

    ##############################################

    def to_dom(self):

        element = super().to_dom()
        for child in self._childs:
            element.append(child.to_dom())

        return element

    ##############################################

    def to_python(self, anonymous=False):

        # py_code = super().to_python()

        py_code = SourceCode()
        if not anonymous:
            py_code += self.instance_id + ' = '
        py_code += self.class_name + '('
        attributes = self.attributes_to_python()
        if attributes:
            py_code += attributes

        if self.depth_level() < 4: # self.childs_are_leaf()
            if attributes:
                py_code += ','
            py_code += '\n'
            py_code.increment_level()
            if attributes:  # not self.is_container
                py_code.append_line('childs=(')
                py_code.increment_level()
            for child in self._childs:
                py_code.append_lines(child.to_python(True).rstrip() + ',')
            if attributes:
                py_code.close_block(decrement=True)
            py_code.close_block(decrement=True)
        else:
            py_code.close_block()
            template = '{}.append({})\n'
            for child in self._childs:
                if isinstance(child, XmlObjectifierLeaf):
                    py_code += template.format(self.instance_id, child.to_python(True))
                else:
                    py_code += child.to_python()
                    py_code += template.format(self.instance_id, child.instance_id)

        return str(py_code)

    ##############################################

    def to_tree(self):

        return ElementTree.ElementTree(self.to_dom())

    ##############################################

    def write_xml(self, path, doctype=None):

        dom = self.to_tree()

        with open(path, 'wb') as fh:
            fh.write('<?xml version="1.0" encoding="UTF-8"?>'.encode('utf-8'))
            if doctype is not None:
                fh.write(doctype.encode('utf-8'))
            dom.write(fh, encoding='utf-8', xml_declaration=False)

        # dom.write(path, encoding='utf-8', xml_declaration=True)

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
            text = str(self._text)
            if text:
                element.text = text

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

        py_code = '{}({})'.format(self.class_name, ', '.join(args))

        if anonymous:
            return py_code
        else:
            return '{} = {}\n'.format(self.instance_id, py_code)

####################################################################################################

class XmlObjectifierFactory:

    _logger = _module_logger.getChild('XmlObjectifierFactory')

    ##############################################

    def __init__(self, doctype=None, node_hints=()):

        self._doctype = doctype
        self._node_hints = tuple(node_hints)

        self._classes = {}
        self._root_cls = None

    ##############################################

    def _get_classe(self, element):

        name = element.tag
        class_name = ''.join([part.title() for part in name.split('-')])
        if class_name not in self._classes:
            is_node = len(element) > 0
            cls = self._build_class(class_name, name, is_node)
        else:
            cls = self._classes[class_name]

        return cls

    ##############################################

    def _build_class(self, class_name, name, is_node):

        # Fixme:
        # if element.text is not None:

        if is_node or class_name in self._node_hints:
            base_class = XmlObjectifierNode
        else:
            base_class = XmlObjectifierLeaf

        self._logger.info('Create class {} {}'.format(class_name, base_class))

        cls = types.new_class(
            class_name,
            bases=(base_class,),
            kwds=None,
            exec_body=XmlObjectifierNode.populate_class
        )
        cls.__tag__ = name

        self._classes[class_name] = cls

        if self._root_cls is None:
            self._root_cls = cls
            cls.__is_root__ = True

        return cls

    ##############################################

    def _cast_to_node(self, py_element):

        # Fixme: hack !
        #  old element are not recasted !!!

        cls = py_element.__class__
        class_name = cls.__name__
        self._logger.warning('{} must be reacasted to Node'.format(class_name))
        del self._classes[class_name]

        new_cls = self._build_class(class_name, cls.__tag__, True)
        new_cls.__attribute_names__ = cls.__attribute_names__
        new_cls.__attribute_map__ = cls.__attribute_map__

        return new_cls(** py_element.attributes())

    ##############################################

    def __getitem__(self, element):

        return self._get_classe(element)

    ##############################################

    def __iter__(self):
        return iter(self._classes.values())

    ##############################################

    def parse(self, file_path):

        tree = ElementTree.parse(file_path)
        root = tree.getroot()

        return self._process_element(root)

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
            if not hasattr(py_element, 'append'):
                py_element = self._cast_to_node(py_element)
            py_element.append(py_subelement)

        return py_element
