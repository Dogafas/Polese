from django.db import models
from django.core.validators import MinValueValidator
import random

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, verbose_name="ID билета")
    voyage = models.ForeignKey('voyages.Voyage', on_delete=models.CASCADE, verbose_name="Рейс")
    passenger = models.ForeignKey('passenger.Passenger', on_delete=models.CASCADE, verbose_name="Пассажир")
    departure_stop = models.ForeignKey('routes.Stop', on_delete=models.CASCADE, related_name='departure_tickets', verbose_name="Пункт отправления") 
    arrival_stop = models.ForeignKey('routes.Stop', on_delete=models.CASCADE, related_name='arrival_tickets', verbose_name="Пункт прибытия") 
    seat_number = models.IntegerField(verbose_name="Номер места", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")
    status = models.CharField(max_length=50, verbose_name="Статус")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Билет #{self.ticket_id} на {self.voyage}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

    def assign_seat(self):
        """
        Назначает случайный доступный номер места на рейс, учитывая available_seats.
        """
        voyage = self.voyage
        # Проверяем, есть ли еще доступные места на этот рейс
        if voyage.available_seats <= 0:
            raise ValueError("Нет доступных мест на этот рейс")

        # Получаем все уже занятые места на этот рейс
        booked_seats = Ticket.objects.filter(voyage=voyage).values_list('seat_number', flat=True)

        # Создаем список потенциальных мест (от 1 до кол-ва мест в available_seats)
        potential_seats = list(range(1, voyage.ship.capacity + 1))

        # Фильтруем список потенциальных мест, оставляя только те, которые еще не забронированы
        available_seats = [seat for seat in potential_seats if seat not in booked_seats]

        if available_seats:
            # Выбираем случайное место из списка доступных
            self.seat_number = random.choice(available_seats)  
            self.voyage.available_seats -= 1
            self.voyage.save()
            self.save()  
        else:
            # Если нет доступных мест, выбрасываем исключение
            raise ValueError("Нет доступных мест на этот рейс")

