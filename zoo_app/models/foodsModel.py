# ----------------------------- DINH NGHIA CAC THUOC TINH CHO DATABASE -----------------------------------------------------------


from django.db import models
from zoo_app.enums.enums import TypeFood
from django.core.validators import MaxValueValidator, MinValueValidator
class FoodModel(models.Model):
    idFood = models.CharField(max_length = 100, primary_key=True)
    nameFood = models.CharField(max_length = 100)
    typeFood = models.CharField(max_length=100, choices=[(choice.name, choice.value) for choice in TypeFood])
    caloriesPerUnit = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    
    
    # # Dat ten cho table trong database la foods 
    class Meta:
        db_table = "foods"
    
    # Ham dung de log thong tin khi can thiet
    def __str__(self):
        return f"{self.idFood} - {self.nameFood} - {self.typeFood} - {self.caloriesPerUnit}"