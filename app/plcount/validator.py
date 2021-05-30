from django.core.exceptions import ValidationError

def file_size(value):
    filesize = value.size 
    if filesize > 100000000000:
        raise ValidationError("O tamanho maximo é de 12500 MB")