from enum import Enum


class StoryGenre(str, Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    HORROR = "Horror"
    FANTASY = "Fantasy"
    SCIFI = "Sci-fi"
    ROMANCE = "Romance"


class StoryLength(str, Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"

    @classmethod
    def num_exchanges(cls, value: "StoryLength") -> int:
        lengths = {
            StoryLength.SHORT: 3,
            StoryLength.MEDIUM: 7,
            StoryLength.LONG: 15,
        }
