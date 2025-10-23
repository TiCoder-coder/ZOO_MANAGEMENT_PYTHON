from rest_framework import serializers
from zoo_app.models.animalsModels import AnimalsModel
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
        
# BaseSerializerAnimal ke thua tu modelSerializer de tu dong anh xa cac field trong AnimalModel sang de post/ put
class BaseSerializerAnimal(serializers.ModelSerializer):
    class Meta:
        model = AnimalsModel
        fields = '__all__'                                                      # Lay tat ca cac field cua model de su dung
        extra_kwargs = {                                                        # Dung de dinh nghia cac field nay da duoc tao trong AnimalsModel roi nen khong can set lai
            'createAt': {'read_only':True},
            'updateAt': {'read_only': True}
        } 