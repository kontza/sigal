# -*- coding: utf-8 -*-

# Copyright (c)      2015 - Juha Ruotsalainen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""Plugin which replaces certain characters in album names.

Rules for conversion are specified in sigal.conf.py -file in
an array of tuples by the name of 'album_title_mangler'. E.g.

album_title_mangler = [('__','-'),('_',' ')]

This example will first convert all double underscores into a single dash,
then convert all single underscores into a single space. You can add
as many tuples as you want, just remember: the order is important,
mangling rules are processed in first-come-first-serve -order.

Btw, the given example above is the default name mangling rule.
"""

import collections
import logging
import os.path

from sigal import signals

logger = logging.getLogger(__name__)

orderedDict = collections.OrderedDict([('__', '-'), ('_', ' ')])


def process_album(album):
    '''Process an album title with the predefined rules set in orderedDict.'''
    toMangle = album.title
    for key in orderedDict.keys():
        value = orderedDict[key]
        toMangle = toMangle.replace(key, value)
    album.title = toMangle
    logger.info("Album name mangled to '%s'." % toMangle)


def register(settings):
    global orderedDict
    pluginName = os.path.splitext(__name__)[-1][1:]
    try:
        dictInput = settings[pluginName]
        od = collections.OrderedDict(dictInput)
        orderedDict = od
        logger.info(
            "Using the following name mangling rules: %s", orderedDict)
    except:
        # Settings didn't contain input. Use the default.
        logger.info("Using the default name mangling rules: %s", orderedDict)
    signals.album_initialized.connect(process_album)
