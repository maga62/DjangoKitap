from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField()
    parent=TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'

class Kitap(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category=models.ForeignKey(Category,on_delete=models.CASCADE)# cayegory kitap iliskisi
    title= models.CharField(max_length=30)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    yazar=models.CharField(max_length=50)
    basim_yili=models.IntegerField()
    fiyat = models.FloatField()
    baski_sira=models.IntegerField()
    yayinevi=models.CharField(max_length=50)
    stok_durum= models.IntegerField()
    detail=RichTextUploadingField()
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'

class Images(models.Model):
    kitap=models.ForeignKey(Kitap,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'

class Comment(models.Model):
    STATUS=(
        ('New','Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product=models.ForeignKey(Kitap,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE)
    subject= models.CharField(max_length=50)
    comment=models.TextField(max_length=200,blank=True)
    rate=models.IntegerField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment','rate']