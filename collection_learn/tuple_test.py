#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple

User = namedtuple('User', ['name', 'age', 'height'])
user_tuple = ('xiaojian', 22, 171)
user = User(*user_tuple)
print(user.name, user.age, user.height)
