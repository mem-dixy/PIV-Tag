""""""

import os

from celestine.load.directory import walk_file_old


def _execute(session, directory):
    """"""
    image_format = session.interface.image_format()

    def file_extension(path):
        (_, ext) = os.path.splitext(path)
        extension = ext.lower()
        return extension in image_format

    file = walk_file_old(directory)
    image = filter(file_extension, file)
    return list(image)


def setup(window):
    """"""
    print("cow")
    directory = window.session.attribute.directory
    images = _execute(window.session, directory)
    grid = window.load("grid")

    items = zip(grid.__iter__(), images)

    for group, image in items:
        (_, item) = group
        item.update(image=image)
