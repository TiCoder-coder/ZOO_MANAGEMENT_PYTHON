# ----------------------------- DINH NGHIA CAC THUOC TINH CHO DATABASE -----------------------------------------------------------


from django.db import models
from zoo_app.enums.enums import HealthStatus, Gender

# Dinh nghia cac thuoc tinh cho database animals
class AnimalsModel(models.Model):
    id = models.CharField(max_length = 100, primary_key=True)
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    species = models.CharField(max_length = 100)
    gender = models.CharField(max_length=100, choices=[(choice.name, choice.value) for choice in Gender])
    weight = models.IntegerField()
    healthStatus = models.CharField(max_length=100, choices=[(choice.name, choice.value) for choice in HealthStatus])
    enclosureId = models.CharField(max_length = 100)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)


    # Dat ten cho table trong database la animals
    class Meta:
        db_table = "animals"
    
    # Ham dung de log thong tin khi can thiet
    def __str__(self):
        return f"{self.id} - {self.name} - {self.age} - {self.species} - {self.gender} - {self.weight} - {self.healthStatus} - {self.enclosureId} - {self.createAt} - {self.updateAt}"