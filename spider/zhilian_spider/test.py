#!/usr/bin/env python
# -*- coding: utf-8 -*-


def raisd_error():
    raise IndexError


try:
    print('test')
    raisd_error()
    print('test')
except:
    print('hello')
