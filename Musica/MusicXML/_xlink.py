# ./_xlink.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:b43cd366527ddb6a0e58594876e07421e0148f30
# Generated 2017-10-09 18:48:41.313719 by PyXB version 1.2.6 using Python 3.6.2.final.0
# Namespace http://www.w3.org/1999/xlink [xmlns:xlink]

from __future__ import unicode_literals
import pyxb
from pyxb.binding.datatypes import positiveInteger as p_positiveInteger
from pyxb.binding.basis import complexTypeDefinition as p_complexTypeDefinition
from pyxb.binding.basis import element as p_element
from pyxb.binding.basis import enumeration_mixin as p_enumeration_mixin
from pyxb.binding.content import AttributeUse as p_AttributeUse
from pyxb.binding.content import ElementDeclaration as p_ElementDeclaration
from pyxb.binding.content import ElementUse as p_ElementUse
from pyxb.binding.datatypes import ID as p_ID
from pyxb.binding.datatypes import IDREF as p_IDREF
from pyxb.binding.datatypes import NMTOKEN as p_NMTOKEN
from pyxb.binding.datatypes import anySimpleType as p_anySimpleType
from pyxb.binding.datatypes import anyType as p_anyType
from pyxb.binding.datatypes import decimal as p_decimal
from pyxb.binding.datatypes import integer as p_integer
from pyxb.binding.datatypes import nonNegativeInteger as p_nonNegativeInteger
from pyxb.binding.datatypes import string as p_string
from pyxb.binding.datatypes import token as p_token
from pyxb.binding.facets import CF_enumeration as p_CF_enumeration
from pyxb.binding.facets import CF_maxInclusive as p_CF_maxInclusive
from pyxb.binding.facets import CF_minExclusive as p_CF_minExclusive
from pyxb.binding.facets import CF_minInclusive as p_CF_minInclusive
from pyxb.namespace import ExpandedName as p_ExpandedName
from pyxb.utils.utility import Location as p_Location
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:b41e9400-ad11-11e7-be22-185e0f77ec0a')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3.org/1999/xlink', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return p_element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (p_NMTOKEN, p_enumeration_mixin):


    _ExpandedName = None
    _XSDLocation = p_Location('xlink.xsd', 23, 2)
    _Documentation = ''
STD_ANON._CF_enumeration = p_CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.simple = STD_ANON._CF_enumeration.addEnumeration(unicode_value='simple', tag='simple')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (p_NMTOKEN, p_enumeration_mixin):


    _ExpandedName = None
    _XSDLocation = p_Location('xlink.xsd', 35, 2)
    _Documentation = ''
STD_ANON_._CF_enumeration = p_CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.new = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='new', tag='new')
STD_ANON_.replace = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='replace', tag='replace')
STD_ANON_.embed = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='embed', tag='embed')
STD_ANON_.other = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON_.none = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (p_NMTOKEN, p_enumeration_mixin):


    _ExpandedName = None
    _XSDLocation = p_Location('xlink.xsd', 47, 2)
    _Documentation = ''
STD_ANON_2._CF_enumeration = p_CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.onRequest = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='onRequest', tag='onRequest')
STD_ANON_2.onLoad = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='onLoad', tag='onLoad')
STD_ANON_2.other = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON_2.none = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)
_module_typeBindings.STD_ANON_2 = STD_ANON_2
