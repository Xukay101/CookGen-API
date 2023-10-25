from enum import Enum

class PreferenceType(str, Enum):
    ALLERGY = 'allergy'
    LIKE = 'like'
    DISLIKE = 'dislike'
