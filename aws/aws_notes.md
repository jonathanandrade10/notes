## Boto3

### Refresh assume role tokens

In order to extend life of assumed role tokens, a role can be set to a maxSessionDuration of 12 hours (maximum) and to add custom durations DurationSeconds parameter needs to be set when using boto3.

Other options are, to create a credentials file or use the RefreshableCredentials boto3 class.

if using a **credentials file**

```
[profile profile_name]
role_arn = arn:aws:iam::123456789:role/role-name-here
credential_source = Ec2InstanceMetadata
```

then create a boto3 client like below

```
session = boto3.Session(profile_name='smallfiles') 
s3client = session.client('s3') 
```

if using RefreshableCredentials boto3 class. 

Source https://medium.com/@li.chastina/auto-refresh-aws-tokens-using-iam-role-and-boto3-afd3c52fd8c7 

```python
def _refresh(self):
    " Refresh tokens by calling assume_role again "
    params = {
        "RoleArn": self.role_name,
        "RoleSessionName": self.session_name,
        "DurationSeconds": 3600,
    }

    response = self.sts_client.assume_role(**params).get("Credentials")
    credentials = {
        "access_key": response.get("AccessKeyId"),
        "secret_key": response.get("SecretAccessKey"),
        "token": response.get("SessionToken"),
        "expiry_time": response.get("Expiration").isoformat(),
    }
    return credentials
```

then refer back to it as RefreshableCredentials metadata parameter

```python
from botocore.credentials import RefreshableCredentials
session_credentials = RefreshableCredentials.create_from_metadata(
    metadata=self._refresh(),
    refresh_using=self._refresh,
    method="sts-assume-role",
)
```

which can be used it in a boto3 session

```python
from boto3 import Session
from botocore.session import get_session
session = get_session()
session._credentials = session_credentials
session.set_config_variable("region", aws_region)
autorefresh_session = Session(botocore_session=session)

db_client = autorefresh_session.client("rds", region_name='us-east-1')

```
