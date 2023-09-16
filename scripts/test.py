import os
import re
import pandas as pd

# Define the directory containing the .conf files
conf_directory = "H:\\readme-tester\\syslog-ng\\conf.d\\integrations"
root = "H:\\readme-tester\\"

github_repo_url = "https://github.com/objectbased/readme-tester/blob/main/syslog-ng/conf.d/integrations/"

# Define the regex pattern to extract information from the conf files
pattern = r'input\( source\((\w+)\) port\((\d+)\) protocol\("(\w+)"\)(?: protocol2\("(\w+)"\))?'

# Create an empty DataFrame to store the extracted data
data = []

# Iterate through .conf files in the directory
for filename in os.listdir(conf_directory):
    if filename.endswith(".conf"):
        with open(os.path.join(conf_directory, filename), 'r') as file:
            content = file.read()
            matches = re.findall(pattern, content)
            for match in matches:
                source, port, protocol, protocol2 = match
                if protocol2:
                    protocol = f"{protocol},{protocol2}"
                file_url = github_repo_url + filename
                data.append((source, int(port), protocol, file_url))

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=["source", "port", "protocol", "origin"])

# Sort the DataFrame by source for better organization
df.sort_values(by="port", inplace=True)

# Reset the index after sorting
df.reset_index(drop=True, inplace=True)

# Create a clickable link for the "origin" column
df["origin"] = df["origin"].apply(lambda x: f'[Link]({x})')

# Update the README.md file with the extracted data
with open(root + "README.md", 'w+') as readme_file:
    readme_file.write("\n\n## Extracted Configuration Data\n")
    readme_file.write(df.to_markdown(index=False))

print("Data extraction and README update complete.")