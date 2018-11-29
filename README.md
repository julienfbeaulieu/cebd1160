# Environmental footprint using exiobase2
## Intro
This data analysis was performed for the course 
[CEBD 1160 - Intro to big data technology](https://www.concordia.ca/cce/courses/details.html?subject=CEBD&catalog_number=1160). The scripts are writen in Python and explore the environmental footprint of sectors and nations using [Exiobase2](https://www.exiobase.eu/index.php/data-download/exiobase2-year-2007-full-data-set).

## Exiobase2
Life cycle assessment is a "technique to assess environmental impacts associated with all the stages of a product's 
life from raw material extraction through materials processing, manufacture, distribution, use, repair and maintenance,
 and disposal or recycling" ([source](https://en.wikipedia.org/wiki/Life-cycle_assessment)). More specifically, Input-output LCA uses economic data to quantify the consumption-based environmental footprint of industrial sectors and nations.  

[Exiobase2](https://www.exiobase.eu/index.php/data-download/exiobase2-year-2007-full-data-set) is a joint project of NTNU, TNO, SERI, Universiteit Leiden, WU, and 2.-0 LCA Consultants. It is a global multi-regional environmentally extented input output table. It details the trade flows from 43 countries and 163 sectors (totaling 7824 country-sectors) and 124 different impact categories.

Exobase2 can be downloaded [here](https://www.exiobase.eu/index.php/data-download/exiobase2-year-2007-full-data-set) (login is required but free).

## Dependencies

The scripts rely on the following python packages:

- pandas
- matplotlib 
- numpy
- [pymrio](https://github.com/konstantinstadler/pymrio)

If pymrio is installed using 'pip install pymrio', make sure that the [population.txt](https://github.com/konstantinstadler/pymrio/tree/master/pymrio/mrio_models/exio20/misc) file is present.

The scripts can also be run using [docker-airflow](https://github.com/konstantinstadler/pymrio).

## Process
Here is a description of the python scripts:
- **load_database.py** : Parse exiobase2 with pymrio package. Perform matrix operations to calculate consumption-based 
environmental footprint of sectors and countries
- **analyse_results.py** : Data exploration of results. Calculation of the environmental footprint associated with 
canadian consumption

If you run the scripts, make sure to adapt the 'PATH' constant to your setting.

## Analysis
The following section shows example of explorations possible with the data.

The **transaction matrix (Z.txt)** (*not uploaded to github due to size restriction*) show the monetary flows from each sector in each country (x-axis) 
to other country-sectors (y-axis). The visible squares are flows within a given country.

![fig4.png](https://github.com/julienfbeaulieu/cebd1160/blob/master/fig4.png)

The **consumption-based account (cba.txt)** details the environmental impact of each country.
For instance, the following figures plot the carbon footprint (kg-CO2eq and kg-CO2eq/capita)of each 
nation. While Canada is the 11th largest contributor in absolute term, it is the 6th most important 
polluter in relative to its population.

![fig1.png](https://github.com/julienfbeaulieu/cebd1160/blob/master/fig1.png)
![fig2.png](https://github.com/julienfbeaulieu/cebd1160/blob/master/fig2.png)

The **multiplyer matrix (M.txt)** (*not uploaded to github due to size restriction*) give further
detail on the environmental impact of each product. For instance, the following plot shows the
carbon, water, land and material footprint of various commodities consumed in Canada. Namely, cultural
activities have low water and material footprint, but are responsible for higher carbon and land
footprints. Leather bags are worst in every footprints shown.

![fig3.png](https://github.com/julienfbeaulieu/cebd1160/blob/master/fig3.png)

## Next steps

The exiobase2 analysis could be used to:
+ Model the environmental impact of changes in consumption
+ Develop a footprint calculator to guide people in their consumption decisions