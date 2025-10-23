from .baseSerializerEnclosure import BaseEnclosureSerializer


# Tao du lieu json khi tao mot enclosure
class EnclosureCreate(BaseEnclosureSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinh nghia cac thuoc tinh bat buoc khi khoi tao
        fields_required = ["idEnclosure", "nameEnclosure", "areaSize", "climate", 'capacity']
        for field_name, field in self.fields.items():
            if field in self.fields:
                field.required = True
    