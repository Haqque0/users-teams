
import gspread
import csv
import sys
from oauth2client.service_account import ServiceAccountCredentials

# Настройки
SERVICE_ACCOUNT_FILE = 'service_account.json'
SHEET_NAME = "answers_test" # Укажи свое

def main():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME).get_worksheet(0)
        raw_data = sheet.get_all_values()
        
        if len(raw_data) < 2:
            print("❌ Таблица пуста")
            sys.exit(1)

        user_rows = [['name', 'email', 'password', 'team_id', 'role', 'verified', 'hidden', 'banned']]
        unique_teams = set()

        for row in raw_data[1:]:
            u_name, u_email, u_pwd, t_name = row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()
            if not t_name: t_name = "Individual"
            user_rows.append([u_name, u_email, u_pwd, t_name, 'user', 'true', 'false', 'false'])
            unique_teams.add(t_name)

        with open('users.csv', 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(user_rows)

        team_rows = [['name', 'email', 'password', 'hidden', 'banned']]
        for t in sorted(list(unique_teams)):
            team_rows.append([t, f"{t.lower().replace(' ','')}@ctf.local", f"{t}_pass2026", 'false', 'false'])
        
        with open('teams.csv', 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(team_rows)

        print(f"✅ Данные готовы: {len(user_rows)-1} юзеров, {len(team_rows)-1} команд.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
