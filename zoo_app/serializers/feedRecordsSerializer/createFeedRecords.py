from .baseSerializerFeedRecord import BaseSerializerFeedRecord


# Tao du lieu json khi tao mot feedRecord
class FeedRecordCreate(BaseSerializerFeedRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinh nghia cac thuoc tinh bat buoc khi khoi tao
        field_required = ["idFeedRecord", "animalIdFeedRecord", "foodId", "quantity", "feedAt"]
        for field_name, field in self.fields.items():
            if field in self.fields:
                field.required = True