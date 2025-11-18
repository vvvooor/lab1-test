import pytest
from bank import Account, InsufficientFundsError


@pytest.fixture
def acc():
    return Account("Test", 100.0)

# параметризация для deposit
@pytest.mark.parametrize(
    "initial, amount, expected",
    [
        (100, 50, 150),
        (0, 10, 10),
        (10, 0.5, 10.5),
        (1.5, 2.5, 4.0)
    ]
)
def test_deposit(initial, amount, expected):
    a = Account("A", initial)
    assert a.deposit(amount) == pytest.approx(expected)

def test_deposit_invalid():
    a = Account("A", 10)
    with pytest.raises(ValueError):
        a.deposit(0)
    with pytest.raises(ValueError):
        a.deposit(-5)

# параметризация для withdraw
@pytest.mark.parametrize(
    "initial, amount, expected",
    [
        (100, 50, 50),
        (80, 80, 0),
        (20.5, 0.5, 20.0)
    ]
)
def test_withdraw(initial, amount, expected):
    a = Account("A", initial)
    assert a.withdraw(amount) == pytest.approx(expected)

def test_withdraw_invalid_and_insufficient():
    a = Account("A", 50)
    with pytest.raises(ValueError):
        a.withdraw(0)
    with pytest.raises(ValueError):
        a.withdraw(-1)
    with pytest.raises(InsufficientFundsError):
        a.withdraw(100)

# тесты перевода
@pytest.mark.parametrize(
    "from_init,to_init,amount,expected_from,expected_to",
    [
        (200, 50, 100, 100, 150),
        (10, 0, 5, 5, 5)
    ]
)
def test_transfer_success(from_init, to_init, amount, expected_from, expected_to):
    a = Account("A", from_init)
    b = Account("B", to_init)
    a.transfer_to(b, amount)
    assert a.get_balance() == pytest.approx(expected_from)
    assert b.get_balance() == pytest.approx(expected_to)

def test_transfer_insufficient_and_invalid_target():
    a = Account("A", 50)
    b = Account("B", 10)
    with pytest.raises(InsufficientFundsError):
        a.transfer_to(b, 100)
    with pytest.raises(TypeError):
        a.transfer_to("не счёт", 10)

# дополнительный тест: строковое представление (необязательно)
def test_repr_and_get_balance():
    a = Account("Ivan", 123.45)
    assert "Ivan" in repr(a)
    assert a.get_balance() == pytest.approx(123.45)