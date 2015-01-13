import os
import pytest
import sigal
from sigal.gallery import Gallery


def test_album_title_mangler(settings):
    settings['plugins'].append('sigal.plugins.album_title_mangler')
    sigal.init_plugins(settings)
    gal = Gallery(settings, ncpu=1)
    gal.build()
    for key in gal.albums.keys():
        album = gal.albums[key]
        if album.path.startswith('Album'):
            assert album.title == 'Album name-underscored'
