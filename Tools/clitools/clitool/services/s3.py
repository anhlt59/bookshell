from clitool.services.base import AwsService
from clitool.types.s3 import S3Bucket


class S3Service(AwsService):
    def list_bucket(self, prefix: str) -> list[S3Bucket]:
        response = self.session.client("s3").list_buckets()
        buckets = []
        for item in response.get("Buckets"):
            if prefix and not item.get("Name", "").startswith(prefix):
                continue
            buckets.append(S3Bucket(name=item["Name"], creation_date=item.get("CreationDate")))
        return buckets
