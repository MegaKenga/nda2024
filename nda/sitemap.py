from django.contrib.sitemaps import Sitemap

from catalog.models import Brand, Category, Product
from django.urls import reverse


class IndexSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['home', 'privacy', 'contacts', 'work', 'brands_with_certificates']

    def location(self, item):
        return reverse(item)


class Certificates(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        brand = Brand.visible.all()
        return brand

    def location(self, item):
        return reverse('brand_certificates', args=[item.pk])


class BrandSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Brand.visible.all()


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Category.visible.all().distinct()


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.visible.all()

sitemaps = {
    'index': IndexSitemap,
    'certificates': Certificates,
    'brand': BrandSitemap,
    'category': CategorySitemap,
    'product': ProductSitemap,
        }
