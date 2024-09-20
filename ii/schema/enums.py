from enum import Enum


class StoryGenre(str, Enum):
    ACTION = "action"
    DRAMA = "drama"
    COMEDY = "comedy"
    HORROR = "horror"
    FANTASY = "fantasy"
    SCIFI = "scifi"
    ROMANCE = "romance"


class StoryLength(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
