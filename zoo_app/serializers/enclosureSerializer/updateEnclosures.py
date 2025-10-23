from rest_framework import serializers
from .baseSerializerEnclosure import BaseEnclosureSerializer


# Ham dung de tao ra du lieu json khi update cac thuoc tinh
class EnclosureUpdate(BaseEnclosureSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False                                                       # Cac thuoc tinh la khong bat buoc
        
        # Loai bo field id khi update
        if "idEnclosure" in self.fields:
            self.fields.pop("idEnclosure")