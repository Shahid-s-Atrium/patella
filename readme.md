Patella, a webservice resource providing easy collection and comparison of data scraped from urls

The main utility of patella is is COVFEFE (COVariation from First Executive to First Executive) - A package to visualise variation from
term to term as the party in power evolved.


File structure:

---------------------

patellaserver- The module which controls the startup and requests from the webservice, the port, address,
and processes user input

click_commands - Defines the command line arguments and options for the utility

htmlparser - The heavy lifter of the project: provides a function which scrapes urls provided in the  arguments, looks
for download links, downloads them, formats the data, and sends them through the flask service to be manipulated further
by users, such as by being graphed by other functions in the module. Compare graphs the variation in scraped data
against presidental term and party data.

Installation and Use:

---------------------
