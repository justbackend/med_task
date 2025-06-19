from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data="success", status=200, **kwargs):
        response_data = {"response": data}
        super().__init__(response_data, status=status, **kwargs)


class CustomException(APIException):
    status_code = 400
    default_detail = {"detail": "Something went wrong"}


def get_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist as err:
        model_name = model._meta.verbose_name.title()
        explanation = f"{model_name} object not found with parameters: {kwargs}"
        raise NotFound(explanation) from err
