from rest_framework import serializers
from zoo_app.models.managersModel import ManagerModel
from bson import ObjectId

# Dung de chuyen doi cac objectId thanh string de nhan dien duoc
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)  # Chuyen objectId thanh chuoi khi tra ve client
    
    # Chuyen doi json --> object
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId format")


# BaseSerializerManager ke thua tu modelSerializer de tu dong anh xa cac field trong ManagerModel sang de post/ put
class BaseSerializerManager(serializers.ModelSerializer):
    class Meta:
        model = ManagerModel
        fields = '__all__'