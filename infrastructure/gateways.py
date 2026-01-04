from typing import Dict
from uuid import UUID

from domain.models import Money
from application.use_cases import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Fake реализация платежного шлюза"""
    
    def __init__(self, should_fail: bool = False):
        self._should_fail = should_fail
        self._charges: Dict[UUID, Money] = {}
    
    def charge(self, order_id: UUID, money: Money) -> bool:
        """
        Выполнить списание средств
        
        Args:
            order_id: Идентификатор заказа
            money: Сумма для списания
            
        Returns:
            bool: True если списание успешно, False в противном случае
        """
        if self._should_fail:
            return False
        
        # Сохраняем информацию о списании
        self._charges[order_id] = money
        return True
    
    def get_charge(self, order_id: UUID) -> Optional[Money]:
        """Получить информацию о списании"""
        return self._charges.get(order_id)
    
    def reset(self) -> None:
        """Сбросить состояние (для тестов)"""
        self._charges.clear()
