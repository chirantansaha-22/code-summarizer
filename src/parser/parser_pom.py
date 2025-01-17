import os
import xml.etree.ElementTree as ET
from colorama import Style, Fore

def parse_pom(pom_file_path):
    
    tree = ET.parse(pom_file_path)
    root = tree.getroot()

    # Define the XML namespace (commonly "http://maven.apache.org/POM/4.0.0")
    namespace = {'mvn': 'http://maven.apache.org/POM/4.0.0'}

    # Extract artifact details
    group_id = root.find('mvn:groupId', namespace)
    artifact_id = root.find('mvn:artifactId', namespace)
    version = root.find('mvn:version', namespace)

    # Extract modules (if present)
    modules = root.find('mvn:modules', namespace)
    
    module_list = [module.text for module in modules] if modules is not None else []

    return {
        "groupId": group_id.text if group_id is not None else None,
        "artifactId": artifact_id.text if artifact_id is not None else None,
        "version": version.text if version is not None else None,
        "modules": module_list
    }


def explore_directory(repo_path):
    project_structure = {}
    for root, dirs, files in os.walk(repo_path):
        #print(Fore.LIGHTGREEN_EX,f"root: {Style.RESET_ALL}{root} {Fore.LIGHTRED_EX}|Directory: {Style.RESET_ALL} {dirs} {Fore.LIGHTYELLOW_EX}|File: {Style.RESET_ALL}{files}")
        dirs[:] = [dir for dir in dirs if dir not in [".git"]]

        if "pom.xml" in files:
            pom_file_path = os.path.join(root,"pom.xml")
            #print(pom_file_path)
            module_info = parse_pom(pom_file_path)

            # Store module information
            relative_path = os.path.relpath(root, repo_path)
            project_structure[relative_path] = module_info

    return project_structure
    

# Define the repo path that contains the code
code_repo_path = "E:/Chirantan/Projects/bank/spring-boot-microservices"
project_structure = explore_directory(code_repo_path)

# Display the structure
for path, info in project_structure.items():
    print(f"Module Path: {path}")
    print(f"  ArtifactId: {info['artifactId']}")
    print(f"  GroupId: {info['groupId']}")
    print(f"  Version: {info['version']}")
    print(f"  Submodules: {info['modules']}")
    print()
