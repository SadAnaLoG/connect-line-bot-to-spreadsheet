from oauth2client.service_account import ServiceAccountCredentials
import gspread

# If modifying these scopes, delete the file token.json.
scope = ['https://www.googleapis.com/auth/spreadsheets']


credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1h3jk5KxcPcY1Wt1qgwDOeXxRZz_h49MmIlz9Bs1KsEs/edit?usp=sharing")
worksheet = sheet.get_worksheet(0) # sheet index in spreadsheets

print(worksheet.get_all_values())
# worksheet.update_cell(1, 2, "BIDEN VOTES")
worksheet.update("A8:C8", [["Texas", 5261485, 5261485]])
worksheet.append_rows(values=[["Pennsylvania", 3458312, 3376499]])
# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1h3jk5KxcPcY1Wt1qgwDOeXxRZz_h49MmIlz9Bs1KsEs'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E14'

# def main():
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('sheets', 'v4', credentials=creds)

#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                 range=SAMPLE_RANGE_NAME).execute()
#     values = result.get('values', [])

#     if not values:
#         print('No data found.')
#     else:
#         print('Name, Major:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %s' % (row[0], row[4]))

# if __name__ == '__main__':
#     main()