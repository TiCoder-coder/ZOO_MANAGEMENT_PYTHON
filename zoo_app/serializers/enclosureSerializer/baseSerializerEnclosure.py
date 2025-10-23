from rest_framework import serializers
from zoo_app.models.enclosuresModel import EnclosureModel
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
        
        
# BaseEnclosureSerializer ke thua tu modelSerializer de tu dong anh xa cac field trong EnclosureModel sang de post/ put
class BaseEnclosureSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)  # thêm dòng này để xử lý _id

    class Meta:
        model = EnclosureModel
        fields = '__all__'
