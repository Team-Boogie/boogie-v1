"""
This type stub file was generated by pyright.
"""

from ..utils import PostProcessingError

class PostProcessorMetaClass(type):
    @staticmethod
    def run_wrapper(func): # -> _Wrapped[..., Unknown, (self: Unknown, info: Unknown, *args: Unknown, **kwargs: Unknown), Unknown]:
        ...
    
    def __new__(cls, name, bases, attrs): # -> Self@PostProcessorMetaClass:
        ...
    


class PostProcessor(metaclass=PostProcessorMetaClass):
    """Post Processor class.

    PostProcessor objects can be added to downloaders with their
    add_post_processor() method. When the downloader has finished a
    successful download, it will take its internal chain of PostProcessors
    and start calling the run() method on each one of them, first with
    an initial argument and then with the returned value of the previous
    PostProcessor.

    PostProcessor objects follow a "mutual registration" process similar
    to InfoExtractor objects.

    Optionally PostProcessor can use a list of additional command-line arguments
    with self._configuration_args.
    """
    _downloader = ...
    def __init__(self, downloader=...) -> None:
        ...
    
    @classmethod
    def pp_key(cls): # -> str:
        ...
    
    def to_screen(self, text, prefix=..., *args, **kwargs): # -> None:
        ...
    
    def report_warning(self, text, *args, **kwargs): # -> None:
        ...
    
    def deprecation_warning(self, msg): # -> Any | None:
        ...
    
    def deprecated_feature(self, msg): # -> None:
        ...
    
    def report_error(self, text, *args, **kwargs): # -> None:
        ...
    
    def write_debug(self, text, *args, **kwargs): # -> None:
        ...
    
    def get_param(self, name, default=..., *args, **kwargs): # -> None:
        ...
    
    def set_downloader(self, downloader): # -> None:
        """Sets the downloader for this PP."""
        ...
    
    def run(self, information): # -> tuple[list[Unknown], Unknown]:
        """Run the PostProcessor.

        The "information" argument is a dictionary like the ones
        composed by InfoExtractors. The only difference is that this
        one has an extra field called "filepath" that points to the
        downloaded file.

        This method returns a tuple, the first element is a list of the files
        that can be deleted, and the second of which is the updated
        information.

        In addition, this method may raise a PostProcessingError
        exception if post processing fails.
        """
        ...
    
    def try_utime(self, path, atime, mtime, errnote=...): # -> None:
        ...
    
    def add_progress_hook(self, ph): # -> None:
        ...
    
    def report_progress(self, s): # -> None:
        ...
    


class AudioConversionError(PostProcessingError):
    ...


