import os
import logging
from django.conf import settings

# Создание основного логгера Django
django_logger = logging.getLogger("django")

# Создание логгера для безопасности
security_logger = logging.getLogger("django.security")

# Создание основного логгера приложения
app_logger = logging.getLogger("myapp")

# Уровень логирования для основного логгера Django
django_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Уровень логирования для логгера безопасности
security_logger.setLevel(logging.INFO)

# Уровень логирования для логгера приложения
app_logger.setLevel(logging.INFO)

# Создание форматтера для сообщений в консоль
console_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Создание форматтера для файловых логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)

# Запись в файл general.log
general_log_path = os.path.join(settings.LOG_DIR, "general.log")
general_log_handler = logging.FileHandler(general_log_path)
general_log_handler.setLevel(logging.INFO)
general_log_handler.setFormatter(file_formatter)

# Запись ошибок в файл errors.log
errors_log_path = os.path.join(settings.LOG_DIR, "errors.log")
errors_log_handler = logging.FileHandler(errors_log_path)
errors_log_handler.setLevel(logging.ERROR)
errors_log_handler.setFormatter(file_formatter)

# Создание хендлера для отправки ошибок на почту
if not settings.DEBUG:
    mail_handler = logging.handlers.SMTPHandler(
        mailhost=("smtp.example.com", 587),
        fromaddr="your_email@example.com",
        toaddrs=["admin@example.com"],
        subject="Django Error",
        credentials=("your_email@example.com", "your_email_password"),
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(file_formatter)

# Добавление хендлеров к логгерам
django_logger.addHandler(console_handler)
django_logger.addHandler(general_log_handler)
django_logger.addHandler(errors_log_handler)
if not settings.DEBUG:
    django_logger.addHandler(mail_handler)

security_logger.addHandler(console_handler)
security_logger.addHandler(errors_log_handler)

app_logger.addHandler(console_handler)


# Логирование сообщения о безопасности
security_logger.info("Security-related message")
