from serpy import Serializer, StrField, IntField, FloatField


class BookSerializer(Serializer):
    name = StrField()
    author = StrField()
    pages = IntField()
    price = FloatField()
