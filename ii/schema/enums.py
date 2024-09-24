from enum import Enum


class StoryGenre(str, Enum):
    ACTION = "action"
    DRAMA = "drama"
    COMEDY = "comedy"
    HORROR = "horror"
    FANTASY = "fantasy"
    SCIFI = "sci-fi"
    ROMANCE = "romance"


class StoryLength(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    
    @classmethod
    def num_exchanges(cls, value: "StoryLength") -> int:
        lengths = {
            StoryLength.SHORT: 3,
            StoryLength.MEDIUM: 5,
            StoryLength.LONG: 10,
        }