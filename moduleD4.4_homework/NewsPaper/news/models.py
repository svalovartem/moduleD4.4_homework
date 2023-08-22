from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('accounts.Author', on_delete=models.CASCADE, verbose_name="Автор")

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Опубликованно")
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категория")
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Содержимое")
    rating = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return f'{self.title} ({self.posted.ctime()})'

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()


    def preview(self):
        return self.text[0:123] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.text
    
    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()
