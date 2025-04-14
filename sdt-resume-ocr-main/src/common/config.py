from src.utils import get_env


class DBConfig:
    def __init__(self):
        self.host = get_env('DB_HOST')
        self.database = get_env('DB_DATABASE')
        self.username = get_env('DB_USERNAME')
        self.password = get_env('DB_PASSWORD')
        self.port = get_env('DB_PORT')


class KafkaConfig:
    def __init__(self):
        self.bootstrap_servers = get_env('KAFKA_BOOTSTRAP_SERVERS')
        self.group_id = get_env('KAFKA_GROUP_ID')


class MinioConfig:
    def __init__(self):
        self.endpoint = get_env('MINIO_ENDPOINT')
        self.access_key = get_env('MINIO_ACCESS_KEY')
        self.secret_key = get_env('MINIO_SECRET_KEY')


class Config:
    def __init__(self):
        self.kafka_config = KafkaConfig()
        self.db_config = DBConfig()
        self.minio_config = MinioConfig()
