import logging
import os

from pyftpdlib.handlers import ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

from config import Config
from handlers import CustomHandler, CustomAuthorizer


def setup_logging(config: Config):
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )


def create_server(config: Config) -> FTPServer:
    """Creates and configures FTP server"""
    authorizer = CustomAuthorizer(config)
    
    # Configure handler class
    class ConfiguredHandler(CustomHandler):
        def __init__(self, conn, server, ioloop=None):
            super().__init__(conn, server, config=config, ioloop=ioloop)

    # Configure throttling
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = config.DTP_READ_LIMIT
    dtp_handler.write_limit = config.DTP_WRITE_LIMIT

    ConfiguredHandler.dtp_handler = dtp_handler
    ConfiguredHandler.authorizer = authorizer

    server = FTPServer((config.FTP_HOST, config.FTP_PORT), ConfiguredHandler)
    server.max_cons = config.MAX_CONNECTIONS
    server.max_cons_per_ip = config.MAX_CONNECTIONS_PER_IP

    return server


def main():
    config = Config.load()
    setup_logging(config)
    
    server = create_server(config)
    
    logging.info(f"Starting FTP server on {config.FTP_HOST}:{config.FTP_PORT}")
    server.serve_forever()


if __name__ == '__main__':
    main()
