# import os
#
# import pandas as pd
# from datetime import datetime
#
#
# async def id_excel_writer(data: list):
#     df = pd.DataFrame(data)
#     print(1.1)
#     today_date = datetime.today().strftime('%Y-%m-%d')
#     file_name = f'id_excel{today_date}.xlsx'
#     print(file_name)
#     print(1.2)
#     df.to_excel(file_name, index=False)
#     print(1.3)
#
#     return file_name
