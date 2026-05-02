import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TOKEN_PATH = os.path.expanduser('~/.hermes/google_token.json')

def main():
    with open(TOKEN_PATH) as f:
        creds_info = json.load(f)
    
    creds = Credentials.from_authorized_user_info(creds_info)
    
    sheets_service = build('sheets', 'v4', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)

    # 1. Create Spreadsheet
    spreadsheet = {
        'properties': {
            'title': '待辦事項庫_Stable'
        }
    }
    sheet_metadata = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    sheet_id = sheet_metadata.get('spreadsheetId')
    
    # Get the default sheet name (usually '工作表1' or 'Sheet1')
    spreadsheet_detail = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    sheet_name = spreadsheet_detail['sheets'][0]['properties']['title']
    print(f"Created Sheet ID: {sheet_id}, Sheet Name: {sheet_name}")

    # 2. Set Headers
    headers = [["任務名稱", "到期日", "狀態", "優先級"]]
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}!A1:D1",
        valueInputOption="RAW",
        body={"values": headers}
    ).execute()

    # 3. Data to sync
    tasks = [
        ["🏠 訂民宿", "2026-05-11", "進行中", "中"],
        ["📸 拍全家福", "2026-05-19", "進行中", "中"],
        ["🍽 逐鹿用餐 12:00", "2026-05-20", "進行中", "中"],
        ["🎁 準備太太生日禮物", "2026-05-21", "進行中", "中"]
    ]

    # Append tasks
    sheets_service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}!A2",
        valueInputOption="RAW",
        body={"values": tasks}
    ).execute()

    # 4. Create Calendar Events
    for task in tasks:
        event = {
            'summary': task[0],
            'start': {'date': task[1]},
            'end': {'date': task[1]},
            'description': f'狀態: {task[2]}, 優先級: {task[3]}'
        }
        calendar_service.events().insert(calendarId='primary', body=event).execute()

    print(f"SUCCESS: All tasks synced to Sheet ({sheet_id}) and Calendar!")

if __name__ == "__main__":
    main()
