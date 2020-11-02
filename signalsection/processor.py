from . models import Email, Number, Address, Social


def context(request):
    number = Number.objects.last
    email = Email.objects.last
    address = Address.objects.last
    social = Social.objects.last
    
    return {'number': number, 'email': email, 'address': address, 'social': social}


