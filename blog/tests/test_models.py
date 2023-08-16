from django.test import TestCase
from blog.models import Post

class ModelTest(TestCase):
	@classmethod
	def setUp(cls):
		Post.objects.create(title='tester',content='hello world')
		

	def test_field_name(self):
		post = Post.objects.get(id=1)
		field= post._meta.get_field('title').verbose_name
		self.assertEquals('Title',field)

	def test_field_length(self):
		post = Post.objects.get(id=1)
		fields = post._meta.get_field('title').max_length
		self.assertEquals(fields,250)

	def test_field_url(self):
		post = Post.objects.get(id=1)
		url = post.get_absolute_url()
		self.assertEquals(url,'post/1')
