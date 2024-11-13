from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data='success', status=200, **kwargs):
        response_data = {
            'response': data
        }
        super().__init__(response_data, status=status, **kwargs)


class CustomException(APIException):
    status_code = 400
    default_detail = {'response': 'Something went wrong'}


def get_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        model_name = model._meta.verbose_name.title()
        raise NotFound(f"{model_name} object not found with parameters: {kwargs}")
