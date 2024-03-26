from typing import TypedDict, NotRequired


__all__ = (
    'ValidateAccount',
    'Error',
    'AnonymToken',
    'SendOTP',
    'CheckOTP',
    'VerificationMethods',
    'WebToken'
)


class AnonymToken(TypedDict):
    token: str
    expired_at: int


class Param(TypedDict):
    key: str
    value: str


class Error(TypedDict):
    error_code: int
    error_msg: str
    error_text: str
    request_params: NotRequired[list[Param]]


class NextStep(TypedDict):
    verification_method: str
    has_another_verification_methods: bool


class ValidateAccount(TypedDict):
    flow_name: str
    flow_names: list[str]
    is_email: bool
    next_step: NotRequired[NextStep]
    remember_hash: str
    sid: str


class VerificationMethod(TypedDict):
    can_fallback: bool
    info: str
    name: str
    priority: int
    timeout: int


class VerificationMethods(TypedDict):
    methods: list[VerificationMethod]


class SendOTP(TypedDict):
    status: int
    sid: str
    code_length: int
    info: str


class Profile(TypedDict):
    first_name: str
    last_name: str
    has_2fa: bool
    photo_200: str
    phone: str
    can_unbind_phone: bool


class SignupParams(TypedDict):
    password_min_length: int
    birth_date_max: str


class CheckOTP(TypedDict):
    sid: str
    profile_exist: bool
    can_skip_password: bool
    signup_restriction_reason: str
    profile: Profile
    signup_fields: list[str]
    signup_params: SignupParams


class WebToken(TypedDict):
    access_token: str
    expires_in: int
    user_id: int
    trusted_hash: str
    webview_refresh_token: str
    webview_refresh_token_expires_in: int
    webview_access_token: str
    webview_access_token_expires_in: int
