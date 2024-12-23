class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Ошибка: Деление на ноль!"
        return a / b

    def calculate(self, expression):
        try:
            result = eval(expression)
            return result
        except ZeroDivisionError:
            return "Ошибка: Деление на ноль!"
