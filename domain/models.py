# Это как физические деньги: 10 долларов всегда равны 10 долларам
@dataclass(frozen=True)  # frozen=True значит "неизменяемый"
class Money:
    amount: Decimal      # сумма (100.50)
    currency: str = "USD" # валюта
