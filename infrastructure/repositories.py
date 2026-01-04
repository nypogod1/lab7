from typing import Dict, Optional
from uuid import UUID

from domain.models import Order
from application.use_cases import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""
    
    def __init__(self):
        self._orders: Dict[UUID, Order] = {}
    
    def get_by_id(self, order_id: UUID) -> Order:
        order = self._orders.get(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        return order
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order
    
    def clear(self) -> None:
        """Очистить хранилище (для тестов)"""
        self._orders.clear()
