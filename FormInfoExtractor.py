import re
import asyncio

class FormInfoExtractor:
    # Function to analyze a form using the Layout model
    async def analyze_layout(self, form_path, client):
        with open(form_path, "rb") as form_file:
            poller = await asyncio.to_thread(client.begin_analyze_document, "prebuilt-document", document=form_file)
            result = await asyncio.to_thread(poller.result)
        return result

    def extract_values_from_table(self, table_data, column_name):
        # Initialize variables
        name_column_index = None
        values_dict = {}

        # First pass: Identify the column index for the column_name
        for cell in table_data:
            if cell['kind'] == 'columnHeader' and cell['content'].lower() == column_name.lower():
                name_column_index = cell['column_index']
                break

        # Second pass: Extract values based on the identified column index
        for cell in table_data:
            if cell['kind'] == 'content' and cell['column_index'] == name_column_index:
                row_index = cell['row_index']
                name = cell['content']
                values_dict[row_index] = name

        return values_dict


    def extractName(self, result):
        pattern = re.compile(r'^\w+')
        # Search for the pattern in the content
        match = pattern.match(result.content)

        if match:
            return match.group(0)
        else:
            return None


    def GetResultsForName(self, result, name, results_dict):
        # Convert the first table to dictionary format
        result_table = result.tables[0].to_dict()

        # Extract values from the table
        names_dict = self.extract_values_from_table(result_table['cells'], 'name')
        yes_dict = self.extract_values_from_table(result_table['cells'], 'yes')

        indie_results_dict = {}

        for idx in range(len(names_dict)):
            if "unselected" not in yes_dict[idx+1]:
                indie_results_dict[names_dict[idx+1]] = "Yes"
            else:
                indie_results_dict[names_dict[idx+1]] = "No"
        
        results_dict[name] = indie_results_dict
    

    def CalculateMatches(self, results_dict, name, matches_dict, match_person):
        # determine if name is within potential match pool
        if name != match_person and name in results_dict[match_person]:

            # if there is a match
            if results_dict[name][match_person] == "Yes" and results_dict[match_person][name] == "Yes":
                if name not in matches_dict:
                        matches_dict[name] = []
                matches_dict[name].append(match_person)