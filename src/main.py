from functions import *
import os
import shutil

def main():
    copy_files(os.getcwd(), "static", "public")

def copy_files(working_directory, source_directory, destination_directory):
    source_path = os.path.join(working_directory, source_directory)
    dest_path = os.path.join(working_directory, destination_directory)
    if not (source_path.startswith(working_directory) and dest_path.startswith(working_directory)):
        raise Exception("illegal directory")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    if os.path.isfile(source_path):
        shutil.copy(source_path, dest_path)
        return
    os.mkdir(dest_path)
    files = os.listdir(source_path)
    for file in files:
        copy_files(working_directory, os.path.join(source_directory, file), os.path.join(destination_directory, file))

main()