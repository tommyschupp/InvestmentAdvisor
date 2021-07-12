# InvestmentAdvisor
This is the first multithreaded Selenium/BS4 scraping project I've done. It basically reduced a program that would have taken days to have take about 3 and a half hours. 

When you want to scrape a site that requires you to access the page you want to scrape manually (cookies, javascript, etc), simply using the URL and BS4 will not allow you to access the information.
So, Selenium can be used to scrape websites in that situation.
Selenium's problem is that it takes a very very very long time to go webpage by webpage, and when you have 15,000 pages to scrape, that can take days.
Therefore, I multithreaded the selenium without using selenium grid or anything, just using concurrent.futures .
I think this could actually be very useful to people who are in the same situation I am. 

