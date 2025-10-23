from .baseSerializerFoods import BaseSerializerFood

# Ham dung de tao ra du lieu json khi update cac thuoc tinh
class FoodUpdate(BaseSerializerFood):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False                                                  # Cac thuoc tinh la khong bat buoc
        
        # Loai bo field id khi update
        if "idFood" in self.fields:
            self.fields.pop("idFood") 