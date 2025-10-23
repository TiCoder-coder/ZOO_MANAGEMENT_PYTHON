# ----------------------------- DINH NGHIA CAC THUOC TINH CHO DATABASE -----------------------------------------------------------


from django.db import models

class FeedRecordModel(models.Model):
    idFeedRecord = models.CharField(max_length = 100, primary_key=True)
    animalIdFeedRecord = models.CharField(max_length = 100)
    foodId = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    feedAt = models.DateTimeField(auto_now_add=True)
    
    # Dat ten cho table trong database la feed_records
    class Meta:
        db_table = "feed_records"
    
    # Ham dung de log thong tin khi can thiet
    def __str__(self):
        return f"{self.idFeedRecord} - {self.animalIdFeedRecord} - {self.foodId} - {self.quantity} - {self.feedAt}"