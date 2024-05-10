import os
from datetime import datetime

def update_date_in_file(file_path):
    try:
        today_date = datetime.now().strftime("%Y-%m-%d")

        with open(file_path, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            file.write(today_date)
            file.writelines(lines[1:])
            file.truncate()

        # 파일 열기
        os.startfile(file_path)

    except Exception as e:
        print("An error occurred:", e)

file_path = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop', 'morning_routine.txt')

update_date_in_file(file_path)


import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def scrape_news():
    news_body = "Today's news in Toronto:\n\n"
    url = "https://toronto.ctvnews.ca/more/local-news"
    soup = create_soup(url)
    titles = soup.findAll("h2", attrs={"class": "teaserTitle"})
    for i in range(5):
        title_text = titles[i].get_text().strip()
        link = titles[i].a["href"]
        news_body += f"{i+1}. {title_text}\n"
        news_body += f"https://toronto.ctvnews.ca{link}\n\n"
    return news_body

if __name__ == "__main__":
    news_content = scrape_news()

    import smtplib
    from account import email_address, email_password

    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_address, email_password)
        
        subject = "Today's News"
        body = news_content

        msg = f"Subject:{subject}\n\n{body}"
        smtp.sendmail(email_address, "dbdn1996@gmail.com", msg.encode('utf-8'))
