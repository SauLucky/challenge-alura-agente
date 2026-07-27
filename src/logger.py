import logging
from src.config import Config

def get_corporate_logger():
    """Configura una bitácora única con formato homologado de nivel producción."""
    Config.LOGS_DIR.mkdir(exist_ok=True)
    log_file = Config.LOGS_DIR / "production.log"

    logger = logging.getLogger("RAG_Enterprise")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d]: %(message)s', 
            '%Y-%m-%d %H:%M:%S'
        )

        # Registro persistente en disco duro
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Despliegue en tiempo real en la consola de VS Code
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Instancia global reutilizable para todo el software
logger = get_corporate_logger()