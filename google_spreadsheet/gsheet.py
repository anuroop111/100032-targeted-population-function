from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class GSpreadSheet:

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'pythonanywhere@quickstart-1616091302695.iam.gserviceaccount.com.json'

    def __init__(self, spreadsheet_id):


        creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        self.service = build('sheets', 'v4', credentials=creds)
        self.spreadsheet_id=spreadsheet_id




    def appendNewRow(self, _range, values):



        body = {
                "majorDimension": "ROWS",
                'values': values,
        }

        result = self.service.spreadsheets().values().append(
        spreadsheetId=self.spreadsheet_id, range=_range,
        valueInputOption="RAW", body=body).execute()
        #print('{0} cells updated.'.format(result.get('updatedCells')))


    def fetch_data_by_updating_lookup_sheet(self, col_val):


        ''' "=FILTER(Marks!A2:E100,Marks!A2:A100>date(2021,1,3),Marks!A2:A100<date(2021,3,10))" '''
    

        update_spreadsheet_request_body={

            "values": [
                [
                    #=MATCH("1234567890123456", team member rights_tran!B:B, 0)
                   col_val
                ]



            ]
        }
        _range="LOOKUP_SHEET_1!A1:E"
        request = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,includeValuesInResponse=True,valueInputOption="USER_ENTERED", range=_range, body=update_spreadsheet_request_body)
        response = request.execute()
        print(response)


        row_index=response['updatedData']['values'][0][0]

        return row_index


    def searchRowIndex(self,sheetName,columnIndex, columnValue):


        col_val= '=MATCH('+columnValue +','+sheetName+'!'+columnIndex+':'+columnIndex+ ',0)'
        #print("col_val:: "+col_val)

        update_spreadsheet_request_body={

            "values": [
                [
                    #=MATCH("1234567890123456", team member rights_tran!B:B, 0)
                    col_val
                ]



            ]
        }
        _range="LOOKUP_SHEET_1!A1"
        request = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,includeValuesInResponse=True,valueInputOption="USER_ENTERED", range=_range, body=update_spreadsheet_request_body)
        response = request.execute()
        #print(response)


        row_index=response['updatedData']['values'][0][0]

        return row_index



    def getRowFromIndex(self, sheetName, row_index, row_start, row_end):

            print("start: "+sheetName)

            _range=sheetName+'!'+row_start+row_index+':'+row_end+row_index

            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=_range).execute()
            #print(result)

            row_array = result.get('values', [])[0]

            if not row_array:
                print('error!. No data found.')
                return


            print(row_array)
            #print("end: "+sheetName)

            return row_array


    def updateRow(self, sheetName, row_index, row_start, row_end,data):

        _range=sheetName+'!'+row_start+row_index+':'+row_end+row_index
        values=[
            data


        ]

        value_input_option = 'RAW'  # TODO: Update placeholder value.



        body = {

                "majorDimension": "ROWS",
                'values': values,

        }

        request = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=_range, valueInputOption=value_input_option, body=body)
        response = request.execute()

        return response


    #batch_update_spreadsheet_request_body={
    #    "requests": [
    #            {
    #                "addSheet": {
    #                    "properties": {
    #                    "hidden": False,
    #                    "title": "LOOKUP_SHEET_1"
    #                    }
    #                }
    #            }

    #    ],

    #}

    #request = service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_update_spreadsheet_request_body)
    #response = request.execute()
