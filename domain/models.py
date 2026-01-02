# Это как физические деньги: 10 долларов всегда равны 10 долларам
@dataclass(frozen=True)  # frozen=True значит "неизменяемый"
class Money:
    amount: Decimal      # сумма (100.50)
    currency: str = "USD" # валюта
# Например: "iPhone 13, цена $999, количество 1"
class OrderLine:
    product_id: str     # ID товара
    product_name: str   # Название
    price: Money        # Цена (объект Money)
    quantity: int       # Количество
    
    def total_price(self):
        return price * quantity  # считаем общую стоимость позиции
class Order:
    def __init__(self, id, customer_id, lines, status):
        self.id = id          # уникальный номер заказа
        self.customer_id = id # кто заказал
        self.lines = lines    # список позиций
        self.status = status  # статус (создан, оплачен, отменен)
    
    # БИЗНЕС-ПРАВИЛА (инварианты):
    
    # Правило 1: Нельзя оплатить пустой заказ
    def pay(self):
        if not self.lines:
            raise Exception("Заказ пуст!")
        
    # Правило 2: Нельзя оплатить дважды
    def pay(self):
        if self.status == "PAID":
            raise Exception("Заказ уже оплачен!")
        
    # Правило 3: После оплаты нельзя менять заказ
    def add_line(self, product):
        if self.status == "PAID":
            raise Exception("Нельзя менять оплаченный заказ!")
