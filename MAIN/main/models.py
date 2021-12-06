from django.db import models
#import logging
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse


User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=40, blank=True)

    #cream un profil pentru fiecare autor
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    
    #bio reprezinta o descriere a autorului 
    bio = HTMLField()
    #points , se adauga un numar de puncte la fiecare postare sau comment realizat de autor
    points = models.IntegerField(default=0)
    #aici este poza de profil
    profile_pic = ResizedImageField(size=[60, 90], quality=100, upload_to="authors", default=None, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullName)
        super(Author,self).save(*args, **kwargs)
    

    #reprezentam modelul author sub forma de titlu (si nu ca obiect) in pagina admin-ului
    def __str__(self):
        return self.fullName


# este un titlu a unui subforum
class Category(models.Model):
    title = models.CharField(max_length=350)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.title
   
   #aici salvam automat fiecare slug a unei Category
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category,self).save(*args, **kwargs)
    
    def get_url(self):
        return reverse("subforum", kwargs={
            "slug":self.slug
        })
    
    @property
    def number_of_posts(self):
        return Post.objects.filter(categories=self).count()

    #ultima postare o verificam dupa data
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")

class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:250]
    
    class Meta:
        verbose_name_plural = "replies"




class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:250]

    replies = models.ManyToManyField(Reply, blank=True)

# aici am implementat o metoda prin care
# pot sa afisez postarea cu tot cu comment-uri + alte chestii
#e asemanator crearii unor DB tables
class Post(models.Model):
    title = models.CharField(max_length=350)
    #cu slug accesam detail page pt fiecare post
    #slug_len == title_len obligatoriu
    #blank=True este pentru fill automatic
    #A "slug" is a way of generating a valid URL, generally using data already obtained. For instance, a slug uses the title to generate a URL
    #ex: www.example.com/article/the-46-year-old-cow (the-46...-cow is the slug)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    #aici este content field-ul
    content = HTMLField()
    #mai multe categorii pentru fiecare postare
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    #tracking the number of views
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name="hit_count_generic_relation"
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("thread", kwargs={
            "slug":self.slug
        })
    
    @property
    def num_comments(self):
        return self.comments.count()
    
    @property
    def last_reply(self):
        return self.comments.latest("date")