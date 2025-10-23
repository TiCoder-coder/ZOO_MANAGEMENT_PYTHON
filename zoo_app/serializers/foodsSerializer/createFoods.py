from .baseSerializerFoods import BaseSerializerFood

# Tao du lieu json khi tao mot food
class FoodCreate(BaseSerializerFood):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinh nghia cac thuoc tinh bat buoc khi khoi tao
        field_required = ["idFood", "nameFood", "typeFood", "caloriesPerUnit"]
        for field_name, field in self.fields.items():
            if field in self.fields:
                field.required = True