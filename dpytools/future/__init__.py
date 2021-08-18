"""
This submodule is under active development
It should be considered unsuited for production and downright unstable
When it's ready for production the contents of this module will be transferred to the main level of the module.

Rules for migration will be as follows:
    If a file or folder shares a name with one present at module level it will be replaced
    if a file or folder starts with a lower dash ("_") it means this file will be deleted at module level
    If a file or folder is not present in the module then no changes will be made

The contents of this submodule will be developed for the 2.0 version of discord.py
"""
import utils
import react_menus
import menu_views
