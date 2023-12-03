class FormatError(Exception):
    """
    Исключение, которое вызывается при наличии недопустимого формата даты.
    """
    def __init__(self):
        self.message = 'Недопустимый формат даты'
        super().__init__(self.message)


class UniqueError(Exception):
    """
    Исключение, которое вызывается при обноружении неуникального ключа,
    передаваемых параметров.
    """
    def __init__(self):
        self.message = 'Найдено неуникальное значение'
        super().__init__(self.message)
