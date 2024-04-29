import time
from decouple import config
from DrissionPage import ChromiumPage, errors
from datetime import datetime, timedelta
from .models import Feed, Post


class InstagramParser:
    INSTAGRAM_BASE_URL = 'https://www.instagram.com/'
    INSTAGRAM_ACCOUNT = config('INSTAGRAM_ACCOUNT')
    INSTAGRAM_PASSWORD = config('INSTAGRAM_PASSWORD')

    def __init__(self, user_id):
        self.user_id = user_id
        self.post_index = 0
        print("Initializing InstagramParser with user_id:", user_id)

    def start_parse(self):
        # if user already logged in, skip log in
        if not self.is_login():
            self.login_to_instagram()
        feed = self.add_feed_to_database()
        self.navigate_to_feed_page()
        self.parse_posts(feed)
        print("Parsing finished for user:", self.user_id)

    def is_login(self):
        page = ChromiumPage()
        page.get('https://www.instagram.com/chen_cdu/')
        text= page.ele('.x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj').text
        if len(text) > 0:
            return True
        else:
            return False

    def login_to_instagram(self):
        page = ChromiumPage()
        try:
            page.get('https://www.instagram.com/accounts/login/')
            if page.ele('#loginForm'):
                page.ele('._aa4b _add6 _ac4d _ap35').input(self.Instagram_account)
                page.ele('._aa4b _add6 _ac4d _ap35').input(self.Instagram_password)
                page.ele('. _acan _acap _acas _aj1- _ap30').click()
                print("login parse")
        except errors.ElementNotFoundError:
            print("Timeout occurred while waiting for the login form.")

    def add_feed_to_database(self):
        user_id = self.user_id
        feed_url = self.INSTAGRAM_BASE_URL + user_id + '/'
        return Feed.objects.create(
            platform='instagram',
            user_id=user_id,
            feed_url=feed_url,
            feed_name=user_id,
            last_update_date=datetime.now()
        )

    def navigate_to_feed_page(self):
        page = ChromiumPage()
        page.get(self.INSTAGRAM_BASE_URL + self.user_id + '/')
        page.ele('._aagw').click()

    def parse_posts(self, feed):
        fetch_num =5
        page = ChromiumPage()
        pop_window_element = page.ele('.x1cy8zhl x9f619 x78zum5 xl56j7k x2lwn1j xeuugli x47corl')
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
                        platform='instagram',
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
            pop_window_element.ele('. _aaqg _aaqh').click()

    def get_post_text(self, pop_window_element):
        post_text_ele = pop_window_element.ele('._ap3a _aaco _aacu _aacx _aad7 _aade')
        return post_text_ele.text

    def get_media_url(self, pop_window_element):
        try:
            img = pop_window_element.ele('.x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3', timeout=4)
            return img.attr('src')
        except errors.ElementNotFoundError:
            try:
                video = pop_window_element.ele('.x1lliihq x5yr21d xh8yej3', timeout=2)
                return video.attr('src')
            except errors.ElementNotFoundError:
                return None

    def get_post_time(self, pop_window_element):
        time_element = pop_window_element.ele('.x1p4m5qa', timeout=2)
        post_time_iso_format = time_element.attr('datetime')
        time_format = datetime.fromisoformat(post_time_iso_format.replace('Z', '+00:00'))
        return time_format.strftime('%Y-%m-%d %H:%M:%S')

