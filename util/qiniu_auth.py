from qiniu import Auth,BucketManager,put_data

access_key = "hVeOAldZ7OdLUTA8Wyunu2oeCPGhOlGqpIHOhF_H"
secret_key = "nH9k4WvK4xfSLWqDwDdqFVx2CVcJf59iI0KzAQCp"
BASE_URL = "http://cache.lhananld.xyz/"

def get_qiu_auth():
    return Auth(access_key, secret_key)

def get_bucket(bucket_name="liuhui-12",prefix=""):
    q = get_qiu_auth()
    bucket = BucketManager(q)
    limit = 10
    # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
    delimiter = None
    # 标记
    marker = None
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)

    return [BASE_URL+o["key"] for o in ret["items"]]


def upload_data(key,data):
    q = get_qiu_auth()
    token = q.upload_token("liuhui-12")
    info = put_data(token,key,data)

