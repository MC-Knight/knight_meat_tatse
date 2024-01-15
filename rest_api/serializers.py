from rest_framework import serializers, validators


from rest_api.models import Dish


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish.
    """

    class Meta:
        model = Dish
        fields = ("id", "name", "image", "price")
