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

from struct import *

####################################################################################################

# [Bloc de déclaration d'un fichier au format WAVE]
#    FileTypeBlocID  (4 octets) : Constante «RIFF»  (0x52,0x49,0x46,0x46)
#    FileSize        (4 octets) : Taille du fichier moins 8 octets
#    FileFormatID    (4 octets) : Format = «WAVE»  (0x57,0x41,0x56,0x45)
#
# [Bloc décrivant le format audio]
#    FormatBlocID    (4 octets) : Identifiant «fmt »  (0x66,0x6D, 0x74,0x20)
#    BlocSize        (4 octets) : Nombre d'octets du bloc - 16  (0x10)
#
#    AudioFormat     (2 octets) : Format du stockage dans le fichier (1: PCM, ...)
#    NbrCanaux       (2 octets) : Nombre de canaux (de 1 à 6, cf. ci-dessous)
#    Frequence       (4 octets) : Fréquence d'échantillonnage (en hertz) [Valeurs standardisées : 11025, 22050, 44100 et éventuellement 48000 et 96000]
#    BytePerSec      (4 octets) : Nombre d'octets à lire par seconde (c.-à-d., Frequence * BytePerBloc).
#    BytePerBloc     (2 octets) : Nombre d'octets par bloc d'échantillonnage (c.-à-d., tous canaux confondus : NbrCanaux * BitsPerSample/8).
#    BitsPerSample   (2 octets) : Nombre de bits utilisés pour le codage de chaque échantillon (8, 16, 24)
#
# [Bloc des données]
#    DataBlocID      (4 octets) : Constante «data»  (0x64,0x61,0x74,0x61)
#    DataSize        (4 octets) : Nombre d'octets des données (c.-à-d. "Data[]", c.-à-d. taille_du_fichier - taille_de_l'entête  (qui fait 44 octets normalement).
#    DATAS[] : [Octets du Sample 1 du Canal 1] [Octets du Sample 1 du Canal 2] [Octets du Sample 2 du Canal 1] [Octets du Sample 2 du Canal 2]
#
#    * Les Canaux :
#       1 pour mono,
#       2 pour stéréo
#       3 pour gauche, droit et centre
#       4 pour face gauche, face droit, arrière gauche, arrière droit
#       5 pour gauche, centre, droit, surround (ambiant)
#       6 pour centre gauche, gauche, centre, centre droit, droit, surround (ambiant)

# NOTES IMPORTANTES :  Les octets des mots sont stockés sous la forme  (c.-à-d., en "little endian")
# [87654321][16..9][24..17] [8..1][16..9][24..17] [...

####################################################################################################

def read_str(stream, size):
    return stream.read(size).decode('ascii')

def read_int4(stream):
    # little-endian
    return unpack('<i', stream.read(4))[0]

def read_int2(stream):
    return unpack('<h', stream.read(2))[0]

####################################################################################################

# short-pulse.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz
path = 'short-pulse.wav'

# RIFF 35316 WAVE
# fmt  16
# 1 2 44100 16
# 4 = 4
# 176400 = 176400
# data
# 35280 = 35280 44
# 0 0
# 3 3
# 12 12
# 27 27
# 48 48
# 72 72
# 100 100
# 131 131
# 162 162
# 192 192

with open(path, 'rb') as f:

    # [Bloc de déclaration d'un fichier au format WAVE]
    FileTypeBlocID  = read_str(f, 4) # Constante «RIFF»  (0x52,0x49,0x46,0x46)
    FileSize        = read_int4(f)   # Taille du fichier moins 8 octets
    FileFormatID    = read_str(f, 4) # Format = «WAVE»  (0x57,0x41,0x56,0x45)
    print(FileTypeBlocID)
    print(FileSize, '/', FileSize + 8)
    print(FileFormatID)

    # [Bloc décrivant le format audio]
    FormatBlocID    = read_str(f, 4) # Identifiant «fmt »  (0x66,0x6D, 0x74,0x20)
    BlocSize        = read_int4(f)   # Nombre d'octets du bloc - 16  (0x10)
    print(FormatBlocID)
    print(BlocSize, '=', 16)

    AudioFormat     = read_int2(f)   # Format du stockage dans le fichier (1: PCM, ...)
    NbrCanaux       = read_int2(f)   # Nombre de canaux (de 1 à 6, cf. ci-dessous)
    Frequence       = read_int4(f)   # Fréquence d'échantillonnage (en hertz) [Valeurs standardisées : 11025, 22050, 44100 et éventuellement 48000 et 96000]
    BytePerSec      = read_int4(f)   # Nombre d'octets à lire par seconde (c.-à-d., Frequence * BytePerBloc).
    BytePerBloc     = read_int2(f)   # Nombre d'octets par bloc d'échantillonnage (c.-à-d., tous canaux confondus : NbrCanaux * BitsPerSample/8).
    BitsPerSample   = read_int2(f)   # Nombre de bits utilisés pour le codage de chaque échantillon (8, 16, 24)
    print(AudioFormat, NbrCanaux, Frequence, BitsPerSample)
    print(BytePerBloc, '=', NbrCanaux * BitsPerSample // 8)
    print(BytePerSec, '=', Frequence * BytePerBloc)

    # [Bloc des données]
    DataBlocID     = read_str(f, 4)  # Constante «data»  (0x64,0x61,0x74,0x61)
    DataSize       = read_int4(f)    # Nombre d'octets des données (c.-à-d. "Data[]", c.-à-d. taille_du_fichier - taille_de_l'entête  (qui fait 44 octets normalement).
    print(DataBlocID)
    header_size = 4*3 + 4*2 + 2*4 + 4*2 + 4*2
    print(DataSize, '=', FileSize + 8 - header_size, header_size)

    for i in range(10):
        print(read_int2(f), read_int2(f))
