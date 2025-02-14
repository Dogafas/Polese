class ShortDescriptionMixin:
    def short_description(self, obj):
        return obj.description[:100] + '...'
    short_description.short_description = "Описание"  # Задаем verbose_name для колонки