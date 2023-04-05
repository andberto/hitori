from unittest import TestCase, main
import Constants
from Hitori import Hitori

class HitoriTest(TestCase):

    def test_play_at(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        hitori.play_at(0,0)
        self.assertTrue(hitori.annotation_at(0,0) == Constants.BLACK)

    def test_flag_at(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        hitori.flag_at(0,0)
        self.assertTrue(hitori.annotation_at(0,0) == Constants.CIRCLE)

    def test_value_at(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        matrix = hitori.read_board("offline_puzzles/hitori-5x5.csv")
        self.assertTrue(hitori.value_at(0,0) == matrix[0][0])

    def test_finished(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        moves = [(0, 0), (0, 4), (1, 1), (2, 4), (3, 1), (3, 3), (4, 0)]
        self.assertFalse(hitori.finished()) 
        for i in moves:
            hitori.play_at(i[0],i[1])
        self.assertTrue(hitori.finished())

    def test_wrong(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        hitori.play_at(0,0)
        hitori.play_at(0,1)
        self.assertTrue(hitori.wrong())
        hitori.remove_annotations()
        hitori.play_at(0,0)
        hitori.play_at(1,0)
        self.assertTrue(hitori.wrong())

    def test_solve(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        hitori.solve()
        self.assertTrue(hitori.finished())

    def test_automat(self):
        hitori = Hitori("offline_puzzles/hitori-5x5.csv")
        hitori.play_at(0,0)
        hitori.help_user_with_circles()
        self.assertTrue(hitori.annotation_at(0,1) == Constants.CIRCLE and hitori.annotation_at(1,0) == Constants.CIRCLE)
        hitori.flag_at(2,2)
        hitori.help_user_with_duplicates()
        self.assertTrue(hitori.annotation_at(2,4) == Constants.BLACK)

if __name__ == '__main__':
    main()