import argparse
import pandas
import pdb


def filter_data(df, groups):
    """Filter by research group.
    
    Args:
      groups (list)
    
    """
        
    if groups:
        df = df[df['research_group'].isin(groups)]
        
    return df

    
def get_demographics(selected_groups):
    """Get the demographic information"""
    
    people_df = pandas.read_csv('../data/people.csv', header=0, encoding='utf-8-sig')
    people_df = filter_data(people_df, selected_groups)
    career_stage_gdf = people_df.groupby('career_stage')
    
    print('# DEMOGRAPHICS', '\n')
    
    total_people = len(people_df)
    print('Total people:', total_people, '\n')
    for career_stage, career_stage_df in career_stage_gdf:
        print(career_stage, len(career_stage_df))     

    non_coders = people_df['programming_languages'].isnull().sum()
    print('coders:', total_people - non_coders)
    print('non-coders:', non_coders, '\n')


def get_prog_results(selected_groups):
    """Get programming language results"""

    programming_language_df = pandas.read_csv('../data/derived/people_programming_languages.csv', header=0, encoding='utf-8-sig')
    programming_language_df = filter_data(programming_language_df, selected_groups) 

    print('# PROGRAMMING LANGUAGES', '\n')
    print(programming_language_df['tool'].value_counts().to_string(), '\n')


def get_general_results(selected_groups):
    """Get general data science tool results"""

    general_datasci_df = pandas.read_csv('../data/derived/people_general_datasci_tools.csv', header=0, encoding='utf-8-sig')
    general_datasci_df = filter_data(general_datasci_df, selected_groups)
    general_datasci_purpose_gdf = general_datasci_df.groupby('purpose')
    
    print('# GENERAL DATA SCIENCE TOOLS', '\n')
    for purpose, purpose_df in general_datasci_purpose_gdf:
        print('##', purpose)
        print(purpose_df['tool'].value_counts().to_string(), '\n')


def get_discipline_results(selected_groups):
    """Get discipline-specific data science tool results"""

    discipline_datasci_df = pandas.read_csv('../data/derived/people_discipline_datasci_tools.csv', header=0, encoding='utf-8-sig')
    discipline_datasci_df = filter_data(discipline_datasci_df, selected_groups)
    discipline_datasci_purpose_gdf = discipline_datasci_df.groupby('discipline')
    
    print('# DISCIPLINE DATA SCIENCE TOOLS', '\n')
    for purpose, purpose_df in discipline_datasci_purpose_gdf:
        print('##', purpose)
        print(purpose_df['tool'].value_counts().to_string(), '\n')


def get_support_results(selected_groups):
    """Get support tool results"""

    support_tool_df = pandas.read_csv('../data/derived/people_support_tools.csv', header=0, encoding='utf-8-sig')
    support_tool_df = filter_data(support_tool_df, selected_groups)
    support_tool_gdf = support_tool_df.groupby(['category', 'task'])

    print('# SUPPORT TOOLS', '\n')
    for category_task, task_df in support_tool_gdf:
        print('##', category_task[0] + ': ' + category_task[1])
        print(task_df['tool'].value_counts().to_string(), '\n')


def main(inargs):
    """Run the program."""
    
    research_field_df = pandas.read_csv('../data/anzsrc_research_groups.csv', header=0, encoding='utf-8-sig')
    all_divisions = research_field_df['research_division'].tolist()
    all_groups = research_field_df['research_group'].tolist()

    selected_groups = []
    for division in inargs.divisions:
        division = division.replace('_', ' ')
        assert division in all_divisions, "selected division %s not valid"  %(division)
        groups = research_field_df[research_field_df['research_division'] == division]['research_group'].tolist()
        selected_groups.extend(groups)
    
    for group in inargs.groups:
        group = group.replace('_', ' ')
        assert group in all_groups, "selected group %s not valid"  %(group)
        selected_groups.append(group)
    
    get_demographics(selected_groups)
    get_prog_results(selected_groups)
    get_general_results(selected_groups)
    get_discipline_results(selected_groups)
    get_support_results(selected_groups)


if __name__ == '__main__':

    extra_info =""" 
example:
    
author:
    Damien Irving, irving.damien@gmail.com
    
"""

    description='Get tool list for a given research group or discipline'
    parser = argparse.ArgumentParser(description=description,
                                     epilog=extra_info, 
                                     argument_default=argparse.SUPPRESS,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--divisions", type=str, nargs='*', default=[], 
                        help="Research divisions to select")
    parser.add_argument("--groups", type=str, nargs='*', default=[], 
                        help="Research groups to select")

    args = parser.parse_args()            
    main(args)
