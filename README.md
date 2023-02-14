# Unit 10 Homework: Surf’s Up

Introduction
This is my favourite topic in which I will be covering the weather for my best tourist region Hawaii. In this project I will be using SQLalchemy python library to connect with the sql database and extract the queries out of it to analyse the following


Part 1-Explore and analyse climate data of Huwaii
1. Precipitation Analysis
        
        Find the most recent date in the dataset.

        Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
        
        Select only the "date" and "prcp" values.

        Load the query results into a Pandas DataFrame, and set the index to the "date" column.

        Sort the DataFrame values by "date".

        Plot the results by using the DataFrame plot method

        Use Pandas to print the summary statistics for the precipitation data.
2. Station analsis
        Design a query to calculate the total number of stations in the dataset.

        Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
                List the stations and observation counts in descending order.

                Answer the following question: which station id has the greatest number of observations?

                Using the most-active station id, calculate the lowest, highest, and average temperatures.

        Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

                Filter by the station that has the greatest number of observations.

                Query the previous 12 months of TOBS data for that station.

                Plot the results as a histogram with bins=12, as the following image shows:

        close your session

Part 2: Design Your Climate App

After completion of the initial analysis, next step to design the Flask API based queries
that will return qurery result in dictionary using date as key and prcp value.
using the JSON representation to show my dictionary returns.

The homework instructions and requirements are located in Canvas (or in the 08-Canvas folder for those cohorts not on Canvas).

- - -

© 2022 edX Boot Camps LLC. Confidential and Proprietary. All Rights Reserved.