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

class TestSvtModule(unittest.TestCase):

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
        letter = u'V' # "A" should always have programs...

        programs = svt.getProgramsByLetter(letter)

        self.assertHasContent(programs)

        for program in programs:
            for key in program.keys():
                self.assertIsNotNone(program[key])

    def test_start_video(self):
        print "###### Testing resolveShowURL ######"
        programs = helper.resolveShowURL('http://ur.se/Produkter/161124-Valj-sprak!-Varfor-ett-sprak-till')
        self.assertHasContent(programs)
        programs = helper.resolveShowURL('http://ur.se/Produkter/177414-Ar-det-sant-Kallkritik')
        self.assertHasContent(programs)
        programs = helper.resolveShowURL('http://ur.se/Produkter/183604-Lilla-Aktuellt-skola-2014-10-03')
        self.assertHasContent(programs)

    def test_get_episodes(self):
        print "###### Testing getEpisodes ######"
        episodes = svt.getEpisodes("http://ur.se/Produkter/161123-Valj-sprak")
        self.assertHasContent(episodes)

if __name__ == "__main__":
    unittest.main()
