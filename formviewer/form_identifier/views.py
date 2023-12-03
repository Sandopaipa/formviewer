import dotenv
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from .utils.db import get_doc
from .utils.exceptions import UniqueError
from .utils.validators import DictBuilder, Field, get_type

import os

dotenv.load_dotenv(os.getenv('ENVIRONMENT_FILE', 'env'))

class GetFormView(APIView):
    """
    Представление для проведения валидации данных с формы и поиска формы.
    Если форма была найдена - то возвращает её имя и код 200.
    Если форма не была найдена - возвращает переданные названия полей, их тип и код 203.
    """
    def post(self, request):
        #  Набор полей и типов для запроса к БД на поиск нужной формы.
        field_set = {}
        query_set = {
            "name": {"$exists": True}
        }
        #  Составление словаря из полученных параметров.
        #  Если обнаружено неуникальное название поля - вызывается исключение.
        try:
            data = DictBuilder(request.data).get_dict
        except UniqueError:
            return Response(UniqueError)
        #  Валидация полей.
        for key, value in data.items():
            attr = Field(property_name=key, property_value=value)
            field_type = attr.check(value)
            field_set[key] = get_type(field_type)
        #  Поиск документа.
        query_set.update(field_set)
        document = get_doc(
            host=os.getenv('MONGO_HOST'),
            db_name=os.getenv('MONGO_DB_NAME'),
            collection_name=os.getenv('MONGO_COLLECTION_NAME'),
            query=query_set
        )

        if document is not None:
            return Response(data=document['name'], status=status.HTTP_200_OK)
        else:
            return Response(data=field_set, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
