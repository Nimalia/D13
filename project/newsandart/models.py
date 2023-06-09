from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)


    def __str__(self):
        return f'{self.authorUser.username}'

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating"))
        pRat = 0
        pRat += postRat.get("postRating")

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum("rating"))
        cRat = 0
        cRat += commentRat.get("commentRating")

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name="categories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = "NW"
    ARTICLE = "AR"
    CATEGORY_CHOICE = (
        (NEWS, _('Новость')),
        (ARTICLE, _('Статья')),
    )
    categoryType = models.CharField(max_length=8, choices=CATEGORY_CHOICE, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128, verbose_name=_('Заголовок'))
    text = models.TextField(verbose_name=_('Текст'))
    rating = models.SmallIntegerField(default=0)


    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."

    def __str__(self):
        return f'{self.title}, {self.dateCreation}, {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.dateCreation}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# class Subscription(models.Model):
#     user = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )
#     category = models.ForeignKey(
#         to='Category',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )