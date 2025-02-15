from django.db import models
from django.contrib.auth.models import User
from voyages.models import Voyage
from passenger.models import Passenger  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: (Исправлен импорт Passenger)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, verbose_name="ID билета")
    voyage = models.ForeignKey('voyages.Voyage', on_delete=models.CASCADE, verbose_name="Рейс")  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: (укажите voyages.Voyage)
    passenger = models.ForeignKey('passenger.Passenger', on_delete=models.CASCADE, verbose_name="Пассажир")
    seat_number = models.IntegerField(verbose_name="Номер места")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    status = models.CharField(max_length=50, verbose_name="Статус")
    qr_code = models.CharField(max_length=255, verbose_name="QR-код")
  

    def __str__(self):
        return f"Билет #{self.ticket_id} на {self.voyage}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"