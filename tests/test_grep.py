#!/usr/bin/env python

import unittest
import re

from csvkit.grep import FilteringCSVReader

class TestGrep(unittest.TestCase):
    def setUp(self):
        self.tab1 = [
            ['id', 'name', 'i_work_here'],
            [u'1', u'Chicago Reader', u'first'],
            [u'2', u'Chicago Sun-Times', u'only'],
            [u'3', u'Chicago Tribune', u'only'],
            [u'1', u'Chicago Reader', u'second']]

        self.tab2 = [
            ['id', 'age', 'i_work_here'],
            [u'1', u'first', u'0'],
            [u'4', u'only', u'0'],
            [u'1', u'second', u'0'],
            [u'2', u'only', u'0', u'0']] # Note extra value in this column

    def test_pattern(self):
        fcr = FilteringCSVReader(iter(self.tab1),patterns=['1'])
        self.assertEqual(self.tab1[0],fcr.next())
        self.assertEqual(self.tab1[1],fcr.next())
        self.assertEqual(self.tab1[4],fcr.next())
        try:
            fcr.next()
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_no_header(self):
        fcr = FilteringCSVReader(iter(self.tab1),patterns={ 2: 'only' },header=False)
        self.assertEqual(self.tab1[2],fcr.next())
        self.assertEqual(self.tab1[3],fcr.next())
        try:
            fcr.next()
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_regex(self):
        pattern = re.compile(".*(Reader|Tribune).*")
        fcr = FilteringCSVReader(iter(self.tab1),patterns = { 1: pattern })
        
        self.assertEqual(self.tab1[0],fcr.next())
        self.assertEqual(self.tab1[1],fcr.next())
        self.assertEqual(self.tab1[3],fcr.next())
        self.assertEqual(self.tab1[4],fcr.next())
        try:
            fcr.next()
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass
        
    def test_inverse(self):
        fcr = FilteringCSVReader(iter(self.tab2),patterns = ['1'], inverse=True)
        self.assertEqual(self.tab2[0],fcr.next())
        self.assertEqual(self.tab2[2],fcr.next())
        self.assertEqual(self.tab2[4],fcr.next())
        try:
            fcr.next()
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass
            
