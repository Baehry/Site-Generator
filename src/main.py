from functions import *
import os
import shutil

def main():
    copy_files(os.getcwd(), "static", "public")
    generate_page(os.path.join(os.getcwd(), "content/index.md"), os.path.join(os.getcwd(), "template.html"), os.path.join(os.getcwd(), "public/index.html"))

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(page)
    
    

main()