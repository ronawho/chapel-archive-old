#!/usr/bin/env python

"""Simple script that effectively "greps" the runtime for calls to the system
allocator. Generally speaking, unless the memory layer hasn't been initialized,
or you need memory that isn't registered, the runtime should use the chapel
allocator, not the system one.

Finds all C/C++ files in the runtime, and uses cscope to check for calls to
system allocation/deallocation routines. Note that we don't check files that
are allowed to call the system allocator (sys alloc wrapper)"""

import fnmatch
import optparse
import os
import sys

chplenv_dir = os.path.join(os.path.dirname(__file__), '..', 'chplenv')
sys.path.insert(0, os.path.abspath(chplenv_dir))

from chpl_home_utils import get_chpl_home
from utils import run_command


def get_alloc_funcs():
    """Return a list of the possible C alloc/dealloc routines"""
    std = ['malloc', 'calloc', 'realloc', 'free']
    align = ['aligned_alloc', 'posix_memalign', 'memalign']
    page_align = ['valloc', 'pvalloc']
    string = ['strdup', 'strndup', 'asprintf', 'vasprintf']
    obscure = ['getline', 'getdelim']

    return std + align + page_align + string + obscure


def find_files(search_dir, extensions):
    """Return a list of absolute paths to files with any of the provided
       extensions in the search_dir."""
    source_files = []
    for root, _, filenames in os.walk(search_dir):
        for ext in extensions:
            for filename in fnmatch.filter(filenames, '*.{0}'.format(ext)):
                source_files.append(os.path.join(root, filename))
    return source_files


def find_source_files(search_dir):
    """Return a list of absolute paths to any C/C++ source files in
       the search_dir"""
    cpp_sources = ['cc', 'cp', 'cxx', 'cpp', 'CPP', 'c++', 'C']
    cpp_headers = ['hh', 'H', 'hp', 'hxx', 'hpp', 'HPP', 'h++', 'tcc']
    c_sources = ['c']
    c_headers = ['h']
    code_file_exts = set(cpp_sources + cpp_headers + c_sources + c_headers)
    return find_files(search_dir, code_file_exts)


def get_allowed_files():
    """Return a list of files that are allowed to call the system allocator"""
    # The system alloc wrapper is the only place that's allowed to directly
    # call the system allocator
    return ['chpl-mem-sys.h']


def get_non_allowed_files(search_dir):
    """Return a list of absolute paths to files that are not allowed to call
       the system allocator. i.e. source files in search_dir minus any files
       that end with an allowed file"""
    srcs = find_source_files(search_dir)
    for allowed_file in get_allowed_files():
        srcs = [s for s in srcs if not s.endswith(allowed_file)]
    return srcs


def build_cscope_ref(src_files):
    """Build a cscope cross-reference for crazy fast searching of src_files"""
    # -b -- build cross ref only
    # -q -- enable faster symbol lookup
    # -k -- turns off default include dir (don't include/parse system files
    #       since we only care if our files call the system allocator)
    cscope_cmd = ['cscope', '-b', '-q', '-k'] + src_files
    run_command(cscope_cmd)


def cscope_find_calls(func_call):
    """Run cscope searching for calls to func_call"""
    # -d  -- don't rebuild the cross-reference, use the one we already built
    # -L3 -- line based "Find functions calling this function"
    cscope_cmd = ['cscope', '-d', '-L3{0}'.format(func_call)]
    return run_command(cscope_cmd)


def check_for_alloc_calls(search_dir, rel_dir=''):
    """ Check src files in search_dir for calls to the system allocator. Report
        files relative to rel_dir.  Returns True if alloc calls were found,
        False otherwise"""
    src_files = get_non_allowed_files(search_dir)

    # TODO check that cscope is available
    # TODO check for errors in calls to cscope
    build_cscope_ref(src_files)

    found_alloc_calls = False
    for alloc_func in get_alloc_funcs():
        out = cscope_find_calls(alloc_func)
        if out:
            found_alloc_calls = True
            sys.stdout.write('Error: found "{0}" calls:\n'.format(alloc_func))
            sys.stdout.write(out.replace(rel_dir, '') + '\n')
    return found_alloc_calls


def main():
    """Determine chpl_home and check for alloc calls in chpl_home/runtime"""
    parser = optparse.OptionParser(description=__doc__)
    parser.add_option('--chpl_home', dest='chpl_home', default=get_chpl_home())
    options = parser.parse_args()[0]
    chpl_home = os.path.normpath(options.chpl_home)

    # TODO check that runtime dir exists
    # TODO print out number of runtime files that we check?
    runtime_dir = os.path.join(chpl_home, 'runtime')
    rel_dir = chpl_home + os.path.sep
    return check_for_alloc_calls(runtime_dir, rel_dir)


if __name__ == "__main__":
    exit(main())
