'''TRender - Python template parser.

:copyright: 2016, Jeroen van der Heijden (Transceptor Technology)
:license: MIT
'''

from .trender import TRender
from .exceptions import (
    TRenderException,
    CompileException,
    RenderException,
    MacroOrBlockNotDefinedError,
    MacroOrBlockExistError,
    UnexpectedBlockError,
    UnexpectedEOFError,
    DefineBlockError,
    TemplateNotExistsError,
    MacroBlockUsageError)

__author__ = 'Jeroen van der Heijden'
__maintainer__ = 'Jeroen van der Heijden'
__email__ = 'jeroen@transceptor.technology'
__version__ = '1.0.7'
