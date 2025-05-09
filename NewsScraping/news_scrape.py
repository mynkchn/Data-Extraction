import newspaper
import lxml
import feedparser

def scrape_news(feed_url) :
    articles=[]
    feed=feedparser.parse(feed_url)
    for entry in feed.entries :
        article=newspaper.Article(entry.link)
        article.download()
        article.parse()
        articles.append({
            'title': article.title,
            'author': article.authors,
            'publish_date': article.publish_date,
            'content': article.text
        })
    return articles


feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'
articles = scrape_news(feed_url)

# print the extracted articles
for article in articles:
    print('Title:', article['title'])
    print('Author:', article['author'])
    print('Publish Date:', article['publish_date'])
    print('Content:', article['content'])
    print()
    