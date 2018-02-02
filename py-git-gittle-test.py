# -*- coding: utf8 -*-

# Copyright 2013 Aaron O'Mullan <aaron.omullan@friendco.de>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

import os
from gittle import Gittle

path = os.getcwd()
filename = os.path.join(path, __file__) # monitoring current file
print filename

# name = 'Samy Pessé'
# email = 'samypesse@gmail.com'
message = "111C'est beau là bas"

repo = Gittle(path)

repo.stage(__file__)
repo.commit(message=message)


print(('COMMIT_INFO =', repo.commit_info()))

print(('PATH =', path))
