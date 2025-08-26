from rest_framework import generics
from rest_framework.views import APIView

from apps.order.models import Order
from apps.order.serializers import OrderPaymentSerializer
from apps.order.serializers import OrderSerializer
from apps.order.serializers import OrderStatusUpdateSerializer
from apps.order.serializers import WorkerAssignmentToOrderSerializer
from apps.users.models import User
from apps.utils.customs import CustomResponse
from apps.utils.customs import get_or_404


class OrderCreateListView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related("service", "user", "worker").all()
    serializer_class = OrderSerializer


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    allowed_roles = [User.Role.ADMIN, User.Role.WORKER]


class WorkerAssignmentToOrderAPIView(APIView):
    serializer_class = WorkerAssignmentToOrderSerializer
    allowed_roles = [User.Role.ADMIN]

    def post(self, request):
        serializer = WorkerAssignmentToOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_or_404(Order, id=serializer.validated_data["order_id"])
        worker = get_or_404(User, id=serializer.validated_data["worker_id"])

        order.worker = worker
        order.save()

        return CustomResponse()


class OrderPaymentView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPaymentSerializer
