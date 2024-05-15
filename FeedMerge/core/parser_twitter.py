import time
from decouple import config
from DrissionPage import ChromiumPage, errors
from datetime import datetime, timedelta
from .models import Feed, Post


class TwitterParser:
    TWITTER_BASE_URL = 'https://www.twitter.com/'
    TWITTER_ACCOUNT = config('TWITTER_ACCOUNT')
    TWITTER_PASSWORD = config('TWITTER_PASSWORD')

    def __init__(self, user_id):
        self.user_id = user_id
        self.post_index = 0
        print("Initializing TWITTERParser with user_id:", user_id)

    def start_parse(self):
        # if user already logged in, skip log in
        # if not self.is_login():
        #     self.login_to_twitter()
        feed = self.add_feed_to_database()
        print("finish add data to dabase")
        self.parse_posts(feed)
        print("Parsing finished for user:", self.user_id)

    # def is_login(self):
    #     page = ChromiumPage()
    #     page.get('https://www.twitter.com/chen_cdu/', timeout=2)
    #     screen= page.ele('.css-1qaijid r-bcqeeo r-qvutc0 r-poiln3')
    #     text= screen.ele('.css-1qaijid r-bcqeeo r-qvutc0 r-poiln3').text
    #     print("text", text)
    #     if text =="Sign in to X":
    #         return False
    #     else:
    #         return True

    # def login_to_twitter(self):
    #     page = ChromiumPage()
    #     try:
    #         page.get('https://twitter.com/i/flow/login')
    #         page.ele('.r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7').input(self.TWITTER_ACCOUNT)
    #         page.ele('.css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l').click()
    #         page.ele('.r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7').input(self.TWITTER_PASSWORD)
    #         page.ele('.css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1dye5f7 r-o7ynqc r-6416eg r-icoktb r-1ny4l3l').click()
    #         print("login parse")
    #     except errors.ElementNotFoundError:
    #         print("Timeout occurred while waiting for the login form.")

    def add_feed_to_database(self):
        user_id = self.user_id
        feed_url = self.TWITTER_BASE_URL + user_id + '/'
        return Feed.objects.create(
            platform='twitter',
            user_id=user_id,
            feed_url=feed_url,
            feed_name=user_id,
            last_update_date=datetime.now()
        )

    def parse_posts(self, feed):
        fetch_num =5
        page = ChromiumPage()
        page.get(self.TWITTER_BASE_URL + self.user_id + '/')
        pop_window_element = page.ele('tag:article')
        print("step i")
        for i in range(fetch_num):
            print('=== ', i + 1, ' Post ===')
            post_url = page.url
            retry_count = 0

            while retry_count < 2:
                try:
                    # page.wait.load_start()
                    post_text = self.get_post_text(pop_window_element)
                    print('post_text:', post_text)

                    post_media_url = self.get_media_url(pop_window_element)
                    print('media_url:', post_media_url)

                    post_time = self.get_post_time(pop_window_element)
                    print("Datetime:", post_time)

                    Post.objects.create(
                        feed_line_no=feed.feed_line_no,
                        user_id=self.user_id,
                        platform='twitter',
                        post_text=post_text,
                        post_media_url=post_media_url,
                        post_url=post_url,
                        post_time=post_time,
                        post_fetch_time=datetime.now()
                    )

                    break
                except errors.ElementNotFoundError:
                    self.post_index += 1
                    break
                except errors.ElementLostError:
                    retry_count += 1
                    time.sleep(3)

            self.post_index += 1
            

    def get_post_text(self, pop_window_element):
        post_text_ele = pop_window_element.ele('.css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim')
        return post_text_ele.text

    def get_media_url(self, pop_window_element):
        try:
            img = pop_window_element.ele('.css-9pa8cd', timeout=2)
            return img.attr('src')
        except errors.ElementNotFoundError:
            return None

    def get_post_time(self, pop_window_element):
        time_element = pop_window_element.ele('tag:time', timeout=2)
        post_time_iso_format = time_element.attr('datetime')
        time_format = datetime.fromisoformat(post_time_iso_format.replace('Z', '+00:00'))
        return time_format.strftime('%Y-%m-%d %H:%M:%S')

