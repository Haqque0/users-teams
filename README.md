# users-teams

# Автоматизированный сбор данных из форм (Google / Yandex)

## Состав проекта
* `google_script.py` — сбор данных из Google форм.
* `yandex_script.py` — сбор данных из Яндекс Форм.
* `run.sh` — скрипт запуска.

---

## 1. Google Script (`google_script.py`)
Использует Service Account для доступа к данным. Для работы необходим json файл (service_account.json) от сервисного аккаунта, у которого есть доступ к таблице от гугл формы.

### Подготовка гугл формы
1. Привяжите форму к Google Таблице.
2. В [Google Cloud Console](https://console.cloud.google.com/):
   - Создайте проект.
   - Включите **Google Sheets API** и **Google Drive API**.
   - В разделе [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) создайте аккаунт с ролью **Editor**.
   - Вкладка **Keys** -> **Add Key** -> **Create new key** -> (JSON). Скачайте файл.
3. В самой Google Таблице нажмите «Поделиться» и добавьте email сервисного аккаунта с правами **Editor**.

### Настройка кода
В файле `google_script.py` измените:
- `SERVICE_ACCOUNT_FILE` — путь к вашему JSON-файлу (по дефолту `service_account.json`).
- `SHEET_NAME` — точное название таблицы.

**Выходные файлы:** `users.csv` и `teams.csv`.

---

## 2. Yandex Script (`yandex_script.py`)
Работает только с формой из категории **«Формы для бизнеса»**.

### Подготовка (Yandex)
1. **OAuth-токен:** Создайте приложение на [oauth.yandex.ru](https://oauth.yandex.ru/). 
   - Тип: «Для доступа к API или отладки».
   - Доступ к данным: `forms:read` и `forms:write`.
   - В созданном приложении скопируйте ClientID. После перейдите по ссылке, вставив в нее скопированный ID: `https://oauth.yandex.ru/authorize?response_type=token&client_id=ВАШ_ID`.
2. **ID Организации:** берется в [профиле организации](https://center.yandex.cloud/).
3. **ID Формы:** берется из URL ссылки на форму, пример: `https://forms.yandex.ru/cloud/admin/ID_ФОРМЫ/edit`.

### Настройка кода
В файле `yandex_script.py` измените:
- `OAUTH_TOKEN` — OAuth-токен.
- `ORG_ID` — ID организации.
- `SURVEY_ID` — ID формы.

**Выходные файлы:** `users.csv` и `teams.csv`.

---

## 3. run.sh
Устанавливает необходимые библиотеки, по порядку запускает `google_script.py` или `yandex_script.py` в зависимости от выбора платформы, после запускает `auto-setup.py`.

### Необходимые пакеты в системе
* `python3-pip`
* `python3-venv`

### Настройка кода
- `PLATFORM` — вписывать "yandex" или "google".

### Настройка и использование
1. Переместите файлы в рабочую директорию (например, в папку с CTFd):
   ```bash
   mv auto-setup.py yandex_script.py google_script.py run.sh ctfd-config.json service_account.json ctfd/
2. Запустить run.sh
   ```bash
   ./run.sh
