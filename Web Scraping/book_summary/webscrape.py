"""
Web Scraping with Beautiful Soup

Goal:
Getting Top recommended books and their summaries from some reputable blogs e.g. 
"""

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

# Using James Clear Book Summary website
path = "https://jamesclear.com/book-summaries?utm_source=designepiclife"

# Create Beautiful Soup Object with URL path
source = requests.get(path).text
soup = bs(source, 'html.parser')

""" 
# Alternatives: Using HTML file to import 
with open('bookSummary.html') as html_file:
 	soup = BeautifulSoup(html_file, 'lxml')
"""

# Inspect on the html
# print(soup.prettify())

# Get the book titles
titles = []
authors = []
for count, book in enumerate(soup.find_all('div', class_='sale-book')):
	content = book.h3.text

	# Handling special cases where there is a word "by" in the book title, only split by the second occurance of "by" 
	by_count = content.count("by")
	if by_count > 1:
		title = "by".join(content.split("by", by_count)[:by_count])
		author = content.split("by", by_count)[by_count].strip()

	else:
	 	title = content.split("by")[0].strip()
	 	author = content.split("by")[1].strip()
	

	titles.append(title)
	authors.append(author)

print(f"Number of books: {len(titles)} and Number of authors: {len(authors)}")
print()

# Scraping the 3 sentences summaries of each book

summaryTexts = []

for counter, summary in enumerate(soup.find_all('p')):
	# On James Clear's website, the summary text appear in the 4th appearance of paragraph
	if counter >= 3:
		if re.search(r":", summary.text):
			summaryText = summary.text.split(":")[1].strip() 
			summaryTexts.append(summaryText)
		
print(f"Number of Summaries: {len(summaryTexts)}")
print()

# Get the URLs

counter = 0
urls = []
for url in soup.find_all("a", href=True):
	if re.search("book-summaries", url['href']) and re.search("https:", url['href']):
		counter += 1
		urls.append(url['href'])
print(f"Number of URLs: {counter}")

# Create Data Frame 

books = {"Title": titles, "Authors": authors, "Summary": summaryTexts, "URL": urls}
df = pd.DataFrame(books)

# Export to excel
import os
export_directory = "./"
filename = "books_summaries"
file_suffix = ".xlsx"
df.to_excel(os.path.join(export_directory, filename + file_suffix), index=False)



