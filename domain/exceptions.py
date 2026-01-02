
class DomainException(Exception):
    """Базовое исключение для доменных ошибок"""
    pass


class EmptyOrderException(DomainException):
    """Заказ пуст"""
    pass


class AlreadyPaidException(DomainException):
    """Заказ уже оплачен"""
    pass


class OrderCannotBeModifiedException(DomainException):
    """Нельзя изменять оплаченный заказ"""
    pass
