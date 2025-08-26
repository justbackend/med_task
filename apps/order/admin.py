from apps.order.models import Order
from apps.utils.admin_panel import AdminRegister

AdminRegister.register(Order)
