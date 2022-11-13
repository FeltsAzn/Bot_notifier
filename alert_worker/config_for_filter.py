from decimal import Decimal

"""
Файл конфигурации сортировщика валют для регулировки минимальных и максимальных значений, а так же 
стартовое значение и шаг перехода.
"""

HIGH_PERCENT = Decimal(5)
START_PERCENT = Decimal(3)
UP_PERCENT = Decimal(1)
DOWN_PERCENT = Decimal(1.5)
