import requests
import csv
import os

# Конфигурация
OAUTH_TOKEN = "токен"
ORG_ID = "id организации"
SURVEY_ID = "id формы"
API_URL = f"https://api.forms.yandex.net/v1/surveys/{SURVEY_ID}/answers"

def fetch_all_answers():
    headers = {
        "Authorization": f"OAuth {OAUTH_TOKEN}",
        "X-Org-ID": ORG_ID
    }
    # Оставляем 50 для реальной работы, или 1 для теста
    params = {"page_size": 50}
    all_answers = []
    url = API_URL

    while url:
        print(f"📡 Запрос к: {url}")
        # Если url уже содержит параметры (из next_url), дополнительные params не шлем
        current_params = params if url == API_URL else None
        response = requests.get(url, headers=headers, params=current_params)
        
        if response.status_code != 200:
            print(f"❌ Ошибка API: {response.status_code}")
            print(response.text)
            break
        
        data = response.json()
        all_answers.extend(data.get("answers", []))
        
        # Обработка перехода на следующую страницу
        next_data = data.get("next")
        if next_data and next_data.get("next_url"):
            next_url = next_data.get("next_url")
            
            # 1. Делаем ссылку полной, если она пришла относительной
            if not next_url.startswith('http'):
                next_url = f"https://api.forms.yandex.net{next_url}"
            
            # 2. ФИКС: Принудительно возвращаем v1 вместо v3, чтобы не было 404
            if "/v3/" in next_url:
                next_url = next_url.replace("/v3/", "/v1/")
            
            url = next_url
        else:
            url = None
            
    return all_answers

def process_data(answers):
    answers.reverse() 
    
    users_data = []
    teams_list = [] # Используем список для сохранения порядка команд
    
    for ans in answers:
        d = ans.get("data", [])
        if len(d) >= 4:
            name = d[0].get("value")
            email = d[1].get("value")
            password = d[2].get("value")
            team_name = d[3].get("value")
            
            # Формат для CTFd: name,email,password,team_id,role,verified,hidden,banned
            users_data.append([
                name, email, password, team_name, "user", "true", "false", "false"
            ])
            
            # Собираем уникальные команды в порядке их появления
            if team_name and team_name not in teams_list:
                teams_list.append(team_name)
    
    return users_data, teams_list

def save_csv_files(users, teams):
    # Запись участников
    with open('users.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'email', 'password', 'team_id', 'role', 'verified', 'hidden', 'banned'])
        writer.writerows(users)
    print(f"✅ Создан users.csv: {len(users)} пользователей")

    # Запись команд
    with open('teams.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'email', 'password', 'hidden', 'banned'])
        
        for i, team_name in enumerate(teams, start=1):
            team_email = f"team{i}@ctf.local"
            team_pass = f"{team_name}_pass2026"
            writer.writerow([team_name, team_email, team_pass, "false", "false"])
    print(f"✅ Создан teams.csv: {len(teams)} уникальных команд")

if __name__ == "__main__":
    print("📥 Загрузка данных из Яндекс...")
    raw_answers = fetch_all_answers()
    
    if raw_answers:
        users, teams = process_data(raw_answers)
        save_csv_files(users, teams)
        print("🚀 Обработка успешно завершена!")
    else:
        print("📭 Ответы не найдены.")
