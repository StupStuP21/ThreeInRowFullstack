import os

import toml


class SettingsParser:
    def __init__(
            self, filepath: str = 'config.toml', db_name: str = "three-row-game", db_user: str = "postgres",
            db_pass: str = "user", db_host: str = "localhost", db_port: int = 5432,
            front_hosts: list[dict[str, str]] = None
    ):
        self.front_hosts = [
            {"protocol": "http", "host": "localhost", "port": "5173"},
            {"protocol": "http", "host": "127.0.0.1", "port": "5173"}
        ] if front_hosts is None else front_hosts
        self.filepath = filepath
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_pass
        self.db_host = db_host
        self.db_port = db_port

    def create_settings_file(self, replace_if_exist: bool = False) -> bool:
        if not replace_if_exist:
            if os.path.exists(self.filepath):
                return False
        with open(self.filepath, 'w') as file:
            toml.dump({'db_connection': {
                'db_name': self.db_name, 'db_user': self.db_user,
                'db_password': self.db_password, 'db_host': self.db_host,
                'db_port': self.db_port,
            },
                'front_connection': {
                    'hosts': [f'{host["protocol"]}://{host["host"]}:{host["port"]}' for host in self.front_hosts]
                }
            }, file)
        return True

    def get_settings(self) -> dict:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                settings = toml.load(file)
            return settings
        else:
            return {}
