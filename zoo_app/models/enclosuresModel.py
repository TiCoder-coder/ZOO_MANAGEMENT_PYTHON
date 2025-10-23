# ----------------------------- DINH NGHIA CAC THUOC TINH CHO DATABASE -----------------------------------------------------------


from django.db import models
from zoo_app.enums.enums import Climate


# Dinh nghia cac thuoc tinh cho database enclosures 
class EnclosureModel(models.Model):
    idEnclosure = models.CharField(max_length = 100, primary_key=True)
    nameEnclosure = models.CharField(max_length = 100)
    areaSize = models.CharField(max_length = 100)
    climate = models.CharField(max_length=100, choices = [(choice.name, choice.value) for choice in Climate])
    capacity = models.IntegerField()
    
    # Dat ten cho table trong database la enclosures
    class Meta:
        db_table = 'enclosures'
    
    # Ham dung de log thong tin khi can thiet
    def __str__(self):
        return f"{self.idEnclosure} - {self.nameEnclosure} - {self.areaSize} - {self.climate} - {self.capacity}"