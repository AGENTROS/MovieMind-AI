import os
import ssl
import urllib.request
import zipfile

def download_and_extract_movielens():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    zip_path = os.path.join(data_dir, 'ml-latest-small.zip')
    url = 'https://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
    
    print(f"Downloading MovieLens dataset from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    # Bypass local SSL verification issue
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, context=ctx) as response, open(zip_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    print("Download completed! Extracting...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
        
    extracted_folder = os.path.join(data_dir, 'ml-latest-small')
    if os.path.exists(extracted_folder):
        for file_name in os.listdir(extracted_folder):
            src = os.path.join(extracted_folder, file_name)
            dst = os.path.join(data_dir, file_name)
            if os.path.exists(dst):
                os.remove(dst)
            os.rename(src, dst)
        os.rmdir(extracted_folder)
        
    if os.path.exists(zip_path):
        os.remove(zip_path)
        
    print(f"Dataset successfully extracted into {data_dir}!")
    for f in os.listdir(data_dir):
        print(" -", f)

if __name__ == '__main__':
    download_and_extract_movielens()
