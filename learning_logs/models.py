from django.db import models

# Create your models here.


class Topic(models.Model):
    '''A topic the user is learning'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Returen the text field as a representation of the Topic instead of less meaningful description of the object itself'''
        return self.text


class Entry(models.Model):
    '''An entry tied to a topic'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''to display the plural form of the word entry instead of 'entrys' '''
        '''this is to override default class Meta'''
        verbose_name_plural = 'entries'

    def __str__(self):
        '''Return the first 50 characters of the entry'''
        return "{} \n {}...".format(self.title, str(self.text)[:50])
