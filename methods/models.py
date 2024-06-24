from django.db.models import Model,CharField

# Create your models here.
class Hermite(Model):
    x_values = CharField(verbose_name="Valores de X",max_length=100,null=False,blank=False)
    y_values = CharField(verbose_name="Valores de Y",max_length=100,null=True,blank=False)
    y_derivate = CharField(verbose_name="Y derivada",max_length=100,null=True,blank=False)
    class Meta:
        verbose_name = "Metodo de Hermite"
        verbose_name_plural = "Metodode Hermite"
        db_table = "hermite"
    