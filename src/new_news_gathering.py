import articleDateExtractor
import newspaper
import pandas as pd
from langdetect import detect
from os import path
PATH = "./data/definitive_all.pkl"
import datetime

import sys
columns = ['title','text','url','source','publish_date']
import tqdm


#if res, resets the newspaper3k cache
OP = 'up' if len(sys.argv)==1 else 'res'

#removed:

# 'http://www.time.com',
# 'http://www.vice.com/en_us',
# 'http://cnet.com',
# 'http://www.sfgate.com',
# 'http://yahoo.com',
# 'http://www.c-span.org',
# 'http://betabeat.com',
# 'http://www.nasa.gov',
# 'http://zdnet.com',
# 'http://www.aljazeera.com',
# 'http://www.sciencedaily.com',
# 'http://cbn.com'

# news_sites = [
    # 'http://www.bbc.co.uk',
    # 'http://telegraph.co.uk',
    # 'http://independent.co.uk',
    # 'https://cnn.com',
    # 'https://www.foxnews.com',
    # 'https://theatlantic.com',
    # 'https://www.npr.org',
    # 'https://www.suntimes.com',
    # 'https://www.newrepublic.com',
    # 'https://thecitizen.com',
    # 'https://www.news.com.au',
    # 'https://thedailyworld.com',
    # 'https://nytimes.com',
    # 'https://www.nbcnews.com',
    # 'https://www.etonline.com',
    # 'https://www.wired.com',
    # 'https://www.mlive.com',
    # 'https://seattletimes.com',
    # 'https://www.cleveland.com',
    # 'https://www.today.com',
    # 'https://townhall.com',
    # 'https://www.nypost.com',
    # 'https://www.reuters.com',
    # 'https://www.scientificamerican.com',
    # 'https://www.theverge.com',
    # 'https://www.latimes.com',
    # 'https://abcnews.com',
    # 'https://washingtonexaminer.com',
    # 'https://celebuzz.com',
    # 'https://www.rollingstone.com',
    # 'https://news.sky.com',
    # 'https://thinkprogress.org',
    # 'https://www.people.com',
    # 'https://thedailybeast.com',
    # 'https://thechronicle.com.au',
    # 'https://usatoday.com'
    # # 'https://www.redstate.com',
# ]

news_sites = [
    'https://www.nypost.com',
    'http://www.bbc.co.uk',
    'https://www.nbcnews.com',
    'https://usatoday.com',
    'https://www.reuters.com',
    "https://www.activistpost.com/",
    "https://21stcenturywire.com/",
]


not_valid_titles = [
    "Quiz: ",
    "Top",
    "Daily",
    "Things"
]


def reset_cache():
    builders = []
    for paper in tqdm.tqdm(news_sites,total=len(news_sites),desc="Generating builders..."):
        p_builder= newspaper.build(paper)
        # p_builder= newspaper.build(paper, memoize_articles=False)
        builders.append(p_builder)

    for builder in builders:
        print(builder.size())

def valid_article(title):
    for word in not_valid_titles:
        if word in title:
            return False
    return True

doms = ["in.reuters.com","af.reuters.com","uk.reuters.com","ca.reuters.com"]

day = datetime.date(2020,2,20)
start_day = day_datetime = datetime.datetime.combine(day, datetime.datetime.min.time())

def update_articles():
    for paper in tqdm.tqdm(news_sites,total=len(news_sites),desc="Updating news.."):
        builder= newspaper.build(paper)
        print(paper, builder.size())
        articles = []
        for article in builder.articles[:200]:
            if any(dom in article.url for dom in doms):
                continue
            try:
                article.download()
                article.parse()
                                # if article.meta_lang == 'en':
                if detect(article.title) == 'en':
                    title = article.title
                    if valid_article(title):
                        publish_date = article.publish_date
                        if not publish_date:
                            publish_date = articleDateExtractor.extractArticlePublishedDate(article.url)

                        if publish_date != None:
                          if publish_date.tzinfo != None:
                            publish = publish_date.replace(tzinfo=None)
                            text = article.text
                            source = builder.domain
                            url = article.url
                            if publish > start_day:
                                articles.append((title,text,url,source,publish))
            except Exception as e:
                print(e)

        dataframe = pd.DataFrame(articles,columns=columns)
        if path.exists(PATH):
            df = pd.read_pickle(PATH)
            df = df.append(dataframe, ignore_index=True)
            df = df.drop_duplicates(subset=['title','source'])
            df.reset_index(drop=True,inplace=True)
            df.to_pickle(PATH)
        else:
            dataframe.to_pickle(PATH)


if OP == 'res':
    reset_cache()
else:
    update_articles()
    print("Done at ",datetime.datetime.now())


