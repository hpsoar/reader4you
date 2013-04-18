class StoryWordUpdateRecord(models.Model):
    story_id = models.IntegerField()
    last_update = models.DateTimeField()
    num_updates = models.IntegerField()

TITLE_WORD, CONTENT_WORD, TAG_WORD = range(3)

class StoryWord(models.Model):
    story_id                 = models.IntegerField()
    word_id                  = models.IntegerField()
    location                 = models.IntegerField()
    word_type                = models.IntegerField()  # title word; (latest) content word; tag word; comment word;

def extract_words(text):
    pass

def extract_words_from_story(story):
    # NOTE: assumes that story doesn't change
    title_words = extract_words(story.story_title)
    content_words = extract_words(story.story_content)
    tag_words = extract_words(' '.join(story.story_tags))
    #story_content            = mongo.StringField()
    #story_content_z          = mongo.BinaryField()
    #story_content_type       = mongo.StringField(max_length=255)
    #story_author_name        = mongo.StringField()
    #story_permalink          = mongo.StringField()

    def _update_words(story, word_list, word_type):
        for i in range(len(word_list)):
            word = Word.objects.get_or_create(word_text=word_list[i])
            StoryWord.objects.get_or_create(word_id=word.pk, story_id=story.pk, location=i, word_type=word_type)

    _update_words(story, title_words, TITLE_WORDS)
    _update_words(story, content_words, CONTENT_WORDS)
    _update_words(story, tag_words, TAG_WORDS)


