import pytest
from decimal import Decimal
from uuid import uuid4

from src.domain.models import Order, OrderLine, Money, OrderStatus
from src.application.use_cases import PayOrderUseCase, PaymentResult
from src.infrastructure.repositories import InMemoryOrderRepository
from src.infrastructure.gateways import FakePaymentGateway


class TestPayOrderUseCase:
    """Тесты для use-case оплаты заказа"""
    
    @pytest.fixture
    def order_id(self):
        return uuid4()
    
    @pytest.fixture
    def customer_id(self):
        return uuid4()
    
    @pytest.fixture
    def repository(self):
        return InMemoryOrderRepository()
    
    @pytest.fixture
    def payment_gateway(self):
        return FakePaymentGateway()
    
    @pytest.fixture
    def use_case(self, repository, payment_gateway):
        return PayOrderUseCase(repository, payment_gateway)
    
    @pytest.fixture
    def sample_order(self, order_id, customer_id, repository):
        order = Order(order_id, customer_id)
        line = OrderLine(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("100")),
            quantity=2
        )
        order.add_line(line)
        repository.save(order)
        return order
    
    def test_successful_payment(self, use_case, repository, payment_gateway, sample_order):
        # Выполняем оплату
        result = use_case.execute(sample_order.id)
        
        # Проверяем результат
        assert result.success is True
        assert result.order_id == sample_order.id
        assert result.amount.amount == Decimal("200")
        assert "successfully" in result.message.lower()
        
        # Проверяем, что заказ сохранен с правильным статусом
        saved_order = repository.get_by_id(sample_order.id)
        assert saved_order.status == OrderStatus.PAID
        
        # Проверяем, что платежный шлюз был вызван
        charge = payment_gateway.get_charge(sample_order.id)
        assert charge is not None
        assert charge.amount == Decimal("200")
    
    def test_payment_empty_order(self, use_case, repository, order_id, customer_id):
        # Создаем пустой заказ
        empty_order = Order(order_id, customer_id)
        repository.save(empty_order)
        
        # Пытаемся оплатить
        result = use_case.execute(order_id)
        
        # Проверяем результат
        assert result.success is False
        assert "empty order" in result.message.lower()
        
        # Проверяем, что статус не изменился
        saved_order = repository.get_by_id(order_id)
        assert saved_order.status == OrderStatus.CREATED
    
    def test_double_payment_attempt(self, use_case, repository, payment_gateway, sample_order):
        # Первая оплата должна быть успешной
        result1 = use_case.execute(sample_order.id)
        assert result1.success is True
        
        # Вторая оплата должна завершиться ошибкой
        result2 = use_case.execute(sample_order.id)
        assert result2.success is False
        assert "already paid" in result2.message.lower()
    
    def test_payment_gateway_failure(self, repository, order_id, customer_id):
        # Создаем платежный шлюз, который всегда падает
        failing_gateway = FakePaymentGateway(should_fail=True)
        use_case = PayOrderUseCase(repository, failing_gateway)
        
        # Создаем заказ
        order = Order(order_id, customer_id)
        line = OrderLine(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("100")),
            quantity=1
        )
        order.add_line(line)
        repository.save(order)
        
        # Пытаемся оплатить
        result = use_case.execute(order_id)
        
        # Проверяем результат
        assert result.success is False
        assert "failed" in result.message.lower()
        
        # Проверяем, что статус не изменился
        saved_order = repository.get_by_id(order_id)
        assert saved_order.status == OrderStatus.CREATED
    
    def test_order_not_found(self, use_case):
        non_existent_id = uuid4()
        result = use_case.execute(non_existent_id)
        assert result.success is False
        assert "not found" in result.message.lower()
