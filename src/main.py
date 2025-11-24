from functions import *
import os
import shutil
import sys

def main():
    basepath = sys.argv[1] if sys.argv[1] else "/"
    copy_files(os.getcwd(), "static", "docs")
    generate_pages_recursive(os.path.join(os.getcwd(), "content"), os.path.join(os.getcwd(), "template.html"), os.path.join(os.getcwd(), "docs"), basepath)
    

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, f"{file.split(".")[0]}.html"), basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)

main()