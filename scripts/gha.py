import os
import re
import pandas as pd
from tabulate import tabulate

# Define the directory containing the .conf files
script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)
conf_directory = parent_directory + "/syslog-ng/conf.d/integrations"
github_repo_url = "https://github.com/objectbased/readme-tester/blob/main/syslog-ng/conf.d/integrations/"

# Define the regex pattern to extract information from the conf files
pattern = r'input\( source\((\w+)\) port\((\w+)\) protocol\("(\w+)"\)(?:.*?protocol2\("(\w+)"\))?'
comments = r'Comments\:(.*?)\n'
apps = r'Apps:(.*?)\n'

# Create an empty DataFrame to store the extracted data
data = []

# Iterate through .conf files in the directory
for filename in os.listdir(conf_directory):
    if filename.endswith(".conf"):
        with open(os.path.join(conf_directory, filename), 'r') as file:
            content = file.read()
            matches = re.findall(pattern, content)
            comments_match = re.findall(comments, content)
            apps_match = re.findall(apps, content)
            for match, comment, app in zip(matches, comments_match, apps_match):
                source, port, protocol, protocol2 = match
                if protocol2:
                    protocol = f"{protocol},{protocol2}"
                file_url = github_repo_url + filename
                syslog_path = "/var/log/forward/%s/${HOST}/%s_${YEAR}-${MONTH}-${DAY}.log" % (source, source)
                data.append((source, port, protocol, syslog_path, app, comment, file_url))

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=["source", "port", "protocol", "path", "apps", "comment", "origin"])

# Sort the DataFrame by source for better organization
df.sort_values(by="port", inplace=True)

# Reset the index after sorting
df.reset_index(drop=True, inplace=True)

# Create a clickable link for the "origin" column
df["origin"] = df["origin"].apply(lambda x: f'[Link]({x})')

# Convert the DataFrame to a markdown table with left-aligned "port" column
table = tabulate(df, headers='keys', tablefmt='pipe', stralign='left', numalign='left', showindex='never', disable_numparse=True)

# Pull existing content before update
with open(parent_directory + "/README.md", 'r') as readme_file:
    existing_content  = readme_file.read()

# Find the start and end of the "Syslog-ng Port Tracker" section
start_of_section = existing_content.find("## Syslog-ng Port Tracker")

# Construct the updated README content
updated_readme_content = existing_content[:start_of_section] + "## Syslog-ng Port Tracker\n" + table

# Update the README.md file with the extracted data
with open(parent_directory + "/README.md", 'w') as readme_file:
    readme_file.write(updated_readme_content)

print("Data extraction and README update complete.")