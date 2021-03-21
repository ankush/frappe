import frappe
import unittest

import frappe.utils.nestedset as ns


class TestNestedSet(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.TreeDocType = 'TreeTestDoc'

		if frappe.db.exists('DocType', cls.TreeDocType):
			return

		frappe.get_doc({
			'doctype': 'DocType',
			'name': cls.TreeDocType,
			'module': 'Custom',
			'is_tree': 1,
			'custom': 1,
		}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.get_doc('DocType', cls.TreeDocType).delete()


	def setUp(self):
		self.doc = frappe.new_doc(self.TreeDocType)
		self.doc.save()

	def tearDown(self):
		pass

	def test_basic(self):
		self.assertTrue(self.doc.lft > 0)

	def test_update_node(self):
		pass

	def test_move_node(self):

		pass

	def test_rebuild_tree(self):
		pass

	def test_rebuild_node(self):
		pass

	def test_validate_loop(self):
		pass

	def test_validate_ledger(self):
		pass

	def test_validate_child_exists(self):
		pass

	def test_get_root_node_count(self):
		pass

	def test_validate_one_root(self):
		pass

	def test_get_root_of(self):
		pass

	def test_get_descendants(self):
		pass

	def test_get_ancestors(self):
		pass
