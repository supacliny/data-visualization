Data Visualizer 3
=================
Ability to line-graph a time-series using a django backend with [highcharts](http://www.highcharts.com/) - an amped up interactive JavaScript charting library.

Contact
-------
[@supacliny](https://twitter.com/supacliny)

Requirements
------------
Our web application was developed on Mac OS X 10.6.8 using Django 1.3.1 and Python 2.6, and pulls data using Yahoo's historical stock data web api.

Screenshot
------------
How it should look.

Installation
------------
Now, assuming you are familiar with the Django framework, here's how we can quickly and safely deploy this app.

1. Edit "infrastructure/settings.py" for your environment paths including:

	a. DATABASES (currently configured for sqlite3 with file "data.db" - create your own!)

	b. MEDIA_ROOT

	c. TEMPLATE_DIRS
		
2. While in the "infrastructure" folder, run the following command to create all the necessary database tables:

	$ python manage.py syncdb

3. While in the "infrastructure" folder, run the following command to kick off the development server at http://localhost:8000/datavis/:

	$ python manage.py runserver

4. The default time-series is Texas Instruments (TXN) - input your own stock symbol and date range, and graph away!

5. Ultimately, the aim here is to load large data sets, and run machine learning tests using appropriate libraries like apache mahout.

6. Have fun  :)