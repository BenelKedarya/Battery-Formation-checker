import NewareNDA
import pandas as pd
import os
import json
from tkinter import Tk, filedialog


def convert_nda_to_serializable(input_files):
    result = []
    sizes = []
    errors = []
    for input_file in input_files:
        try:
            df = NewareNDA.read(input_file)
            df = pd.DataFrame(df)

            # Convert non-serializable types to strings
            df = df.apply(lambda x: x.map(lambda y: y.isoformat() if isinstance(y, pd.Timestamp) else y))

            # Get the size of the DataFrame
            num_rows, num_cols = df.shape
            sizes.append({'file': input_file, 'rows': num_rows, 'columns': num_cols})

            result.append(df.to_dict(orient='list'))
        except Exception as e:
            errors.append({'file': input_file, 'error': str(e)})

    return result, sizes, errors


def select_files():
    # Initialize tkinter
    root = Tk()
    root.withdraw()  # Hide the root window

    # File selection dialog
    input_files = filedialog.askopenfilenames(title='Select NDA Files', filetypes=[('NDAX Files', '*.ndax'),('NDA Files', '*.nda')])
    if not input_files:
        print('No files selected')
        return

    return input_files


if __name__ == "__main__":
    input_files = select_files()
    if input_files:
        data, sizes, errors = convert_nda_to_serializable(input_files)
        result = {'data': data, 'sizes': sizes, 'errors': errors}
        json_result = json.dumps(result)
        print(json_result)

#
# def log_file_metadata(file_path):
#     try:
#         file_size = os.path.getsize(file_path)
#         print(f"File size: {file_size} bytes")
#     except Exception as e:
#         print(f"Error getting file size for {file_path}: {e}")
#
#
# def convert_nda_to_serializable(input_files):
#     result = []
#     sizes = []
#     errors = []
#     for input_file in input_files:
#         print(f"Processing file: {input_file}")
#         log_file_metadata(input_file)
#
#         try:
#             # Try reading the file with more detailed logging
#             print("Attempting to read the file...")
#             df = NewareNDA.read(input_file)
#             print("File read successfully.")
#         except Exception as e:
#             print(f"Error reading file {input_file}: {e}")
#             errors.append({'file': input_file, 'error': f"Error reading file: {str(e)}"})
#             continue
#
#         try:
#             print("Converting to DataFrame...")
#             df = pd.DataFrame(df)
#             print(f"DataFrame shape: {df.shape}")
#         except Exception as e:
#             print(f"Error converting to DataFrame for file {input_file}: {e}")
#             errors.append({'file': input_file, 'error': f"Error converting to DataFrame: {str(e)}"})
#             continue
#
#         # Convert non-serializable types to strings
#         try:
#             print("Converting non-serializable types to strings...")
#             df = df.apply(lambda x: x.map(lambda y: y.isoformat() if isinstance(y, pd.Timestamp) else y))
#         except Exception as e:
#             print(f"Error converting non-serializable types for file {input_file}: {e}")
#             errors.append({'file': input_file, 'error': f"Error converting non-serializable types: {str(e)}"})
#             continue
#
#         # Get the size of the DataFrame
#         num_rows, num_cols = df.shape
#         sizes.append({'file': input_file, 'rows': num_rows, 'columns': num_cols})
#
#         result.append(df.to_dict(orient='list'))
#
#     return result, sizes, errors
#
#
# def select_files():
#     # Initialize tkinter
#     root = Tk()
#     root.withdraw()  # Hide the root window
#
#     # File selection dialog
#     input_files = filedialog.askopenfilenames(title='Select NDA Files', filetypes=[('NDA Files', '*.nda')])
#     if not input_files:
#         print('No files selected')
#         return
#
#     return input_files
#
#
# if __name__ == "__main__":
#     input_files = select_files()
#     if input_files:
#         data, sizes, errors = convert_nda_to_serializable(input_files)
#         result = {'data': data, 'sizes': sizes, 'errors': errors}
#         json_result = json.dumps(result, indent=4)
#         # print(json_result)
#
#         # Optionally, save the result to a file
#         with open('result.json', 'w') as f:
#             json.dump(result, f, indent=4)
