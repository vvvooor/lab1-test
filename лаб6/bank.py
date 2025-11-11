class InsufficientFundsError(Exception):
    pass

class Account:   #Здесь реализованы методы deposit, withdraw, get_balance и transfer_to. При неправильных операциях я выбрасываю исключения
    """
    Простой банковский счёт.
    Методы:
      - deposit: пополнить
      - withdraw: снять
      - get_balance(): получить текущий баланс
      - transfer_to: перевести на другой Account
    """

    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.owner = owner
        self._balance = float(initial_balance)

    def deposit(self, amount: float) -> float:
        """Пополнение счёта. Возвращает новый баланс."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += float(amount)
        return self._balance

    def withdraw(self, amount: float) -> float:
        """Снятие со счёта. Возвращает новый баланс или выбрасывает исключение."""
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств")
        self._balance -= float(amount)
        return self._balance

    def get_balance(self) -> float:
        """Возвращает текущий баланс."""
        return float(self._balance)

    def transfer_to(self, other: 'Account', amount: float):
        """Перевод средств на другой счёт. Проверяет тип и баланс."""
        if not isinstance(other, Account):
            raise TypeError("Перевод возможен только на другой Account")
        # withdraw и deposit выполнят проверки
        self.withdraw(amount)
        other.deposit(amount)

    def __repr__(self) -> str:
        return f"Account(owner={self.owner!r}, balance={self._balance:.2f})"