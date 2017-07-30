# ResBaz posters

Analysis of [ResBaz poster](http://melbourne.resbaz.edu.au/post/108054124634/the-resbaz-poster-session-with-a-difference) data.

The repository contains the following:
* **notes.md** - notes for the report and paper that will arise from the analysis
* **datasci_tools.md** - overview of the data science tool hierarchy
* **support_tools.md** - overview of the support tools identified in the posters

There are then directories for the data, code and development.

## Data entry and analysis

The information from the posters is being entered into tables using an online lightweight database platform called [Airtable](https://airtable.com). Those tables are in the `data/` directory. The main table is `data/people.csv`, which has one row for every person/poster. 

While data entry is easier/quicker if there's just one row for every poster,
analysis of the data is simpler if there's a new row for every single tool
(i.e. if one person used five different digital research tools, their information would be replicated over five rows).
The `code/wrangle_data.py` script takes the raw data from Airtable (i.e. from the `data/` directory)
and converts it to a one row per tool format (see the `data/derived/` directory for the output of `code/wrangle_data.py`).

Finally, the tables in `data/derived/` are used to produce the preliminary results in the `results/` directory.

## Other notes

The research disciplines listed in `data/anzsrc_research_groups.csv` come from the
[Australian and New Zealand Standard Research Classification (ANZSRC), 2008 ](http://www.abs.gov.au/ausstats/abs@.nsf/Products/6BB427AB9696C225CA2574180004463E?opendocument) 













