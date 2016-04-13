# -*- coding: utf-8 -*-
import inspect
import sys
import unittest
# Manipulate path first
sys.path.append("../")
sys.path.append("./lib")

import resources.lib.urplay as svt
import resources.lib.helper as helper
import CommonFunctions as common

# Set up the CommonFunctions module
common.plugin = "TestSvt"
common.dbg = True

episodes = []

class TestURModule(unittest.TestCase):

    def assertHasContent(self, list):
        if list == None:
            self.fail("List is None")
        if list == []:
            self.fail("List is empty")

    def test_get_alphas(self):
        print "###### Testing getAlphas ######"
        alphas = svt.getAlphas()
        self.assertHasContent(alphas)

    def test_programs_by_letter(self):
        print "###### Testing getProgramsByLetter ######"
        programs = svt.getAtoO()
        self.assertHasContent(programs)
        for program in programs:
            for key in program.keys():
                self.assertIsNotNone(program[key])

    def test_start_video(self):
        print "###### Testing resolveShowURL ######"
        programs = helper.resolveShowURL('http://urplay.se/program/190205-livet-i-mattelandet')
        self.assertHasContent(programs)
        print programs
        self.assertHasContent(programs)

    def test_get_episodes(self):
        print "###### Testing getEpisodes (Program) ######"
        episodes = svt.getEpisodes("http://urplay.se/program/190205-livet-i-mattelandet")
        self.assertHasContent(episodes)
    
    def test_get_categories(self):
        print "###### Testing getCategories ######"
        categories = svt.getCategories()
        print categories
        self.assertHasContent(categories)

    def test_get_subjects(self):
        print "###### Testing getSubjects ######"
        categories = svt.getSubjects()
        self.assertHasContent(categories)
        # print categories

if __name__ == "__main__":
    unittest.main()
