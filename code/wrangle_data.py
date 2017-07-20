import pandas
import pdb


def create_people_df(research_groups_df):
    """Join the people and research groups sheets."""
    
    people_df = pandas.read_csv('../data/people.csv', header=0)

    small_research_groups_df = research_groups_df[['research_group','research_division']]
    joined_df = people_df.join(small_research_groups_df.set_index('research_group'), on=['research_group'])

    return joined_df


def expand_row(row, tool_category, df):
    """Take row with list of tools and expand into separate rows.
    
    The rows get appended to df.
    
    """
    
    if pandas.notnull(row[tool_category]):
        tool_list = [x.strip() for x in row[tool_category].split(',')]
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


def join_tools(people_df, tool_df, tool_category):
    """Add extra tool information to a people DataFrame."""
    
    unwanted_columns = ['people', 'website', 'programming_languages',
                        'general_datasci_tools', 'discipline_datasci_tools']
    for column_name in unwanted_columns:
        try:
            tool_df.drop(column_name, axis=1, inplace=True)
        except ValueError:
            pass
    
    people_df = people_df.rename(columns = {tool_category : 'tool'})
    joined_df = people_df.merge(tool_df, left_on='tool', right_on='tool', how='left')

    return joined_df


def main():
    """Run the program."""
    
    research_groups_df = pandas.read_csv('../data/anzsrc_research_groups.csv', header=0)
    people_full_df = create_people_df(research_groups_df)

    languages_df = pandas.read_csv('../data/programming_languages.csv', header=0)
    gen_datasci_df = pandas.read_csv('../data/general_datasci_tools.csv', header=0)
    discipline_datasci_df = pandas.read_csv('../data/discipline_datasci_tools.csv', header=0)
    support_tool_df = pandas.read_csv('../data/support_tools.csv', header=0)

    people_language_df, people_gen_datasci_df, people_discipline_datasci_df, people_support_tool_df = expand_tools(people_full_df) 

    people_full_language_df = join_tools(people_language_df, languages_df, 'programming_languages')
    people_full_gen_datasci_df = join_tools(people_gen_datasci_df, gen_datasci_df, 'general_datasci_tools')
    people_full_discipline_datasci_df = join_tools(people_discipline_datasci_df, discipline_datasci_df, 'discipline_datasci_tools')
    people_full_support_tool_df = join_tools(people_support_tool_df, support_tool_df, 'support_tools')

    people_full_language_df.to_csv('../data/derived/people_programming_languages.csv', index=False)
    people_full_gen_datasci_df.to_csv('../data/derived/people_general_datasci_tools.csv', index=False)
    people_full_discipline_datasci_df.to_csv('../data/derived/people_discipline_datasci_tools.csv', index=False)
    people_full_support_tool_df.to_csv('../data/derived/people_support_tools.csv', index=False)


main()