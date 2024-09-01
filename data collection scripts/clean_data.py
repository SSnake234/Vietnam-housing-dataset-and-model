import pandas as pd

# Load the Excel file
file_path = 'Vietnam-housing-data/vietnam_housing_dataset.xlsx'
house_data = pd.read_excel(file_path)

print(f"Before: {house_data.shape}")
house_data = house_data.drop_duplicates()

# Only take rows where the Price has the word 'tỷ' (billion)
house_data = house_data[house_data['Price'].str.contains('tỷ', na=False)]

# Processing numerical features
house_data['Area'] = house_data['Area'].str.replace(' m²', '').str.replace('.', '').str.replace(',', '.').astype(float)
house_data['Frontage'] = house_data['Frontage'].str.replace(' m', '').str.replace(',', '.').astype(float)
house_data['Access Road'] = house_data['Access Road'].str.replace(' m', '').str.replace(',', '.').astype(float)
house_data['Floors'] = house_data['Floors'].str.replace(' tầng', '').astype(float)
house_data['Bedrooms'] = house_data['Bedrooms'].str.replace(' phòng', '').astype(float)
house_data['Bathrooms'] = house_data['Bathrooms'].str.replace(' phòng', '').astype(float)
house_data['Price'] = house_data['Price'].str.replace(' tỷ', '').str.replace(',', '.').astype(float)

# Processing categorical features
house_data['Legal status'] = house_data['Legal status'].fillna('None')
house_data['Legal status'] = house_data['Legal status'].apply(
    lambda x: 'Have certificate' 
                if 'sổ đỏ' in x.lower() 
                or 'sổ hồng' in x.lower()
                or 'đầy đủ' in x.lower()
    else 'Sale contract' if 'hợp đồng mua bán' in x.lower()
    else 'None'
)

house_data['Furniture state'] = house_data['Furniture state'].fillna('None')
house_data['Furniture state'] = house_data['Furniture state'].apply(
    lambda x: 'Full' 
                if 'đầy đủ' in x.lower()
                or 'full' in x.lower()
                or 'hết' in x.lower()
    else 'Basic' if 'cơ bản' in x.lower()
    else 'None'
)

# Filtering outliers (keep N/A values)
house_data = house_data[
    (house_data['Area'].isna() | (house_data['Area'] < 600)) &
    (house_data['Frontage'].isna() | (house_data['Frontage'] < 100)) &
    (house_data['Access Road'].isna() | (house_data['Access Road'] < 100)) &
    (house_data['Floors'].isna() | (house_data['Floors'] < 15)) &
    (house_data['Bedrooms'].isna() | (house_data['Bedrooms'] < 10)) &
    (house_data['Bathrooms'].isna() | (house_data['Bathrooms'] < 10)) &
    (house_data['Price'].isna() | (house_data['Price'] < 12))
]

print(f"After: {house_data.shape}")
house_data.to_excel('vietnam_housing_dataset_modified.xlsx', index=False)