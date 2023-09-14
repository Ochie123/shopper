# products/models.py
import os
import uuid
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone

#class ActiveProductManager(models.Manager): 
   # def get_query_set(self):
     #   return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    categories = models.ManyToManyField( "categories.Category", 
                            verbose_name=_("Categories"),
                            
                            related_name="category_products",
                        )
    
   
    toprated = models.BooleanField(default=False, help_text="1=toprated")
    bestseller = models.BooleanField(default=False, help_text="1=bestseller")
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)

    description = models.CharField(_("description"), blank=True)
    price = models.DecimalField(
        _("price ($)"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    is_active = models.BooleanField(default=True) 

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
           


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.uuid, self.slug])
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)


    