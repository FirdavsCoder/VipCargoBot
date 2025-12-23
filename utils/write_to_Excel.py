import asyncio
import os
import pandas as pd


async def write_to_excel_express_prognoz(user_id: int, price: str, track_code: str, product_name: str):
    file_path = 'express_prognoz.xlsx'
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        new_data = {
            'User ID': user_id,
            'Price': price,
            'Track Code': track_code,
            'Product Name': product_name
        }
        new_df = pd.DataFrame(new_data, index=[-1])
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = pd.DataFrame({
            'User ID': [user_id],
            'Price': [price],
            'Track Code': [track_code],
            'Product Name': [product_name]
        })
    combined_df.to_excel(file_path, index=False)


async def write_to_excel_cargo_prognoz(user_id: int, cargo_id: str, kub: int, kg: int, photo_id: str):
    file_path = 'cargo_prognoz.xlsx'
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        new_data = {
            'User ID': user_id,
            'Cargo ID': cargo_id,
            'KUB': kub,
            'KG': kg,
            'Photo ID': photo_id
        }
        new_df = pd.DataFrame(new_data, index=[0])
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = pd.DataFrame({
            'User ID': [user_id],
            'Cargo ID': [cargo_id],
            'KUB': [kub],
            'KG': [kg],
            'Photo ID': [photo_id]
        })
    combined_df.to_excel(file_path, index=False)


async def write_to_excel_cargo_id(
        user_id: int,
        cargo_id: str,
        phone_number: int,
        passport_id: str,
        region: str,
        full_name: str):
    file_path = 'cargo_id.xlsx'
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        new_data = {
            'User ID': user_id,
            'Cargo ID': cargo_id,
            'Full Name': full_name,
            'Phone number': phone_number,
            'Passport ID': passport_id,
            'Region': region
        }
        new_df = pd.DataFrame(new_data, index=[0])
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = pd.DataFrame({
            'User ID': [user_id],
            'Cargo ID': [cargo_id],
            'Full Name': [full_name],
            'Phone number': [phone_number],
            'Passport ID': [passport_id],
            'Region': [region]
        })
    combined_df.to_excel(file_path, index=False)


async def write_to_excel_express_id(
        user_id: int,
        cargo_id: str,
        phone_number: int,
        passport_id: str,
        region: str,
        full_name: str):
    file_path = 'express_id.xlsx'
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        new_data = {
            'User ID': user_id,
            'Express ID': cargo_id,
            'Full Name': full_name,
            'Phone number': phone_number,
            'Passport ID': passport_id,
            'Region': region
        }
        new_df = pd.DataFrame(new_data, index=[0])
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = pd.DataFrame({
            'User ID': [user_id],
            'Express ID': [cargo_id],
            'Full Name': [full_name],
            'Phone number': [phone_number],
            'Passport ID': [passport_id],
            'Region': [region]
        })
    combined_df.to_excel(file_path, index=False)
