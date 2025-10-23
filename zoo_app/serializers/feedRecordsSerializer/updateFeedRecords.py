from .baseSerializerFeedRecord import BaseSerializerFeedRecord
from rest_framework import serializers

# Ham dung de tao ra du lieu json khi update cac thuoc tinh
class FeedRecordUpdate(BaseSerializerFeedRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False                                                        # Cac thuoc tinh la khong bat buoc
                        
        # Loai bo field id khi update
        if "idFeedRecord" in self.fields:
            self.fields.pop("idFeedRecord")