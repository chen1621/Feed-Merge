from django.db import models

class Platforms(models.TextChoices):
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    FACEBOOK = 'facebook'

# Create your models here.
class Feed(models.Model):
    feed_line_no = models.CharField(max_length=6)
    platform = models.CharField(max_length=20, choices=Platforms.choices)
    user_id = models.CharField(max_length=100)  #feed id of social media platform
    feed_url = models.TextField()
    feed_name = models.CharField(max_length=255) # for user to write the name
    last_update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
            if not self.feed_line_no:
                last_record = Feed.objects.order_by('-feed_line_no').first()
                if last_record:
                    last_number = int(last_record.feed_line_no[2:])
                    new_number = last_number + 1
                    self.feed_line_no = f"F{new_number:04d}"
                else:
                    self.feed_line_no = "F0001"
            super(Feed, self).save(*args, **kwargs)

    def __str__(self):
        return self.feed_line_no

class Post(models.Model):
    line_no = models.AutoField(primary_key=True)
    feed_line_no = models.CharField(max_length=6)
    user_id = models.CharField(max_length=100)  #feed id of social media platform
    platform = models.CharField(max_length=20, choices=Platforms.choices)
    post_title = models.CharField(max_length=100)
    post_text = models.TextField()
    post_url = models.TextField()
    post_media_url = models.TextField(null=True, blank=True)
    post_time = models.DateTimeField()
    post_fetch_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.post_title:
                self.post_title = self.post_text[:30]  # Set post_title to the first 30 characters of post_text
        super().save(*args, **kwargs)

    def __str__(self):
        return self.line_no
    