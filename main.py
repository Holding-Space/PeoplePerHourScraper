import os
import requests
from bs4 import BeautifulSoup
import csv
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BASE_URL = "https://www.peopleperhour.com/services/technology-programming/programming-coding/python-development"

def get_job_listings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('li', class_='pph-col-xs-12 pph-col-sm-12 pph-col-md-6 pph-col-lg-4 pph-col-xl-4 list__item⤍List⤚2ytmm')

def extract_job_info(job_listing):
    # Extract relevant information from the job listing
    title = job_listing.find('h2', class_='title-nano card__title⤍HourlieTile⤚5LQtW').text.strip()
    skills = job_listing.find('span', class_='hourlieTag__label⤍HourlieTag⤚NL6Ui').text.strip()
    delivery_time = job_listing.find('span', class_='nano card__shipment⤍HourlieTile⤚AjgW3').text.strip().split()[-2:]
    delivery_time = ' '.join(delivery_time)
    price = job_listing.find('span', class_='title-nano').text.strip()

    # Extract number of reviews (number of ratings)
    rating_span = job_listing.find('span', class_='card__freelancer-reviews⤍HourlieTileMeta⤚HCTu6')
    if rating_span:
        num_reviews_str = rating_span.text.strip().replace('(', '').replace(')', '')
        num_reviews = int(num_reviews_str) if num_reviews_str.isdigit() else 0
    else:
        num_reviews = 0

    return title, skills, delivery_time, price, num_reviews

def calculate_price_range(prices):
    prices = [float(price.replace('£', '').replace(',', '')) for price in prices]
    min_price = min(prices)
    max_price = max(prices)
    return f'£{min_price} - £{max_price}'

def filter_skills_by_price(skills_list, prices, min_price, max_price):
    filtered_skills = []
    filtered_titles = []
    for i, price in enumerate(prices):
        price_value = float(price.replace('£', '').replace(',', ''))
        if min_price <= price_value <= max_price:
            filtered_skills.extend(skills_list[i].split(','))
            filtered_titles.append({'title': skills_list[i], 'price': price_value})
    return filtered_skills, filtered_titles

def scrape_and_save_to_csv(num_pages, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Skills', 'Delivery Time', 'Price', 'Number of Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        prices = []

        for page in range(1, num_pages + 1):
            url = f'{BASE_URL}?page={page}'
            job_listings = get_job_listings(url)

            # Check if the page exists
            if not job_listings:
                print(f'Page {page} does not exist. Ending the script.')
                break

            for job_listing in job_listings:
                title, skills, delivery_time, price, num_reviews = extract_job_info(job_listing)
                prices.append(price)
                writer.writerow({'Title': title, 'Skills': skills, 'Delivery Time': delivery_time, 'Price': price, 'Number of Reviews': num_reviews})

            # Add a delay to be polite to the server
            time.sleep(2)

        full_path = os.path.abspath(csv_filename)

        price_range = calculate_price_range(prices)

        os.system("cls")
        print(f'💾 | Data Saved!\n -Short file path: "{csv_filename}"\n -Full file path: "{full_path}"')
        print(f"Total price range: {price_range}")
        return csv_filename

def display_titles(csv_filename, min_price, max_price):
    os.system("cls")
    print('Displaying titles within the specified price range...\n')
    # Read the CSV file and extract titles and prices
    titles_prices = []
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Title' in row and 'Price' in row:
                title = row['Title']
                price = float(row['Price'].replace('£', '').replace(',', ''))
                if min_price <= price <= max_price:
                    titles_prices.append({'title': title, 'price': price, 'num_reviews': row['Number of Reviews']})

    # Sort titles based on price in ascending order
    sorted_titles_prices = sorted(titles_prices, key=lambda x: x['price'])

    # Display titles
    for item in sorted_titles_prices:
        print(f'Title: {item["title"]}\nPrice: £{item["price"]:.2f}\nNumber of Reviews: {item["num_reviews"]}\n{"-" * 30}')

def generate_word_cloud(csv_filename, min_price, max_price):
    os.system("cls")
    print('Analyzing skills and generating word cloud...')

    # Read the CSV file and extract skills and prices
    skills_list = []
    prices = []
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Skills' in row and row['Skills']:
                skills_list.append(row['Skills'])
                prices.append(row['Price'])

    # Filter skills based on the specified price range
    filtered_skills, _ = filter_skills_by_price(skills_list, prices, min_price, max_price)

    # Check if there are skills to generate the word cloud
    if not filtered_skills:
        print(f'No skills found within the specified price range. Cannot generate word cloud.')
        return

    # Create a string from the filtered skills list
    skills_text = ' '.join(filtered_skills)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(skills_text)

    # Plot the WordCloud image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    os.system("cls")

    num_pages = int(input("Enter the number of pages to scrape: "))
    print("Working...")
    csv_filename = scrape_and_save_to_csv(num_pages, 'peopleperhour_data.csv')

    print("\n================")
    print("⚙️  | DISPLAY OPTIONS\n")
    min_price = float(input("\nEnter the minimum price: £"))
    max_price = float(input("Enter the maximum price: £"))

    print("\n1. Display Titles")
    print("2. Generate Word Cloud")
    choice = int(input("Choose an option (1 or 2): "))

    if choice == 1:
        display_titles(csv_filename, min_price, max_price)
    elif choice == 2:
        generate_word_cloud(csv_filename, min_price, max_price)
    else:
        print("Invalid choice. Exiting...")
