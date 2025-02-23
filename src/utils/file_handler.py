import os
import time
import pandas as pd

class FileHandler:
    @staticmethod
    def generate_filename(query):
        valid_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in query)
        valid_filename = valid_filename.strip().replace(' ', '_')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"{valid_filename}_{timestamp}.xlsx"

    @staticmethod
    def save_to_excel(articles, filename):
        df = pd.DataFrame(articles)
        df.to_excel(filename, index=False)
        print(f"Data saved to: {filename}")
        return filename

    @staticmethod
    def ensure_data_directory(folder_path):
        if not folder_path:
            folder_path = "data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path
