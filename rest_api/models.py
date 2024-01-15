from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="dishes/")
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Order Model
