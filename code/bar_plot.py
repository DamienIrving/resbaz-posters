import pdb
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white", context="talk")



def parse_line(line):
    """Parse a line from input file."""
    
    components = line.split()
    freq = int(components[-1])
    label = " ".join(components[0:-1])

    return (label, freq)


def main(inargs):

    # Read data into dataframe
    if inargs.infile:
        data = [parse_line(line) for line in open(inargs.infile)]
        
    else:
        assert len(inargs.labels) == len(inargs.frequencies)
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

    parser.add_argument("--infile", type=str, default=None, 
                        help="Can give a file with tool /space freq on each line")

    parser.add_argument("--labels", type=str, nargs='*',
                        help="bar labels (will appear top to bottom")
    parser.add_argument("--frequencies", type=int, nargs='*',
                        help="frequencies")
    
    parser.add_argument("--palette", type=str, choices=('sequential', 'qualitative'), default='qualitative',
                        help="Colors for the bars")

    parser.add_argument("--title", type=str, default=None,
                        help="plot title")

    args = parser.parse_args()             
    main(args)