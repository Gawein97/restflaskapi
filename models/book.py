class Book:
    """
    Base class for Book representation
    name, author, pages
    """
    def __init__(self, name: str, author: str, pages: int, price: float):
        self.name = name
        self.author = author
        self.pages = pages
        self.price = price
