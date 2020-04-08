__all__ = [
    "gsGetVersion", "gsInit", "gsInitEx", "gsFlush", "gsCleanUp", "gsCloseHandle", "gsGetLastErrorCode", "gsGetLastErrorMessage",
    "gsGetProductId", "gsGetProductName", "gsGetBuildId",
    "gsGetEntityCount","gsOpenEntityByIndex","gsOpenEntityById","gsGetEntityAttributes","gsGetEntityId","gsGetEntityName","gsGetEntityDescription","gsBeginAccessEntity","gsEndAccessEntity"
]

from .v5 import *