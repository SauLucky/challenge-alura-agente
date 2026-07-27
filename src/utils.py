import logging
from src.config import Config

def setup_logger():
    """Configura un sistema de logging profesional dual (Consola y Archivo)."""
    Config.LOGS_DIR.mkdir(exist_ok=True)
    log_file = Config.LOGS_DIR / "app.log"

    logger = logging.getLogger("RAG_Agent")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d]: %(message)s', '%Y-%m-%d %H:%M:%S')

        # Handler para guardar en archivo físico
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler para mostrar limpio en la terminal de VS Code
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Inicializamos el logger global del sistema
logger = setup_logger()