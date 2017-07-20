import pandas
import pdb


def create_people_df(research_groups_df):
    """Join the people and research groups sheets."""
    
    people_df = pandas.read_csv('people.csv', header=0)

    small_research_groups_df = research_groups_df[['research_group','research_division']].set_index('research_group')
    joined_df = people_df.join(small_research_groups_df, on=['research_group'])

    return joined_df


def expand_row(row, tool_category, df):
    """Take row with list of tools and expand into separate rows.
    
    The rows get appended to df.
    
    """
    
    if pandas.notnull(row[tool_category]):
        tool_list = row[tool_category].split(',')
        for tool in tool_list:
            new_row = row[['person name or identifier', 'research_group', 'research_division', tool_category]].copy()
            new_row[tool_category] = tool
            df = df.append(new_row, ignore_index=True)

    return df
    

def expand_tools(people_full_df):
    """Expand contents of tools columns by duplicating rows."""
    
    people_language_df = pandas.DataFrame()
    people_gen_datasci_df = pandas.DataFrame()
    people_discipline_datasci_df = pandas.DataFrame()
    people_support_tool_df = pandas.DataFrame()
    for index, row in people_full_df.iterrows():
        people_language_df = expand_row(row, 'programming_languages', people_language_df)
        people_gen_datasci_df = expand_row(row, 'general_datasci_tools', people_gen_datasci_df)
        people_discipline_datasci_df = expand_row(row, 'discipline_datasci_tools', people_discipline_datasci_df)
        people_support_tool_df = expand_row(row, 'support_tools', people_support_tool_df)
        
    return people_language_df, people_gen_datasci_df, people_discipline_datasci_df, people_support_tool_df


def main():
    """Run the program."""
    
    research_groups_df = pandas.read_csv('anzsrc_research_groups.csv', header=0)
    people_full_df = create_people_df(research_groups_df)

    people_language_df, people_gen_datasci_df, people_discipline_datasci_df, people_support_tool_df = expand_tools(people_full_df) 

    pdb.set_trace()

main()