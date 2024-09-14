# Приводим данные от пользователя к требуемому виду на основе модели
from rest_framework import serializers
from .models import ewsitem

class ewsitemSerializer(serializers.ModelSerializer):
    email_title = serializers.CharField(max_length=250)  # Сюда вставляем заголовки писем с типом из exchangelib
    sender = serializers.EmailField(max_length=254)  # адрес отправителя
    done = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = ewsitem
        fields = '__all__'   # Все поля, полученные от пользователя будут сопоставляться с БД