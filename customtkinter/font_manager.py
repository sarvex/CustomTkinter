import sys
import os
import shutil
from typing import Union


class FontManager:

    @classmethod
    def init_font_manager(cls):
        if not sys.platform.startswith("linux"):
            return True
        try:
            if not os.path.isdir(os.path.expanduser('~/.fonts/')):
                os.mkdir(os.path.expanduser('~/.fonts/'))
            return True
        except Exception as err:
            sys.stderr.write(f"FontManager error: {str(err)}" + "\n")
            return False

    @classmethod
    def windows_load_font(cls, font_path: Union[str, bytes], private: bool = True, enumerable: bool = False) -> bool:
        """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

        from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20

        if isinstance(font_path, bytes):
            path_buffer = create_string_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExA
        elif isinstance(font_path, str):
            path_buffer = create_unicode_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('font_path must be of type bytes or str')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        return bool(num_fonts_added)

    @classmethod
    def load_font(cls, font_path: str) -> bool:
        # Windows
        if sys.platform.startswith("win"):
            return cls.windows_load_font(font_path, private=True, enumerable=False)

        elif sys.platform.startswith("linux"):
            try:
                shutil.copy(font_path, os.path.expanduser("~/.fonts/"))
                return True
            except Exception as err:
                sys.stderr.write(f"FontManager error: {str(err)}" + "\n")
                return False

        else:
            return False
