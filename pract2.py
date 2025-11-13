import argparse
import os
import re
import sys
from urllib.parse import urlparse

def validate_args(args):
    errors = []

    # 1. Проверка имени пакета
    if not args.package_name or not re.match(r'^[A-Za-z0-9_.-]+$', args.package_name):
        errors.append("Некорректное имя пакета (допустимы буквы, цифры, '_', '-', '.')")

    # 2. Проверка URL или пути
    if args.repo_url.startswith(("http://", "https://", "git@")): 
        parsed = urlparse(args.repo_url) 
        if not parsed.scheme or not parsed.netloc:
            errors.append("Некорректный URL репозитория")
    else:
        if not os.path.exists(args.repo_url):
            errors.append(f"Файл или директория '{args.repo_url}' не существует")

    # 3. Проверка режима
    if args.mode not in ["local", "remote", "test"]:
        errors.append("Режим должен быть одним из: local, remote, test")

    # 4. Проверка имени выходного файла
    if not args.output_file.endswith((".png", ".svg", ".jpg")):
        errors.append("Имя выходного файла должно иметь расширение .png, .svg или .jpg")

    # 5. Проверка фильтра
    if args.filter and len(args.filter.strip()) == 0:
        errors.append("Пустая подстрока фильтра недопустима")

    return errors

parser = argparse.ArgumentParser(description="Прототип визуализатора графа зависимостей")

parser.add_argument("--package-name", required=True, help="Имя анализируемого пакета")
parser.add_argument("--repo-url", required=True, help="URL или путь к репозиторию")
parser.add_argument("--mode", required=True, help="Режим работы с тестовым репозиторием")
parser.add_argument("--output-file", required=True, help="Имя сгенерированного файла с изображением графа")
parser.add_argument("--filter", required=False, default="", help="Подстрока для фильтрации пакетов")

args = parser.parse_args()
errors = validate_args(args)

if errors:
    print("Обнаружены ошибки в параметрах:\n", file=sys.stderr)
    for err in errors:
        print(f" - {err}", file=sys.stderr)
    sys.exit(1)

print("Параметры конфигурации:")
print(f"package-name = {args.package_name}")
print(f"repo-url     = {args.repo_url}")
print(f"mode         = {args.mode}")
print(f"output-file  = {args.output_file}")
print(f"filter       = {args.filter or '(не задан)'}")
    
