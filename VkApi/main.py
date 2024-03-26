from aiohttp import ClientSession
from typing import Literal

from Utils import (
    ApiEndpoints,
    ApiData,
    jsonHandler,
    ValidateAccount,
    Error,
    AnonymToken,
    SendOTP,
    CheckOTP,
    VerificationMethods,
    WebToken
)


class Client:
    def __init__(self, login: str, password: str, api_version: str | float = '5.199') -> None:
        self.login = login
        self.password = password
        self.v = api_version
        self.cookies = {}

    async def anonymToken(self) -> AnonymToken | Error:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.anonymToken,
                data=ApiData.anonymToken,
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                return await jsonHandler(response)

    async def validateAccount(self, anonym_token: str) -> ValidateAccount | Error:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.validateAccount,
                data=((data := ApiData.validateAccount).update({'login': self.login, 'access_token': anonym_token}), data)[1],
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def verificationMethods(self, validation_sid: str, anonym_token: str) -> VerificationMethods | Error:
        """
        Метод должен обязательно вызываться перед тем, как подтверждать аккаунт другим способом (не через SMS)
        """
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.verificationMethods,
                data=((data := ApiData.validateAccount).update({'sid': validation_sid, 'access_token': anonym_token}), data)[1],
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def sendOtp(self, validation_sid: str, anonym_token: str, otp_type: Literal['callReset', 'sms', 'push', 'email']) -> SendOTP | Error:
        async with ClientSession() as session:
            async with session.post(
                url=getattr(ApiEndpoints, otp_type),
                data=((data := ApiData.sendOTP).update({'sid': validation_sid, 'access_token': anonym_token}), data)[1],
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def checkOtp(self, code: str | int, validation_sid: str, anonym_token: str, otp_type: Literal['callReset', 'sms', 'push', 'email']) -> CheckOTP | Error:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.checkOTP,
                data=((data := ApiData.checkOTP).update({'code': code, 'sid': validation_sid, 'access_token': anonym_token, 'verification_method': otp_type}), data)[1],
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def webToken(self, sid: str, anonym_token: str) -> WebToken:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.authorize,
                data=((data := ApiData.authorize).update({'username': self.login, 'password': self.password, 'sid': sid, 'anonymous_token': anonym_token}), data)[1],
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def auth(self) -> None:
        token = (await self.anonymToken()).get('token')
        validate = await self.validateAccount(token)
        validation_sid = validate.get('sid')
        otp_type = validate.get('next_step').get('verification_method')
        await self.sendOtp(validation_sid, token, otp_type)
        sid = (await self.checkOtp(input('code: '), validation_sid, token, otp_type)).get('sid')
        await self.webToken(sid, token)
