import pytest
from decimal import Decimal
from uuid import uuid4

from src.domain.models import Order, OrderLine, Money, OrderStatus
from src.domain.exceptions import OrderDomainException


class TestMoney:
    """Тесты для Value Object Money"""
    
    def test_create_money(self):
        money = Money(Decimal("100.50"), "USD")
        assert money.amount == Decimal("100.50")
        assert money.currency == "USD"
    
    def test_create_negative_money_raises_error(self):
        with pytest.raises(ValueError):
            Money(Decimal("-10"))
    
    def test_add_money(self):
        money1 = Money(Decimal("100"))
        money2 = Money(Decimal("50"))
        result = money1 + money2
        assert result.amount == Decimal("150")
    
    def test_add_different_currencies_raises_error(self):
        money1 = Money(Decimal("100"), "USD")
        money2 = Money(Decimal("50"), "EUR")
        with pytest.raises(ValueError):
            money1 + money2
    
    def test_multiply_money(self):
        money = Money(Decimal("100"))
        result = money * 3
        assert result.amount == Decimal("300")


class TestOrder:
    """Тесты для агрегата Order"""
    
    @pytest.fixture
    def order_id(self):
        return uuid4()
    
    @pytest.fixture
    def customer_id(self):
        return uuid4()
    
    @pytest.fixture
    def sample_order(self, order_id, customer_id):
        return Order(order_id, customer_id)
    
    @pytest.fixture
    def order_with_lines(self, order_id, customer_id):
        order = Order(order_id, customer_id)
        line1 = OrderLine(
            product_id=uuid4(),
            product_name="Product 1",
            price=Money(Decimal("100")),
            quantity=2
        )
        line2 = OrderLine(
            product_id=uuid4(),
            product_name="Product 2",
            price=Money(Decimal("50")),
            quantity=3
        )
        order.add_line(line1)
        order.add_line(line2)
        return order
    
    def test_create_order(self, order_id, customer_id):
        order = Order(order_id, customer_id)
        assert order.id == order_id
        assert order.customer_id == customer_id
        assert order.status == OrderStatus.CREATED
        assert len(order.lines) == 0
        assert order.total_amount.amount == Decimal("0")
    
    def test_add_line_to_order(self, sample_order):
        line = OrderLine(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("100")),
            quantity=2
        )
        sample_order.add_line(line)
        assert len(sample_order.lines) == 1
        assert sample_order.total_amount.amount == Decimal("200")
    
    def test_remove_line_from_order(self, order_with_lines):
        product_id = order_with_lines.lines[0].product_id
        order_with_lines.remove_line(product_id)
        assert len(order_with_lines.lines) == 1
    
    def test_pay_order_success(self, order_with_lines):
        order_with_lines.pay()
        assert order_with_lines.status == OrderStatus.PAID
    
    def test_pay_empty_order_raises_error(self, sample_order):
        with pytest.raises(OrderDomainException, match="Cannot pay empty order"):
            sample_order.pay()
    
    def test_pay_already_paid_order_raises_error(self, order_with_lines):
        order_with_lines.pay()
        with pytest.raises(OrderDomainException, match="Order is already paid"):
            order_with_lines.pay()
    
    def test_modify_paid_order_raises_error(self, order_with_lines):
        order_with_lines.pay()
        
        # Попытка добавить строку
        with pytest.raises(OrderDomainException, match="Cannot modify paid order"):
            line = OrderLine(
                product_id=uuid4(),
                product_name="New Product",
                price=Money(Decimal("100")),
                quantity=1
            )
            order_with_lines.add_line(line)
        
        # Попытка удалить строку
        with pytest.raises(OrderDomainException, match="Cannot modify paid order"):
            product_id = order_with_lines.lines[0].product_id
            order_with_lines.remove_line(product_id)
    
    def test_total_amount_calculation(self, order_with_lines):
        # 100 * 2 + 50 * 3 = 200 + 150 = 350
        assert order_with_lines.total_amount.amount == Decimal("350")
    
    def test_cancel_order(self, order_with_lines):
        order_with_lines.cancel()
        assert order_with_lines.status == OrderStatus.CANCELLED
    
    def test_cancel_paid_order_raises_error(self, order_with_lines):
        order_with_lines.pay()
        with pytest.raises(OrderDomainException, match="Cannot cancel paid order"):
            order_with_lines.cancel()


class TestOrderLine:
    """Тесты для OrderLine"""
    
    def test_order_line_total(self):
        line = OrderLine(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("100")),
            quantity=3
        )
        assert line.total.amount == Decimal("300")
