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

__all__ = [
    'gettext',
    ]

####################################################################################################

import logging
import gettext as _gettext
import os

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# https://docs.python.org/3/library/gettext.html
# http://babel.pocoo.org/en/latest/index.html
# https://www.mattlayman.com/2015/i18n.html

####################################################################################################

_module_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
_locale_path = os.path.join(_module_path, 'locale')
# _module_logger.info('Install locale from {}'.format(_locale_path))

_translations = {}

####################################################################################################

def load_translation(language=None):

    if language in _translations:
        return _translations[language]
    else:
        if language is not None:
            languages = [language]
        else:
            languages = None

        translation = _gettext.translation('Musica', localedir=_locale_path, languages=languages)
        _translations[language] = translation

        return translation

####################################################################################################

def translate(message, language=None):

    translation = load_translation(language)
    return translation.gettext(message)

####################################################################################################

translation = load_translation()
gettext = translation.gettext
# _ = gettext
