from.models import User, Product
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class ProductSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(max_length=None, use_url=True)
    # image_url = serializers.SerializerMethodField('get_image_url')
    # # def get_image_url(self, obj):
    # #     request = self.context['request']
    # #     return request.build_absolute_uri(settings.MEDIA_URL + obj['image'])
    # def get_image_url(self, obj):
    #     request = self.context.get("request")
    #     return request.build_absolute_uri(settings.MEDIA_URL + obj.image.url)
    class Meta:
        model = Product
        fields = ("guid", "price", "quantity", "product_name","rating", "image")
    

   
