import pdb
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white", context="talk")


def main(inargs):

    assert len(inargs.labels) == len(inargs.frequencies)

    # Read data into dataframe
    labels = [x.replace('_', ' ') for x in inargs.labels]
    data = list(zip(labels, inargs.frequencies))
    headers = ['label', 'frequency']
    df = pd.DataFrame.from_records(data, columns=headers)
    
    # Create plot
    fig, ax = plt.subplots()
    if inargs.palette == 'qualitative':
        palette = "Set3"
    elif inargs.palette == 'sequential':
        palette = "BuGn_d"
    
    sns.barplot(x="frequency", y="label", data=df, palette=palette)
    ax.set_ylabel("")
    sns.despine(left=True, top=True, right=True)

    if inargs.title:
        ax.set_title(inargs.title.replace('_',' '))

    plt.savefig(inargs.outfile, bbox_inches='tight')

    
if __name__ == '__main__':

    extra_info =""" 
author:
    Damien Irving, irving.damien@gmail.com
"""

    description = 'Plot a bar chart'
    parser = argparse.ArgumentParser(description=description,
                                     epilog=extra_info, 
                                     argument_default=argparse.SUPPRESS,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("outfile", type=str, help="Output file")                                     

    parser.add_argument("--labels", type=str, nargs='*', required=True,
                        help="bar labels (will appear top to bottom")
    parser.add_argument("--frequencies", type=int, nargs='*', required=True,
                        help="frequencies")
    
    parser.add_argument("--palette", type=str, choices=('sequential', 'qualitative'), default='qualitative',
                        help="Colors for the bars")

    parser.add_argument("--title", type=str, default=None,
                        help="plot title")

    args = parser.parse_args()             
    main(args)