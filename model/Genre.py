from dataclasses import dataclass


@dataclass
class Genre:
    GenreId : int
    Name : str

    def __init__(self, GenreId: int, Name: str):
        self.genreId = GenreId
        self.Name = Name

    def __str__(self):
        return self.Name

    def __hash__(self):
        return hash(self.Name)

    def __eq__(self, other):
        return self.Name == other.name



