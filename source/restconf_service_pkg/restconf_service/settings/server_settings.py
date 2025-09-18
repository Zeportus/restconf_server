from pathlib import Path

from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    yang_config_path: Path
    yang_library_path: Path
    yang_modules_dir_path: Path
    server_host: str
    server_port: int
