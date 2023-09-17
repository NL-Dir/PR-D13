from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from .tasks.basic import comment_accepted_mail
from django.contrib.auth.forms import UserCreationForm
from django import forms


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.authorUser.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    TANKS = 'TA'
    HEALERS = 'HE'
    DAMAGEDEALERS = 'DD'
    MERCHANTS = 'ME'
    GUILDMASTERS = 'GM'
    QUESTGIVERS = 'QG'
    BLACKSMITHS = 'BS'
    TANNERS = 'TS'
    POTIONMASTERS = 'PM'
    SPELLMASTERS = 'SM'

    CATEGORY_CHOICES = (
        (TANKS, 'Танки'),
        (HEALERS, 'Хилы'),
        (DAMAGEDEALERS, 'ДД'),
        (MERCHANTS, 'Торговцы'),
        (GUILDMASTERS, 'Гилдмастеры'),
        (QUESTGIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (TANNERS, 'Кожевники'),
        (POTIONMASTERS, 'Зельевары'),
        (SPELLMASTERS, 'Мастера заклинаний')
    )

    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=TANKS)
    creationDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    img = models.ImageField(upload_to='images_uploaded', null=True, blank=True)
    video = models.FileField(upload_to='images_uploaded', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])
                                         ])

    def __str__(self):
        return self.title


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def preview(self):
        return self.text[0:123] + '...'

    def accept(self):
        self.is_accepted = True
        self.save()
        comment_accepted_mail(self)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",)
