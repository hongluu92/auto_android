import enum
class ActionType(str, enum.Enum):  # noqa: WPS600
    TAP = "tap"
    SWIPE = "swipe"
    TAP_BY_IMAGE = "tab_by_image"
    CHECK_BY_IMAGE = "check_by_image"
