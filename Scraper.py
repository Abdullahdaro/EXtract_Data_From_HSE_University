import requests
from bs4 import BeautifulSoup
import time
from fpdf import FPDF

# List to store all course data
all_courses = []

for page in range(1, 41):  # Loop through the first 40 pages
    url = f"https://www.hse.ru/en/edu/courses/page{page}.html?filial=22723&words=&full_words=&flag=ignore&year=2024&level=&language=20592&status=6&audience_scope="
    print(f"Requesting URL: {url}")  # Print the URL being requested
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    print(f"Scraping page {page}: {response.status_code}")  # Print status code

    if response.status_code == 200:  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        courses = soup.find_all('div', class_='courses__item')  # Adjust based on actual HTML structure
        
        print(f"Found {len(courses)} courses on page {page}")  # Debug info
        
        for course in courses:
            # Get course title and link
            title_tag = course.find('h3', class_='courses__header')
            title = title_tag.text if title_tag else 'No title found'
            course_link = "https://www.hse.ru" + (title_tag.find('a')['href'] if title_tag and title_tag.find('a') else 'No link found')
            
            # Initialize variables for additional info
            course_type = ''
            language = ''
            ects_credits = ''
            when = ''

            # Extract additional details
            details = course.find_all('div', class_='with-indent1')  # Updated selector
            for detail in details:
                label = detail.find('span', class_='b').text.strip()  # Get the label text
                value = detail.find_all('span')[1].text.strip() if len(detail.find_all('span')) > 1 else 'No value found'  # Get the value text
                
                if 'Type:' in label:
                    course_type = value
                elif 'Language:' in label:
                    language = value
                elif 'ECTS credits:' in label:
                    ects_credits = value
                elif 'When:' in label:
                    when = value

            # Append the course information to the list
            all_courses.append({
                'Title': title,
                'Link': course_link,
                'Type': course_type,
                'Language': language,
                'ECTS Credits': ects_credits,
                'When': when
            })
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Create a PDF document
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Load a Unicode font
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", size=12)

# Add a title
pdf.cell(200, 10, txt="HSE Courses", ln=True, align='C')

# Add course details
for course in all_courses:
    pdf.cell(0, 10, f"Title: {course['Title']}", ln=True)
    pdf.cell(0, 10, f"Link: {course['Link']}", ln=True)
    pdf.cell(0, 10, f"Type: {course['Type']}", ln=True)
    pdf.cell(0, 10, f"Language: {course['Language']}", ln=True)
    pdf.cell(0, 10, f"ECTS Credits: {course['ECTS Credits']}", ln=True)
    pdf.cell(0, 10, f"When: {course['When']}", ln=True)
    pdf.cell(0, 10, '', ln=True)  # Blank line for spacing

# Save the PDF to a file
pdf_file_name = "HSE_Courses.pdf"
pdf.output(pdf_file_name)

print(f"PDF saved as {pdf_file_name}")
