from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError


class InfluxDBTools:
    _default_retention_policy = {
        'name': 'default_retention_1_week',
        'duration': '7d',
        'replication': 1,
        'default': False,
        'shard_duration':'12h',

    }

    def __init__(self, host, port, db_name, *args, **kwargs):
        self.db_name = db_name
        self.port = port
        self.host = host
        self.default_retention_policy_name = self._default_retention_policy['name']
        self.client = InfluxDBClient(host, port)
        self.client.create_database(db_name)
        self.client.switch_database(db_name)
        try:
            self.client.create_retention_policy(
                name=self._default_retention_policy['name'],
                duration=self._default_retention_policy['duration'],
                replication=self._default_retention_policy['replication'],
                database=self.db_name, default=self._default_retention_policy['default'],
                shard_duration=self._default_retention_policy['shard_duration']
                )
        except InfluxDBClientError as e:
            if str(e) == 'retention policy already exists':
                print('Policy Already Exists ...')
            else:
                raise e

    def write_points(self, json_body):
        self.client.write_points(
            json_body, retention_policy=self.default_retention_policy_name)
