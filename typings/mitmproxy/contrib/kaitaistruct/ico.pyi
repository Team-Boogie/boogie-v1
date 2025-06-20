"""
This type stub file was generated by pyright.
"""

import kaitaistruct
from kaitaistruct import KaitaiStruct

if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    ...
class Ico(KaitaiStruct):
    """Microsoft Windows uses specific file format to store applications
    icons - ICO. This is a container that contains one or more image
    files (effectively, DIB parts of BMP files or full PNG files are
    contained inside).
    
    .. seealso::
       Source - https://docs.microsoft.com/en-us/previous-versions/ms997538(v=msdn.10)
    """
    def __init__(self, _io, _parent=..., _root=...) -> None:
        ...
    
    class IconDirEntry(KaitaiStruct):
        def __init__(self, _io, _parent=..., _root=...) -> None:
            ...
        
        @property
        def img(self): # -> Any | None:
            """Raw image data. Use `is_png` to determine whether this is an
            embedded PNG file (true) or a DIB bitmap (false) and call a
            relevant parser, if needed to parse image data further.
            """
            ...
        
        @property
        def png_header(self): # -> Any | None:
            """Pre-reads first 8 bytes of the image to determine if it's an
            embedded PNG file.
            """
            ...
        
        @property
        def is_png(self): # -> Any | None:
            """True if this image is in PNG format."""
            ...
        
    
    


