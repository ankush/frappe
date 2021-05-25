from __future__ import unicode_literals
import unittest
import frappe
from frappe.website.path_resolver import PathResolver
from frappe.website.serve import get_response, get_response_content
from frappe.utils import set_request

test_records = frappe.get_test_records('Web Page')

def get_page_content(route):
	set_request(method='GET', path = route)
	response = get_response()
	return frappe.as_unicode(response.data)

class TestWebPage(unittest.TestCase):
	def setUp(self):
		frappe.db.sql("delete from `tabWeb Page`")
		for t in test_records:
			frappe.get_doc(t).insert()

	def test_path_resolver(self):
		self.assertTrue(PathResolver("test-web-page-1").is_valid_path())
		self.assertTrue(PathResolver("test-web-page-1/test-web-page-2").is_valid_path())
		self.assertTrue(PathResolver("test-web-page-1/test-web-page-3").is_valid_path())
		self.assertFalse(PathResolver("test-web-page-1/test-web-page-Random").is_valid_path())

	def test_base_template(self):
		content = get_page_content('/_test/_test_custom_base.html')

		# assert the text in base template is rendered
		self.assertTrue('<h1>This is for testing</h1>' in frappe.as_unicode(content))

		# assert template block rendered
		self.assertTrue('<p>Test content</p>' in frappe.as_unicode(content))

	def test_content_type(self):
		web_page = frappe.get_doc(dict(
			doctype = 'Web Page',
			title = 'Test Content Type',
			published = 1,
			content_type = 'Rich Text',
			main_section = 'rich text',
			main_section_md = '# h1\nmarkdown content',
			main_section_html = '<div>html content</div>'
		)).insert()

		self.assertTrue('rich text' in get_page_content('/test-content-type'))

		web_page.content_type = 'Markdown'
		web_page.save()
		self.assertTrue('markdown content' in get_page_content('/test-content-type'))

		web_page.content_type = 'HTML'
		web_page.save()
		self.assertTrue('html content' in get_page_content('/test-content-type'))

		web_page.delete()

	def test_dynamic_route(self):
		web_page = frappe.get_doc(dict(
			doctype = 'Web Page',
			title = 'Test Dynamic Route',
			published = 1,
			dynamic_route = 1,
			route = '/doctype-view/<doctype>',
			content_type = 'HTML',
			dynamic_template = 1,
			main_section_html = '<div>{{ frappe.form_dict.doctype }}</div>'
		)).insert()

		try:
			content = get_page_content('/doctype-view/DocField')
			self.assertTrue('<div>DocField</div>' in content)
		finally:
			web_page.delete()

	def test_custom_base_template_path(self):
		content = get_response_content('/_test/_test_folder/_test_page')
		# assert the text in base template is rendered
		self.assertTrue('<h1>This is for testing</h1>' in frappe.as_unicode(content))

		# assert template block rendered
		self.assertTrue('<p>Test content</p>' in frappe.as_unicode(content))

	def test_json_sidebar_data(self):
		frappe.flags.look_for_sidebar = False
		content = get_response_content('/_test/_test_folder/_test_page')
		self.assertTrue('Test Sidebar' not in frappe.as_unicode(content))
		frappe.flags.look_for_sidebar = True
		content = get_response_content('/_test/_test_folder/_test_page')
		self.assertTrue('Test Sidebar' in frappe.as_unicode(content))
		frappe.flags.look_for_sidebar = False

	def test_index_and_next_comment(self):
		content = get_response_content('/_test/_test_folder')
		# test if {index} was rendered
		self.assertTrue('<a href="/_test/_test_folder/_test_page"> Test Page</a>' \
			in frappe.as_unicode(content))
		self.assertTrue('<a href="/_test/_test_folder/_test_toc"> Test Toc</a>' \
			in frappe.as_unicode(content))

		content = get_response_content('/_test/_test_folder/_test_page')
		# test if {next} was rendered
		self.assertTrue('Next: <a class="btn-next" href="/_test/_test_folder/_test_toc"> Test Toc</a>' \
			in frappe.as_unicode(content))

	def test_meta_tags(self):
		pass

	def test_breadcrumbs(self):
		pass

	def test_downloadable_file(self):
		pass




# breadcrumb
# validate
# page context caching
