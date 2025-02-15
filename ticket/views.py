from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm
from voyages.models import Voyage  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: (Импортируем Voyage)

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            voyage_id = form.cleaned_data['voyage'].pk  # Получаем ID рейса из формы
            voyage = get_object_or_404(Voyage, pk=voyage_id)  # Получаем объект рейса

            if voyage.available_seats > 0:  # Проверяем наличие доступных мест
                try:
                    seat_number = Ticket.assign_seat(Ticket, voyage=voyage)  # Получаем номер места
                    ticket = form.save(commit=False)
                    ticket.seat_number = seat_number  # Устанавливаем номер места
                    ticket.save()
                    voyage.available_seats -= 1  # Уменьшаем количество доступных мест
                    voyage.save()
                    messages.success(request, f"Билет успешно оформлен! Номер вашего места: {ticket.seat_number}")
                    return redirect('ticket_success')
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, 'ticket_form.html', {'form': form, 'error': str(e)})
            else:
                messages.error(request, "К сожалению, на этот рейс больше нет доступных мест.")
                return render(request, 'ticket_form.html', {'form': form})
        else:
            return render(request, 'ticket_form.html', {'form': form})
    else:
        form = TicketForm()
        return render(request, 'ticket_form.html', {'form': form})

def ticket_success(request):
    """
    Отображает страницу успеха с информацией о билете.
    """
    return render(request, 'ticket_success.html')