from influxdb import InfluxDBClient

class InfluxDBTools:
    _default_retention_policy = {
        'name': 'default_retention_1_month',
        'duration': '30d',
        'replication': 1,
        'default': True
        
    }
    def __init__(self, host='localhost', port=8086, db_name='test_db', *args, **kwargs):
        self.db_name = db_name
        self.port = port
        self.host = host
        self.client = InfluxDBClient(host, port)
        self.client.switch_database(db_name)

        self.client.create_retention_policy(
            name=self._default_retention_policy['name'], duration=self._default_retention_policy['duration'], replication=self._default_retention_policy['replication'], database=self.db_name, default=False, shard_duration=u'12h')


    def write_points(self, json_body):
        self.client.write_points(
            json_body, retention_policy=self._default_retention_policy['name'])
