import re
from enum import Enum

from datetime import datetime

from .exceptions import UniqueError, FormatError


class AllowedFieldTypes(Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    DATE = 'date'
    TEXT = 'text'


class DictBuilder:
    """
    Класс для преобразования передаваемых в POST запросе параметров в виде строки
    в словарь.
    """
    def __init__(self, paramset: str):
        self.raw_data = paramset

    def _get_items(self, data: str, delimiter: str) -> list:
        """
        Метод для разделения строки.
        """
        return data.split(delimiter)

    @property
    def get_dict(self) -> dict:
        """
        Метод для преобразования строки - связки параметров и их значений
        в словарь.
        """
        item_dict = {}
        item_list = self._get_items(data=self.raw_data, delimiter='&')
        for item in item_list:
            dict_attr_list = self._get_items(data=item, delimiter='=')
            try:
                new_value = item_dict[dict_attr_list[0]]
                raise UniqueError
            except KeyError:
                item_dict[dict_attr_list[0]] = dict_attr_list[1]

        return item_dict


class Field:
    def __init__(self, property_name: str, property_value: str):
        self.name = property_name
        self.value = property_value

    def check(self, data: str) -> AllowedFieldTypes:
        """
        Метод для проверки типов данных.
        data - значение передаваемых данных в виде строки.
        field_type - тип данных
        """
        methods = {
            AllowedFieldTypes.PHONE: self._is_phone(data),
            AllowedFieldTypes.EMAIL: self._is_email(data),
            AllowedFieldTypes.DATE: self._is_date(data),
            AllowedFieldTypes.TEXT: self._is_text(),
        }
        for field_type, method in methods.items():
            value = method
            if value is not False:
                return field_type
            else:
                continue

    def _is_phone(self, data: str) -> bool:
        """
        Метод для определения - является ли оргумент передаваемого параметра
        номером телефона.
        Вид номера телефона: +7 xxx xxx xx xx (%2B7 XXX XXX XX XX)
        """
        _PATTERN = r"(\+7)(\s\d{3}){2}(\s\d{2}){2}"

        phone = data

        if re.fullmatch(pattern=_PATTERN, string=phone):
            return True
        else:
            return False

    def _is_date(self, data: str) -> bool:
        """
        Метод для валидации даты
        Вид даты:   DD.MM.YYYY - _DATE_PATTERN1
                    YYYY-MM-DD - _DATE_PATTERN2
        Допустима только числовая запись даты
        (например:  10.01.2001
                    2001-01-10)
        """
        try:
            date_format = self._get_format(data)
        except FormatError:
            return False

        date_string = re.match(pattern=date_format['pattern'], string=data)

        if date_string is not None:
            try:
                date_obj = datetime.strptime(data, date_format['form'])
                return True
            except ValueError:
                return False

    def _is_email(self, data: str) -> bool:
        """
        Метод валидации email.
        """
        pattern = r'(^[^~!#$%&]+@[^~!#$%&]+\.[^~!#$%&]+$)'
        is_email = re.match(pattern=pattern, string=data)
        if is_email is not None:
            return True
        else:
            return False

    def _is_text(self) -> bool:
        """
        Валидация текста.
        """
        return True

    def _get_format(self, date: str) -> dict[str, str]:
        """
        Выдает формат даты и паттерн для обработки регулярным выражением.
        date - дата.
        return: dict - метод возвращает словарь: формат даты и паттерн.
        """
        _DATE_FORMAT_1 = '%d.%m.%Y'
        _DATE_FORMAT_2 = '%Y-%m-%d'
        _DATE_PATTERN1 = r'(\d{2}.){2}\d{4}'
        _DATE_PATTERN2 = r'(\d{4})(-\d{2}){2}'
        if '.' in date:
            return {
                'form': _DATE_FORMAT_1,
                'pattern': _DATE_PATTERN1
            }
        elif '-' in date:
            return {
                'form': _DATE_FORMAT_2,
                'pattern': _DATE_PATTERN2
            }
        else:
            raise FormatError


def get_type(data: AllowedFieldTypes) -> str:
    """
    Возвоащает строковое представление типа поля.
    """
    match data:

        case AllowedFieldTypes.PHONE:
            return str(AllowedFieldTypes.PHONE.value)
        case AllowedFieldTypes.TEXT:
            return str(AllowedFieldTypes.TEXT.value)
        case AllowedFieldTypes.EMAIL:
            return str(AllowedFieldTypes.EMAIL.value)
        case AllowedFieldTypes.DATE:
            return str(AllowedFieldTypes.DATE.value)