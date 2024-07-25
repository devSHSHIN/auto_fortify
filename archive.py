import os
import zipfile
import shutil

def zip_files_in_tmp(output_zip_path):
    tmp_dir = '.tmp'
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                if file.endswith('.xlsx') or file.endswith('.fpr'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.basename(file_path))
    os.chmod(output_zip_path, 0o775)
    shutil.rmtree(tmp_dir)