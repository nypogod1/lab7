from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from domain.models import Order, Money
from domain.exceptions import PaymentException


class OrderRepository(Protocol):
    """Интерфейс репозитория заказов"""
    def get_by_id(self, order_id: UUID) -> Order:
        ...
    
    def save(self, order: Order) -> None:
        ...


class PaymentGateway(Protocol):
    """Интерфейс платежного шлюза"""
    def charge(self, order_id: UUID, money: Money) -> bool:
        ...


@dataclass
class PaymentResult:
    """Результат оплаты"""
    success: bool
    order_id: UUID
    amount: Money
    message: str = ""


class PayOrderUseCase:
    """Use-case для оплаты заказа"""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: UUID) -> PaymentResult:
        """
        Выполнить оплату заказа
        
        Args:
            order_id: Идентификатор заказа
            
        Returns:
            PaymentResult: Результат оплаты
            
        Raises:
            PaymentException: Если произошла ошибка при оплате
        """
        # Загружаем заказ
        order = self.order_repository.get_by_id(order_id)
        
        try:
            # Выполняем доменную операцию
            order.pay()
            
            # Вызываем платежный шлюз
            amount = order.total_amount
            payment_success = self.payment_gateway.charge(order_id, amount)
            
            if not payment_success:
                raise PaymentException("Payment gateway charge failed")
            
            # Сохраняем заказ
            self.order_repository.save(order)
            
            return PaymentResult(
                success=True,
                order_id=order_id,
                amount=amount,
                message="Order paid successfully"
            )
            
        except Exception as e:
            return PaymentResult(
                success=False,
                order_id=order_id,
                amount=order.total_amount if hasattr(order, 'total_amount') else Money(Decimal('0')),
                message=str(e)
            )
