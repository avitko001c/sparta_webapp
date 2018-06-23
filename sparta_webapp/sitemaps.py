from django.contrib importfrom .sitemaps
from django.urls import reverse

class StaticViewSitemapfrom .sitemaps.Sitemap):
	priority = 0.5
	changefreq = 'daily'

	def items(self):
		return ['main', 'about', 'license']

	def location(self, item):
		return reverse(item)
