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
        programs = helper.resolveShowURL('http://ur.se/Produkter/177160-Kortfilmsklubben-franska-Mon-amoureux')
        print programs
        self.assertHasContent(programs)

    def test_get_episodes(self):
        print "###### Testing getEpisodes (Program) ######"
        episodes = svt.getEpisodes("http://ur.se/Produkter/161123-Valj-sprak")
        self.assertHasContent(episodes)
        print "###### Testing getEpisodes (Subject) ######"
        episodes = svt.getEpisodes("http://ur.se/Produkter?ur_subject_tree=samh%C3%A4llskunskap")
        self.assertHasContent(episodes)
        print "###### Testing getEpisodes (Subject second page) ######"
        episodes = svt.getEpisodes("http://ur.se/Produkter?page=2&ur_subject_tree=samh%C3%A4llskunskap")
        self.assertHasContent(episodes)
        print "###### Testing getEpisodes (Category) ######"
        episodes = svt.getEpisodes("http://urplay.se/Sprak")
        self.assertHasContent(episodes)
        print "###### Testing getEpisodes (Category last page) ######"
        episodes = svt.getEpisodes("http://urplay.se/Forelasningar-debatt?page=27")
        self.assertHasContent(episodes)
        print "###### Testing getEpisodes (Last Change) ######"
        episodes = svt.getEpisodes(svt.URL_TO_LAST_CHANCE)
        self.assertHasContent(episodes)
    
    def test_get_categories(self):
        print "###### Testing getCategories ######"
        categories = svt.getCategories()
        print categories
        self.assertHasContent(categories)

    def test_get_subjects(self):
        print "###### Testing getSubjects ######"
        categories = svt.getSubjects()
        print categories
        self.assertHasContent(categories)

if __name__ == "__main__":
    unittest.main()
