from django.db import models
# from catalog.models import Unit, Brand, Category, Offer


# class MainPage(models.Model):
#     banner = models.ImageField(upload_to='banners/', blank=True, null=True)
#
#     class Meta:
#         ordering = ['id']
#         verbose_name = 'Файлы, связанные с главной страницей'
#         verbose_name_plural = 'Файлы, связанные с главной страницей'
#
#     def __str__(self):
#         return str(self.id)


class NDAImage(models.Model):
    is_active = models.BooleanField()
    image = models.ImageField()

    class Meta:
        pass

# class NDAFile(models.Model):
#     is_active = models.BooleanField()
#     file = models.FileField()
#
#     class Meta:
#         pass



# class UnitFiles(models.Model):
#     unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
#     banner = models.ImageField(upload_to='banner/', null=True, blank=True)
#     image = models.ImageField(upload_to='image/', null=True, blank=True)
#
#     class Meta:
#         ordering = ['unit']
#         verbose_name = 'Файлы, связанные с направлениями'
#         verbose_name_plural = 'Файлы, связанные с направлениями'
#
#     def __str__(self):
#         return str(self.unit)
#
#
# class BrandFiles(models.Model):
#     brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='logo')
#     banner = models.ImageField(upload_to='banner/', null=True, blank=True)
#     image = models.ImageField(upload_to='image/', null=True, blank=True)
#
#     class Meta:
#         ordering = ['brand']
#         verbose_name = 'Файлы, связанные с брендами'
#         verbose_name_plural = 'Файлы, связанные с брендами'
#
#     def __str__(self):
#         return str(self.brand)
#
#
# class CategoryFiles(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     banner = models.ImageField(upload_to='banner/', null=True, blank=True)
#     image = models.ImageField(upload_to='image/', null=True, blank=True)
#     registration_certificate = models.FileField(upload_to='registration_certificate/', null=True, blank=True)
#     instruction = models.FileField(upload_to='instruction/', null=True, blank=True)
#
#     class Meta:
#         ordering = ['category']
#         verbose_name = 'Файлы, связанные с категориями'
#         verbose_name_plural = 'Файлы, связанные с категориями'
#
#     def __str__(self):
#         return str(self.category)
#
#
# class OfferFiles(models.Model):
#     offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
#     image = models.ImageField(upload_to='image/', null=True, blank=True)
#     tech_specification = models.FileField(upload_to='tech_specification/', null=True, blank=True)
#
#     class Meta:
#         ordering = ['offer']
#         verbose_name = 'Файлы, связанные с товарами'
#         verbose_name_plural = 'Файлы, связанные с товарами'
#
#     def __str__(self):
#         return str(self.offer)
