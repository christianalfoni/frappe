# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals

import unittest, frappe

class TestClient(unittest.TestCase):
	def test_set_value(self):
		todo = frappe.get_doc(dict(doctype='ToDo', description='test')).insert()
		frappe.set_value('ToDo', todo.name, 'description', 'test 1')
		self.assertEqual(frappe.get_value('ToDo', todo.name, 'description'), 'test 1')

		frappe.set_value('ToDo', todo.name, {'description': 'test 2'})
		self.assertEqual(frappe.get_value('ToDo', todo.name, 'description'), 'test 2')

	def test_delete(self):
		from frappe.client import delete

		todo = frappe.get_doc(dict(doctype='ToDo', description='description')).insert()
		delete("ToDo", todo.name)

		self.assertFalse(frappe.db.exists("ToDo", todo.name))
		self.assertRaises(frappe.DoesNotExistError, delete, "ToDo", todo.name)

	def test_http_valid_method_access(self):
		from frappe.client import delete
		from frappe.handler import execute_cmd

		frappe.set_user("Administrator")

		frappe.local.request = frappe._dict()
		frappe.local.request.method = 'POST'

		frappe.local.form_dict = frappe._dict({
			'doc': dict(doctype='ToDo', description='Valid http method'),
			'cmd': 'frappe.client.save'
		})
		todo = execute_cmd('frappe.client.save')

		self.assertEqual(todo.get('description'), 'Valid http method')

		delete("ToDo", todo.name)

	def test_http_invalid_method_access(self):
		from frappe.handler import execute_cmd

		frappe.set_user("Administrator")

		frappe.local.request = frappe._dict()
		frappe.local.request.method = 'GET'

		frappe.local.form_dict = frappe._dict({
			'doc': dict(doctype='ToDo', description='Invalid http method'),
			'cmd': 'frappe.client.save'
		})

		self.assertRaises(frappe.PermissionError, execute_cmd, 'frappe.client.save')
