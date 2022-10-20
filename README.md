# Mission_to_Mars
## Table of Contents
- [Overview of the Analysis](#overview-of-the-analysis)
    - [Purpose](#purpose)
    - [About the Dataset](#about-the-dataset)
    - [Tools Used](#tools-used)
    - [Description](#description)
- [Results](#results)
    - [File Architecture](#File-Architecture)
    - [To Run the Files](#To-Run-the-Files)
- [Summary](#summary)
- [Contact Information](#contact-information)

## Overview of the Analysis
### Purpose:
This project aims to create a web app that showcases the most recently published data on Mars and the Mars mission.

### About the Dataset:
The data is scraped from three websites:
 - NASA Mars News from: https://redplanetscience.com
 - Jet Propulsion Laboratory's Space Images from: https://spaceimages-mars.com
 - Mars facts from: https://galaxyfacts-mars.com
 - Hemispheres from https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars 

### Tools Used:
 - Python (html5lib and lxml libraries)
 - MongoDB
 - Flask-PyMongo
 - Splinter
 - BeautifulSoup
 - Web-Driver Manager

### Description:
Using BeautifulSoup and Splinter, the data is scraped 'live' from the websites, i.e. the most recent data is scraped everytime. The data scraped from the websites comprises the following: news title, Mars facts, and images and titles of the four Mars hemispheres. The scraped data is stored in a Mongo database, which is a NoSQL database. Using Flask-Pymongo, the web app is connected to the Mongo database and the data displayed therein. 

## Results
A 'Scrape New Data' button is added to the top most part of the page. When clicked, this button retrieves and displays the most recent data. BeautifulSoup and Splinter are used to retrieve the data from the websites. The latest Mars news and its summary is displayed near the top of the page. Right under it, the featured Mars image is displayed to the left and the table for Mars facts to the right of the page. The lower half of the page displays the full-resolution images for the four Mars hemispheres - Cerberus Hemisphere, Schiaparelli Hemisphere, Syrtis Major Hemisphere, and the Valles Marineris Hemisphere.

<img width="700" alt="image" src="https://github.com/SohaT7/Mission_to_Mars/blob/main/Images/page1.png"> 

<img width="700" alt="image" src="https://github.com/SohaT7/Mission_to_Mars/blob/main/Images/page2.png"> 

### File Architecture:
The [scraping.py](https://github.com/SohaT7/Mission_to_Mars/blob/main/scraping.py) file contains code that retrieves the data. The Mongo database is updated with this retrieved data. The [index.html](https://github.com/SohaT7/Mission_to_Mars/blob/main/templates/index.html) file contains code that outlines how the data will be dispalyed on the webpage (i.e. it provides the template for the HTML file). The [app.py](https://github.com/SohaT7/Mission_to_Mars/blob/main/app.py) file connects the web app with the Mongo database, and using the index.html file as template, updates the data onto the web app. 

### To Run the Files:
To be able to view the webpage, the files have to be run in the following order:
 - Run app.py in the command terminal ('python app.py')
 - Copy the local host server URL it gives
 - Paste the URL in a web browser and press 'Enter' to visit the page

## Summary
This project successfully builds a web app where the most recently published data on Mars and the Mars mission is scraped from multiple websites and then displayed in one place. The web app displays the title and summary of the most recent news on the Mars mission, a featured image from the mission, a table for facts on Mars, and the images and titles of the four Mars hemispheres.

## Contact Information
Email: st.sohatariq@gmail.com
