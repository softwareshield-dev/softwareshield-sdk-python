__all__ = [
    "gsGetVersion", "gsInit", "gsInitEx", "gsFlush", "gsCleanUp", "gsCloseHandle", "gsGetLastErrorCode", "gsGetLastErrorMessage",

    "gsGetProductId", "gsGetProductName", "gsGetBuildId",
    
    "gsGetEntityCount","gsOpenEntityByIndex","gsOpenEntityById","gsGetEntityAttributes","gsGetEntityId","gsGetEntityName","gsGetEntityDescription","gsBeginAccessEntity","gsEndAccessEntity",

    "gsOpenLicense","gsGetLicenseId","gsGetLicenseName","gsGetLicenseDescription","gsGetLicenseStatus","gsIsLicenseValid","gsLockLicense","gsGetLicenseParamCount","gsGetLicenseParamByIndex",
    
    "gsGetVariable","gsGetVariableName","gsGetVariableType", "gsVariableTypeToString", "gsGetVariableAttr","gsIsVariableValid",
    "gsGetVariableValueAsString","gsSetVariableValueFromString","gsGetVariableValueAsInt","gsSetVariableValueFromInt",
    "gsGetVariableValueAsInt64","gsSetVariableValueFromInt64","gsGetVariableValueAsFloat","gsSetVariableValueFromFloat",
    "gsGetVariableValueAsDouble","gsSetVariableValueFromDouble","gsGetVariableValueAsTime","gsSetVariableValueFromTime",

    "gsCreateRequest", "gsAddRequestAction", "gsGetRequestCode",

    "gsGetActionInfoCount", "gsGetActionInfoByIndex",
    "gsGetActionName", "gsGetActionDescription", "gsGetActionDescription","gsGetActionParamCount","gsGetActionParamByIndex",

    "gsIsServerAlive", "gsApplySN", "gsIsSNValid","gsApplyLicenseCodeEx"
]

from .v5 import *