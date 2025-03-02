import os
import logging
import requests
from typing import Optional

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
from requests.exceptions import RequestException

from config import Config
from validators import FileValidator


class CustomAuthorizer(DummyAuthorizer):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.default_perms = 'elradfmw'

    def validate_authentication(self, username: str, password: str, handler: Optional[FTPHandler] = None) -> None:
        try:
            response = requests.post(
                self.config.DJANGO_AUTH_URL,
                json={'username': username, 'password': password},
                timeout=self.config.TIMEOUT
            )
            
            if response.status_code != 200:
                if handler:
                    handler.respond('530 Authentication failed - Invalid credentials')
                return
            
            is_staff = response.json().get('is_staff', False)
            if not is_staff:
                if handler:
                    handler.respond('530 Authentication failed - Insufficient permissions (must be staff)')
                return

        except RequestException as e:
            logging.error(f"Auth request failed: {str(e)}")
            if handler:
                handler.respond('530 Authentication failed - Service temporarily unavailable')
            return

    def get_home_dir(self, username: str) -> str:
        return os.getcwd()

    def has_user(self, username: str) -> bool:
        return True

    def get_perms(self, username: str) -> str:
        return self.default_perms

    def has_perm(self, username: str, perm: str, path: Optional[str] = None) -> bool:
        return perm in self.default_perms

    def get_msg_login(self, username):
        return "Welcome to Lukoil Discount FTP service"

    def get_msg_quit(self, username):
        return "Goodbye!"

    def impersonate_user(self, username, password):
        pass

    def terminate_impersonation(self, username):
        pass


class CustomHandler(FTPHandler):
    def __init__(self, conn, server, *, config: Config, ioloop=None):
        super().__init__(conn, server, ioloop=ioloop)
        self.config = config

    def on_connect(self) -> None:
        logging.info(f"Client connected: {self.remote_ip}")

    def on_disconnect(self) -> None:
        logging.info(f"Client disconnected: {self.remote_ip}")

    def on_file_received(self, file: str) -> None:
        try:
            validation_result = FileValidator.validate_csv(file)
            
            if not validation_result.is_valid:
                logging.info(f"File validation failed: {validation_result.message}")
                self.respond(f"553 File validation failed: {validation_result.message}")
                return

            self._upload_file(file)

        except Exception as e:
            logging.error(f"File processing error: {str(e)}")
        finally:
            os.remove(file)

    def _upload_file(self, file: str) -> None:
        with open(file, 'rb') as f:
            files = {'file': (os.path.basename(file), f)}
            try:
                response = requests.post(
                    self.config.DJANGO_UPLOAD_URL,
                    files=files,
                    timeout=self.config.TIMEOUT
                )
                if response.status_code == 201:
                    logging.info(f"File {file} successfully uploaded")
                else:
                    logging.error(f"Upload failed: {response.text}")
            except Exception as e:
                logging.error(f"Upload error: {str(e)}")
                raise
