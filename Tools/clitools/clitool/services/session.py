import boto3

from clitool.base import SingletonMeta
from clitool.console import console
from clitool.settings import AWS_DEFAULT_PROFILE, AWS_IGNORED_PROFILES
from clitool.types.session import Credentials, Profile
from clitool.utils import execute_command, mfa_compiler


class SessionService(metaclass=SingletonMeta):
    profile: Profile
    session: boto3.Session

    def __init__(self, profile_name: str = AWS_DEFAULT_PROFILE):
        self.profile = self.get_profile(profile_name)
        self.session = boto3.Session(profile_name=self.profile.name)

    def client(self, *args, **kwargs) -> boto3.client:
        return self.session.client(*args, **kwargs)

    def resource(self, *args, **kwargs) -> boto3.resource:
        return self.session.resource(*args, **kwargs)

    def get_profile(self, name: str = AWS_DEFAULT_PROFILE, lazy=True) -> Profile:
        session = boto3.Session(profile_name=name)
        credentials = session.get_credentials()
        profile = Profile(
            name=session.profile_name,
            region=session.region_name,
            credentials=Credentials(
                aws_access_key_id=credentials.access_key,
                aws_secret_access_key=credentials.secret_key,
                aws_session_token=credentials.token,
            ),
        )
        if not lazy:
            identity = session.client("sts").get_caller_identity()
            profile.user_id = identity.get("UserId")
            profile.account = identity.get("Account")
            profile.arn = profile.credentials.aws_arn = identity.get("Arn")
        return profile

    def list_profiles(self) -> list[Profile]:
        profiles = []
        for profile_name in self.session.available_profiles:
            if profile_name not in AWS_IGNORED_PROFILES:
                try:
                    profile = self.get_profile(profile_name)
                except Exception as e:
                    console.log(f"Profile {profile_name} is inactive: {e}", style="red")
                else:
                    profiles.append(profile)
        return profiles

    def switch_profile(self, name: str) -> Profile:
        if self.profile.name != name:
            self.profile = self.get_profile(name, False)
            self.session = boto3.Session(profile_name=name)
        return self.profile

    def set_credentials(self, credentials: Credentials) -> Profile:
        self.profile.credentials = credentials
        self.session = boto3.Session(
            aws_access_key_id=credentials.aws_access_key_id,
            aws_secret_access_key=credentials.aws_secret_access_key,
            aws_session_token=credentials.aws_session_token,
            region_name=self.profile.region,
        )
        return self.profile

    def assume_role(self, arn: str) -> Credentials:
        if not arn:
            raise ValueError("RoleArn is required")
        if mfa_compiler.match(arn):
            # self.session.client("sts").assume_role(SerialNumber=arn, TokenCode=mfa_token, RoleSessionName="clitool")
            raise ValueError("Does not support MFA serial number this version")

        response = self.session.client("sts").assume_role(RoleArn=arn, RoleSessionName="session")
        if credentials := response.get("Credentials"):
            return Credentials(
                aws_arn=arn,
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
                aws_expiration=credentials["Expiration"],
            )
        else:
            raise Exception("Failed to assume role")

    def get_session_token(self, anr: str, mfa_token: str) -> Credentials:
        if not anr or not mfa_token:
            raise ValueError("SerialNumber and MFA code are required")

        # cannot call GetSessionToken with session credentials, so that use a new session with current profile
        session = boto3.Session(profile_name=self.profile.name)
        response = session.client("sts").get_session_token(SerialNumber=anr, TokenCode=mfa_token)
        if credentials := response.get("Credentials"):
            return Credentials(
                aws_arn=anr,
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
                aws_expiration=credentials["Expiration"],
            )
        else:
            raise Exception("Failed to assume role")

    def store_aws_config_file(self, profile: Profile, name: str = AWS_DEFAULT_PROFILE):
        aws_access_key_id = profile.credentials.aws_access_key_id
        aws_secret_access_key = profile.credentials.aws_secret_access_key
        aws_session_token = profile.credentials.aws_session_token

        execute_command(f"aws configure set output json --profile {name}")
        execute_command(f"aws configure set region {profile.region} --profile {name}")
        execute_command(f"aws configure set aws_access_key_id {aws_access_key_id} --profile {name}")
        execute_command(f"aws configure set aws_secret_access_key {aws_secret_access_key} --profile {name}")
        if aws_session_token:
            execute_command(f"aws configure set aws_session_token {aws_session_token} --profile {name}")
