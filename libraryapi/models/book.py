class Book:
    """
    Base class for Book representation
    name, author, pages
    """
    def __init__(self, name: str, author: str, pages: int, price: float):
        self.name = name
        self.author = author
        self.pages = pages
        self.price = round(price, 2)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                self.__dict__[k] = v
