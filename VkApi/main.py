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
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
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
                data=ApiData.validateAccount | {'login': self.login, 'access_token': anonym_token},
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def verificationMethods(self, validation_sid: str, anonym_token: str) -> VerificationMethods | Error:
        """
        Метод должен обязательно вызываться перед тем, как подтверждать аккаунт другим способом
        """
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.verificationMethods,
                data=ApiData.validateAccount | {'sid': validation_sid, 'access_token': anonym_token},
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def sendOTP(self, validation_sid: str, anonym_token: str, otp_type: Literal['callreset', 'sms', 'push', 'email']) -> SendOTP | Error:
        async with ClientSession() as session:
            async with session.post(
                url=getattr(ApiEndpoints, otp_type),
                data=ApiData.sendOTP | {'sid': validation_sid, 'access_token': anonym_token},
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def checkOTP(self, code: str | int, validation_sid: str, anonym_token: str, otp_type: Literal['callreset', 'sms', 'push', 'email']) -> CheckOTP | Error:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.checkOTP,
                data=ApiData.checkOTP | {'code': code, 'sid': validation_sid, 'access_token': anonym_token, 'verification_method': otp_type},
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def webToken(self, sid: str, anonym_token: str) -> WebToken | Error:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.authorize,
                data=ApiData.authorize | {'username': self.login, 'password': self.password, 'sid': sid, 'anonymous_token': anonym_token},
                headers=ApiData.headers,
                cookies=self.cookies
            ) as response:
                self.cookies.update(response.cookies)
                return await jsonHandler(response)

    async def auth(self) -> None:
        anonym_token = (await self.anonymToken()).get('token')
        validate = await self.validateAccount(anonym_token)
        validation_sid = validate.get('sid')
        otp_type = validate.get('next_step').get('verification_method')
        await self.sendOTP(validation_sid, anonym_token, otp_type)
        await self.verificationMethods(validation_sid, anonym_token)
        sid = (await self.checkOTP(input('code: '), validation_sid, anonym_token, otp_type)).get('sid')
        print(await self.webToken(sid, anonym_token))
        print(self.cookies)
