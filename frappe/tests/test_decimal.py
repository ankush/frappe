import unittest
from decimal import Decimal
from frappe.utils import D, flt


class TestDecimalUtils(unittest.TestCase):

	def test_equivalence(self):
		self.assertEqual(1, D("1"))
		self.assertEqual(0.1, D("0.1"))
		self.assertEqual(D("1"), 1)
		self.assertEqual(D("0.1"), 0.1)

		self.assertNotEqual(D("0.1"), 0.2)
		self.assertNotEqual(0.2, D("0.1"))

	def test_equalities(self):
		self.assertEqual(D("0.1").compare(0.1), D("0"))
		self.assertEqual(D("0.1").compare(0.2), D("-1"))
		self.assertEqual(D("0.1").compare(0.0), D("1"))

		self.assertGreater(D("0.2"), 0.1)
		self.assertGreater(0.3, D("0.2"))
		self.assertFalse(D("0.3") > 0.3)
		self.assertFalse(0.3 < D("0.3"))
		self.assertFalse(0.3 > D("0.3"))
		self.assertFalse(D("0.3") < 0.3)

	def test_from_float(self):
		self.assertEqual(D("0.1") + 0.2, D.from_float(0.3))

	def test_addition_with_floats(self):
		self.assertEqual(D("0.1") + 0.2, D("0.3"))
		self.assertEqual(0.2 + D("0.1"), D("0.3"))

	def test_subtraction_with_floats(self):
		self.assertEqual(D("0.3") - 0.1, D("0.2"))
		self.assertEqual(0.3 - D("0.1"), D("0.2"))

	def test_multiplication_with_floats(self):
		self.assertEqual(D("0.1") * 3, D("0.3"))
		self.assertEqual(0.1 * D("3"), D("0.3"))

	def test_division_int(self):
		self.assertEqual(D("3.0") / 10, D("0.3"))
		self.assertEqual(3.0 / D("10"), D("0.3"))

		self.assertEqual(D("3.0") / 2, D("1.5"))
		self.assertEqual(3.0 / D("2"), D("1.5"))

	def test_division_float(self):
		self.assertEqual(D("3.0") / 1.5, D("2"))
		self.assertEqual(3.0 / D("1.5"), D("2"))

	def test_mod(self):
		self.assertEqual(D("3.0") % 0.5, D("0"))

	def test_mod(self):
		self.assertEqual(D("3.0") % 0.5, D("0"))
		self.assertEqual(3.0 % D("0.5"), D("0"))

	def test_floor_div(self):
		self.assertEqual(D("3.0") // 2, 3 // 2)
		self.assertEqual(6 // D("4.0"), 6 // 4)

		self.assertEqual(D("4.5") // 0.3, 4.5 // 0.3)
		self.assertEqual(66.6 // D("4.4"), 66.6 // 4.4)

	def test_increment(self):
		a = D("0.1")
		a += 0.2
		self.assertEqual(a, D("0.3"))
		a = 0.1
		a += D("0.2")
		self.assertEqual(a, D("0.3"))

	def test_divmod(self):
		self.assertEqual(divmod(D("5.2"), 2.0), (D("2"), D("1.2")))
		self.assertEqual(divmod(5.2, D("0.6")), (D("8"), D("0.4")))

	def test_pow(self):
		self.assertEqual(D("0.5") ** 2, D("0.25"))
		self.assertEqual(D("0.6") ** 3, D("0.216"))
		self.assertEqual(D("100000") ** D("0.2"), D("10"))
		self.assertEqual(100000.0 ** D("0.2"), D("10"))

	def test_rounding(self):
		a = D(Decimal(0.33))
		self.assertNotEqual(a, D("0.33"))
		self.assertEqual(round(a, 6), D("0.33"))

	def test_bankers_rounding(self):
		rounded = flt(D(Decimal(0.33)))
		self.assertEqual(type(rounded), D)
		rounded = flt(D("0.5"), 0)
		self.assertEqual(type(rounded), D)

		self.assertEqual(flt(D("0.5"), 0), D("0"))
		self.assertEqual(flt(D("1.5"), 0), D("2"))
		self.assertEqual(flt(D("0.15"), 1), D("0.2"))
		self.assertEqual(flt(D("1.25"), 1), D("1.2"))
