import time
import hashlib

import requests

from click_up import ClickUp
from click_up.models import ClickTransaction
from click_up.views import ClickWebhook

from django.db import transaction
from django.utils import timezone
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response

click_up = ClickUp(service_id=CLICK_SERVICE_ID, merchant_id=CLICK_MERCHANT_ID)

timestamp = str(int(time.time()))
raw = timestamp + CLICK_SECRET_KEY
digest = hashlib.sha1(raw.encode()).hexdigest()
CLICK_AUTH_HEADER = f"{CLICK_MERCHANT_ID}:{digest}:{timestamp}"


def create_receipt(order, receipt_type):
    stock = order.stock
    poses = stock.pos_set.all()
    if not poses.exists():
        raise exception(ErrorCodes.STOCK_POS_NOT_FOUND, "Pos не найден.")

    pos = None
    manager = None
    for pos in poses:
        manager = managers_models.Manager.objects.filter(pos=pos).first()
        pos = pos
        if manager:
            break
    if not manager:
        raise exception(ErrorCodes.MANAGER_NOT_FOUND, "Manager не найден.")

    paid = False
    if receipt_type == managers_choices.ReceiptTypes.REFUND:
        paid = True

    receipt = managers_models.Receipt.objects.create(
        order=order,
        manager=manager,
        pos=pos,
        stock=stock,
        staff_name=manager.name,
        receipt_type=receipt_type,
        card_number=order.head_company.card_number,
        datetime=timezone.now(),
        received_card=order.price * 100,
        send_soliq=False,
        paid=paid,
    )

    payment_type = managers_models.PaymentType.objects.filter(name="CLICK").first()

    if not payment_type:
        raise exception(
            ErrorCodes.PAYMENT_TYPE_NOT_FOUND, "Тип платежа 'CLICK' не найден."
        )

    managers_models.ReceiptPayment.objects.create(
        receipt=receipt,
        payment_type=payment_type,
        price=order.price,
    )

    for order_product in order.orderproduct_set.all():
        quantity = order_product.quantity
        price = order_product.price * quantity
        nds = order_product.product.nds
        vat_percent = (
            0 if nds is None or nds == "Без НДС" else int(nds.replace("%", ""))
        )
        vat = 0 if vat_percent == 0 else price * (vat_percent / 100)

        managers_models.ReceiptProduct.objects.create(
            receipt=receipt,
            product=order_product.product,
            quantity=quantity,
            price=price,
            vat_percent=vat_percent,
            vat=vat,
            owner_type=1,
            class_code=order_product.product.classifier_code,
            package_code=order_product.product.packagecode,
        )


def send_items_to_click(
    service_id, payment_id, items, received_cash=0, received_ecash=0, received_card=0
):
    url = "https://api.click.uz/v2/merchant/payment/ofd_data/submit_items"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth": CLICK_AUTH_HEADER,
    }
    payload = {
        "service_id": service_id,
        "payment_id": payment_id,
        "items": items,
        "received_cash": received_cash,
        "received_ecash": received_ecash,
        "received_card": received_card,
    }
    send_me(f"URL: {url} \n\nPAYLOAD: {payload}")
    return requests.post(url, json=payload, headers=headers)


def submit_qrcode(service_id, payment_id, qrcode):
    url = "https://api.click.uz/v2/merchant/payment/ofd_data/submit_qrcode"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth": CLICK_AUTH_HEADER,
    }
    payload = {"service_id": service_id, "payment_id": payment_id, "qrcode": qrcode}
    return requests.post(url, json=payload, headers=headers)


def get_qrcode_link(service_id, payment_id):
    url = f"http://api.click.uz/v2/merchant/payment/ofd_data/{service_id}/{payment_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth": CLICK_AUTH_HEADER,
    }
    response = requests.get(url, headers=headers)
    return response.json()


class ClickPayView(ClientsBaseAPIView):
    @swagger_auto_schema(
        operation_summary="Click payment",
        request_body=serializers.ClickPaySerializer,
        responses=resp(200, serializers.ClickPayResponseSerializer),
    )
    def post(self, request):
        with transaction.atomic():
            serializer = serializers.ClickPaySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_id = serializer.validated_data.get("order_id")
            order = self._get_order(order_id, self.request.user.user.company)
            if (
                order.payment_status == managers_choices.OrderPaymentStatuses.PAID
                or order.payment_status
                == managers_choices.OrderPaymentStatuses.CANCELED
            ):
                raise exception(
                    ErrorCodes.ORDER_ALREADY_PAID, "Заказ уже оплачен или отменен."
                )

            if order.price < 100:
                raise exception(
                    ErrorCodes.ORDER_PRICE_LESS_THAN_1000,
                    "Сумма заказа должна быть больше 100 сум.",
                )

            if not order.receipt_set.exists():
                create_receipt(order, managers_choices.ReceiptTypes.SALE)
            pay_link = click_up.initializer.generate_pay_link(
                id=order.id,
                amount=order.price,
                return_url=f"https://kanstik.uz/orders/{order_id}",
            )
            order.payment_status = managers_choices.OrderPaymentStatuses.IN_PROCESS
            order.save()
            return Response({"link": pay_link})

    def _get_order(self, order_id, company):
        try:
            order = managers_models.Order.objects.get(id=order_id, head_company=company)
        except managers_models.Order.DoesNotExist:
            raise exception(ErrorCodes.ORDER_NOT_FOUND, "Order не найден.")
        return order


class ClickWebhookAPIView(ClickWebhook):
    parser_classes = [FormParser, JSONParser]

    def successfully_payment(self, params):
        with transaction.atomic():
            trans_id = int(params.click_trans_id)
            payment_id = int(params.click_paydoc_id)
            # amount = int(params.amount)

            trans = ClickTransaction.objects.get(transaction_id=trans_id)
            order = self._get_order(trans.account_id)

            # if order.price != amount:
            #     raise exception(
            #         ErrorCodes.CLICK_AMOUNT_MISMATCH,
            #         "Сумма заказа не совпадает с суммой Click.",
            #     )
            #
            # if order.payment_status == managers_choices.OrderPaymentStatuses.PAID:
            #     raise exception(ErrorCodes.ORDER_ALREADY_PAID, "Заказ уже оплачен.")

            order.payment_status = managers_choices.OrderPaymentStatuses.PAID

            receipt = order.receipt_set.filter(
                receipt_type=managers_choices.ReceiptTypes.SALE
            ).last()

            items = []
            total_price = 0
            for receipt_product in receipt.receiptproduct_set.all():
                total_price += receipt_product.price * 100
                items.append(
                    {
                        "Name": f"{receipt_product.product.title} {receipt_product.product.measure}",
                        "Barcode": receipt_product.product.barcode[0]
                        if len(receipt_product.product.barcode) > 0
                        else None,
                        "SPIC": receipt_product.class_code,
                        "PackageCode": receipt_product.product.packagecode,
                        "Price": int(receipt_product.price),
                        "Amount": receipt_product.quantity,
                        "VAT": int(receipt_product.vat),
                        "VATPercent": int(receipt_product.vat_percent),
                        "CommissionInfo": {"TIN": 305191400},
                    }
                )

            response = send_items_to_click(
                service_id=CLICK_SERVICE_ID,
                payment_id=payment_id,
                items=items,
                received_ecash=int(total_price),
            )

            if response.status_code != 200 or response.json().get("error_code"):
                raise exception(
                    ErrorCodes.CLICK_FISCAL_ERROR,
                    f"Click Error: {response.json().get('error_note')}",
                )

            receipt.payment_id = payment_id
            receipt.save()
            order.save()

    def cancelled_payment(self, params):
        with transaction.atomic():
            trans_id = int(params.click_trans_id)
            trans = ClickTransaction.objects.get(transaction_id=trans_id)
            if trans.state == ClickTransaction.CANCELLED:
                order_id = trans.account_id
                order = self._get_order(order_id)
                order.payment_status = managers_choices.OrderPaymentStatuses.CANCELED
                order.save()
                receipt = order.receipt_set.filter(
                    receipt_type=managers_choices.ReceiptTypes.SALE
                ).last()
                if not receipt.paid:
                    raise exception(
                        ErrorCodes.CLICK_FISCAL_ERROR,
                        "Click transaction cancelled, but receipt is not paid.",
                    )
                create_receipt(order, managers_choices.ReceiptTypes.REFUND)

    def _get_order(self, order_id):
        try:
            return managers_models.Order.objects.get(id=order_id)
        except managers_models.Order.DoesNotExist:
            raise exception(ErrorCodes.ORDER_NOT_FOUND, "Order не найден.")


class ClickSendFiscalView(AdminBaseAPIView):
    def post(self, request, order_id, payment_id):
        with transaction.atomic():
            order = self._get_order(order_id)

            # if order.price != amount:
            #     raise exception(
            #         ErrorCodes.CLICK_AMOUNT_MISMATCH,
            #         "Сумма заказа не совпадает с суммой Click.",
            #     )
            #
            # if order.payment_status == managers_choices.OrderPaymentStatuses.PAID:
            #     raise exception(ErrorCodes.ORDER_ALREADY_PAID, "Заказ уже оплачен.")

            order.payment_status = managers_choices.OrderPaymentStatuses.PAID

            receipt = order.receipt_set.filter(
                receipt_type=managers_choices.ReceiptTypes.SALE
            ).last()

            items = []
            total_price = 0
            for receipt_product in receipt.receiptproduct_set.all():
                total_price += receipt_product.price * 100
                items.append(
                    {
                        "Name": f"{receipt_product.product.title} {receipt_product.product.measure}",
                        "Barcode": receipt_product.product.barcode[0]
                        if len(receipt_product.product.barcode) > 0
                        else None,
                        "SPIC": receipt_product.class_code,
                        "PackageCode": receipt_product.product.packagecode,
                        "Price": int(receipt_product.price) * 100,
                        "Amount": receipt_product.quantity,
                        "VAT": int(receipt_product.vat) * 100,
                        "VATPercent": int(receipt_product.vat_percent),
                        "CommissionInfo": {"TIN": 305191400},
                    }
                )

            response = send_items_to_click(
                service_id=CLICK_SERVICE_ID,
                payment_id=payment_id,
                items=items,
                received_ecash=int(total_price),
            )

            if response.status_code != 200 or response.json().get("error_code"):
                raise exception(
                    ErrorCodes.CLICK_FISCAL_ERROR,
                    f"Click Error: {response.json().get('error_note')}",
                )

            receipt.payment_id = payment_id
            receipt.save()
            order.save()
            return Response(status=200)

    def _get_order(self, order_id):
        try:
            return managers_models.Order.objects.get(id=order_id)
        except managers_models.Order.DoesNotExist:
            raise exception(ErrorCodes.ORDER_NOT_FOUND, "Order не найден.")
