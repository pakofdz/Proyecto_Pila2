from store.models import Customer

def create_user(backend, user, response, *args, **kwargs):
    print(user)
    print(response)
    Customer.objects.create(
        user=user,
        name=response['user']['username'],
        email=response['user']['email']
    )
    