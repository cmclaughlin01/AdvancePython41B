import baseXDigit
import unittest

class testBaseXDigit(unittest.TestCase):
    def testDunders(self):
        bP = baseXDigit.baseXDigit("0P123")
        bJ = baseXDigit.baseXDigit("0J987")
        bPJ = bP + bJ
        print(bPJ)
        self.assertEqual(bPJ, "0a4086")

        bPJ = bP - bJ
        print(bPJ)
        self.assertEqual(bPJ, "0a-2730")

        bPJ = bP * bJ
        print(bPJ)
        self.assertEqual(bPJ, "0a2310624")

        bG = baseXDigit.baseXDigit("0G12C")
        bH = baseXDigit.baseXDigit("0210100")
        bGH = bG / bH
        print(bGH)
        self.assertEqual(bGH, "0a15.0")

        bPJ = bP % bJ
        print(bPJ)
        self.assertEqual(bP, "0a678")


if __name__ == "__main__":
    unittest.main()