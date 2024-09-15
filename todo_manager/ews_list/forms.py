from django import forms


class ewsitemForm(forms.Form):
    # Сюда вставляем заголовки писем с типом из exchangelib
    email_title = forms.CharField(label="Заголовок письма: ", max_length=250)
    sender = forms.EmailField(label="Отправитель: ", max_length=254)  # адрес отправителя
    done = forms.BooleanField(label="Обработано: ")
