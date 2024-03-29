
# PeoplePerHour WebScraper
![PeoplePerHour](https://logos-download.com/wp-content/uploads/2020/06/PeoplePerHour.com_Logo.png)

[PeoplePerHour](https://www.peopleperhour.com/dashboard/seller) is, apparently, the #1 freelancing community. A place to find professional freelancers and post your own freelance jobs.

This project is a simple Python interface to scrape job listings from a base URL and store them in a .csv file.

## Setup
1. Install Python: Ensure you have Python installed on your system. If not, you can download and install it from https://www.python.org/downloads/.

2. Install the requirements with pip
```
python -m pip install -r requirements.txt
```
## What is happening?

This program scrapes all the job listings on the base URL. You can change this but the program may not work as intended.

![](https://i.imgur.com/DgmEJyF.png)

You can pick how many pages worth of job listings it does and obviously the more pages, the more time it takes.

![](https://i.imgur.com/tXY733O.png)

Once it is done, it will save the information to a .csv file. It will then display the total price range the job offers take up and you can pick which price span you want. Here I did £50 - £200.

![](https://i.imgur.com/tZD39T3.png)

![The CSV file](https://i.imgur.com/ieV2nfw.png)

After it will then give you two options. 

![](https://i.imgur.com/7C1csmG.png)

1. Display Titles will just show all the job listings in that price range.

![](https://i.imgur.com/wcd7QhD.png)

2. However if you picked word cloud, it will generate a word cloud (Really?) of the skills **(shown in red)**. You can use this to view the most popular skills and price your own services competitively.
![](https://i.imgur.com/unS8LbT.png)

![](https://i.imgur.com/t7FmWCP.png)

![Word Cloud](https://i.imgur.com/vYPXA5d.png)
## Final Words
This may or may not be against their terms of services so please **don't** use this. This was for educational purposes and should only be used lawfully. I am not held liable for any damages that may ensue or for the wrongful actions others may conduct with this.
