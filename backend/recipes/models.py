from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридиентов."""
    name = models.CharField(
        max_length=256,
    )
    measure = models.CharField(
        max_length=256,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тэгов."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )
    color = models.CharField(max_length=16)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецептов"""
    name = models.CharField(
        max_length=256,
    )
    description = models.TextField(
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    image = models.ImageField(
        upload_to='pecipes/images/',
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    time_cooking = models.PositiveSmallIntegerField(
        'время приготовления',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(300)
        ),
        error_messages={
            'validators': 'Пожалуйста, поставьте время приготовления'
        },
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Таблица для связи рецептов и ингридиентов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return (f'{self.ingredient.name} ({self.ingredient.measure})'
                f'- {self.amount}')
