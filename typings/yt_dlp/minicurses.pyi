"""
This type stub file was generated by pyright.
"""

CONTROL_SEQUENCES = ...
_COLORS = ...
_TEXT_STYLES = ...
def format_text(text, f): # -> str:
    '''
    @param f    String representation of formatting to apply in the form:
                [style] [light] font_color [on [light] bg_color]
                E.g. "red", "bold green on light blue"
    '''
    ...

class MultilinePrinterBase:
    def __init__(self, stream=..., lines=...) -> None:
        ...
    
    def __enter__(self): # -> Self@MultilinePrinterBase:
        ...
    
    def __exit__(self, *args): # -> None:
        ...
    
    def print_at_line(self, text, pos): # -> None:
        ...
    
    def end(self): # -> None:
        ...
    
    def write(self, *text): # -> None:
        ...
    


class QuietMultilinePrinter(MultilinePrinterBase):
    ...


class MultilineLogger(MultilinePrinterBase):
    def write(self, *text): # -> None:
        ...
    
    def print_at_line(self, text, pos): # -> None:
        ...
    


class BreaklineStatusPrinter(MultilinePrinterBase):
    def print_at_line(self, text, pos): # -> None:
        ...
    


class MultilinePrinter(MultilinePrinterBase):
    def __init__(self, stream=..., lines=..., preserve_output=...) -> None:
        ...
    
    def lock(func): # -> _Wrapped[..., Unknown, (self: Unknown, *args: Unknown, **kwargs: Unknown), Unknown]:
        ...
    
    @lock
    def print_at_line(self, text, pos): # -> None:
        ...
    
    @lock
    def end(self): # -> None:
        ...
    


