from .MetaBase import ReadOnly
from .Types import Error

from aiohttp import ClientResponse, ClientResponseError
from json import loads


__all__ = (
    'ApiEndpoints',
    'ApiData',
    'jsonHandler'
)


async def jsonHandler(response: ClientResponse) -> dict | Error:
    try:
        result = await response.json()
    except ClientResponseError:
        result = loads(await response.text())
    if (r := result.get('error')) and isinstance(r, dict):
        return r
    if r := result.get('response'):
        return r
    return result


class ApiEndpoints(ReadOnly):
    """
    callreset - Звонок-сброс на привязанный номер
    push - push-уведомление на привязанное устройство
    sms - SMS на привязанный номер
    email - Получить код на почту
    """
    anonymToken = 'https://api.vk.com/oauth/get_anonym_token'
    validateAccount = 'https://api.vk.com/method/auth.validateAccount'
    verificationMethods = 'https://api.vk.com/method/ecosystem.getVerificationMethods'
    callreset = 'https://api.vk.com/method/ecosystem.sendOtpCallReset'
    sms = 'https://api.vk.com/method/ecosystem.sendOtpSms'
    push = 'https://api.vk.com/method/ecosystem.sendOtpPush'
    email = 'https://api.vk.com/method/ecosystem.sendOtpEmail'
    checkOTP = 'https://api.vk.com/method/ecosystem.checkOtp'
    authorize = 'https://oauth.vk.com/token'


class ApiData(ReadOnly):
    id_ = '2274003'
    data = {
        'api_id': id_,
        'device_id': '6d1d40620efe92cf:d8991c14ff38bf242a566a605444779e',
        'https': '1',
        'lang': 'ru',
        'v': '5.229',
    }
    data2 = {
        'sak_version': '1.120',
        'gaid': '89feec36-fcda-468a-afe0-5493cebb5c88'
    }
    anonymToken = {
        'client_id': id_,
        'client_secret': 'hHbZxrka2uZ6jB1inYsH'
    } | data
    validateAccount = {
        'login': '',
        'access_token': '',
        'force_password': '0',
        'supported_ways': 'push,email,sms,callreset,password,reserve_code,codegen,libverify',
        'flow_type': 'auth_without_password'
    } | data | data2
    verificationMethods = {
        'sid': '',
        'access_token': ''
    } | data
    sendOTP = {
        'sid': '',
        'access_token': ''
    } | data
    checkOTP = {
        'verification_method': '',
        'code': '',
        'sid': '',
        'access_token': '',
    } | data
    authorize = {
        'libverify_support': '1',
        'scope': 'all',
        'sid': '',
        'grant_type': 'phone_confirmation_sid',
        'username': '',
        'password': '',
        '2fa_supported': '1',
        'supported_ways': 'push,email',
        'anonymous_token': '',
        'flow_type': 'tg_flow'
    } | data | data2
    headers = {
        'user-agent': 'VKAndroidApp/8.71-19427 (Android 7.1.2; SDK 25; armeabi-v7a; samsung SM-G955N; ru; 1280x720)'
    }
