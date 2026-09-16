from backend.aws.s3 import S3Manager

class S3Check:

    def __init__(self):
        self.s3 = S3Manager()

    def check_buckets(self):

        buckets = self.s3.list_buckets()

        results = []

        for bucket in buckets:

            results.append({
                "name": bucket["Name"],
                "created": str(bucket["CreationDate"])
            })

        return results