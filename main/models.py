from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=256, unique=True, primary_key=True)
    description = models.TextField(max_length=1024, null=False)
    date_created = models.DateField(null=False)
    
    @property
    def categories(self):
        return Category.objects.filter(subject=self)
    
    
class Category(models.Model):
    name = models.CharField(max_length=256, unique=True, primary_key=True)
    description = models.TextField(max_length=2048, null=False)
    abbreviation = models.CharField(max_length=32)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    @property
    def papers(self):
        return Paper.objects.filter(subject=self)


class Paper(models.Model):
    title = models.CharField(max_length=512, null=False)
    abstract = models.TextField(max_length=8096, null=False)
    summarization = models.TextField(max_length=16192, null=True)
    score = models.IntegerField(null=False, default=0)
    subject = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    submitted = models.DateField(null=False)
    url = models.TextField(null=False)
    written_by = models.ManyToManyField("Author")
    

class Author(models.Model):
    name = models.CharField(max_length=512, null=False)
    writed_papers = models.ManyToManyField(Paper)