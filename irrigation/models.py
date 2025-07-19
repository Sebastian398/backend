from django.db import models

class Sensor(models.Model):
    tipo = models.CharField(max_length=50)  # e.g. humedad, temperatura
    valor = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.valor}'

class ProgramacionRiego(models.Model):
    inicio = models.TimeField()
    duracion = models.IntegerField(help_text='Duración en segundos')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Riego a las {self.inicio} por {self.duracion} seg'
