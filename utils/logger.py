import logging
import sys
import os


def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 🔸 Формат логов
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 🔸 Поток в консоль
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # 🔸 Поток в файл
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)  # Создаём папку logs, если нет

        file_handler = logging.FileHandler(
            f"{log_dir}/test.log", mode="a", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
