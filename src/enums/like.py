import enum


class LikeChoiceType(str, enum.Enum):
    Genre = "Genre"
    Performer = "Performer"
    Performance = "Performance"
