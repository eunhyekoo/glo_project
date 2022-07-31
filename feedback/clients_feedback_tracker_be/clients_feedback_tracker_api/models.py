from django.db import models


class TimeStampMixin(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.TextChoices):
    TRANSLATOR = "Translator"
    QCER = "QCer"
    DESKTOP_PUBLISHER = "Desktop publisher"
    PROOFREADER = "Proofreader"
    PROJECT_MANAGER = "Project manager"
    PROJECT_COODINATOR = "Project coodinator"
    PROJECT_ASSISTANT = "Project assistant"
    QUALITY_MANAGER = "Quality manager"
    LANGUAGE_MANAGER = "Language manager"
    DESIGNER = "Designer"
    POINT_OF_CONTACT = "Point of contact"
    JUNIOR_PROJECT_MANAGER = "Junior project manager"


class Gender(models.TextChoices):
    MALE = "male"
    FEMALE = "female"


class GenreType(models.TextChoices):
    FANTASY = "Fantasy"
    ROMANCE = "Romance"
    HISTORICAL = "Historical"
    OTHERS = "Others"


class WorkType(models.TextChoices):
    WEBTOON = "webtoon"
    WEBNOVEL = "webnovel"


class SeverityLevel(models.TextChoices):
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"


class SentimentLevel(models.TextChoices):
    POSTITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class StakeholdersType(models.TextChoices):
    INTERNAL = "Internal"
    EXTERNAL = "External"


class ClientName(models.TextChoices):
    KAKAO = "Kakao Ent"
    NHN = "NHN"
    NUON = "Nuon"
    PIURI = "Piuri"
    TAPPYTOON_WEBTOON = "Tappytoon Webtoon"
    TAPPYTOON_WEBNOVEL = "Tappytoon Webnovel"
    TAPAS = "Tapas"
    NAVER = "Naver"
    EINEBLUME = "Eineblume"
    STORYX = "StoryX"
    KANAFEEL = "Kanafeel"
    LEZHIN = "Lezhin"
    RIDI = "Ridi corporation"


class QualityLevel(models.TextChoices):
    EXPERT = "Expert"
    GREAT = "Great"
    GOOD = "Good"
    INTERMEDIATE = "Intermediate"
    ACCEPTABLE = "Acceptable"
    LOW = "Low"
    NOT_ACCEPTABLE = "Not Acceptable"


class ResourceRoles(TimeStampMixin):
    resourceId = models.ForeignKey(
        "Resources",
        related_name="resources",
        on_delete=models.SET_NULL,
        db_column="resourceId",
        null=True,
    )
    role = models.CharField(choices=Role.choices, max_length=25)

    class Meta:
        db_table = "ResourceRoles"


class Resources(TimeStampMixin):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=200, null=True)
    stakeholdersType = models.CharField(choices=StakeholdersType.choices, max_length=10)
    sourceLanguage = models.CharField(max_length=10)
    targetLanguage = models.CharField(max_length=10)

    class Meta:
        db_table = "Resources"


class ContentTitles(TimeStampMixin):
    englishTitle = models.CharField(max_length=150)
    koreanTitle = models.CharField(max_length=150, null=True)
    workType = models.CharField(
        choices=WorkType.choices, max_length=10, null=True, default=WorkType.WEBTOON
    )
    client = models.CharField(
        choices=ClientName.choices, max_length=20, default=ClientName.KAKAO
    )
    genre = models.CharField(choices=GenreType.choices, max_length=20, null=True)
    sourceLanguage = models.CharField(max_length=30, blank=True, null=True)
    targetLanguage = models.CharField(max_length=10, null=True)
    isRrated = models.BooleanField(default=False)
    completedAt = models.DateField(null=True)

    class Meta:
        db_table = "ContentTitles"


class Feedbacks(TimeStampMixin):
    translationWorkId = models.ForeignKey(
        "TranslationWorks",
        related_name="translation_works",
        on_delete=models.SET_NULL,
        db_column="translationWorkId",
        null=True,
    )
    feedbackDate = models.DateField(null=True)
    feedbackComments = models.TextField(null=True)
    errorTypeId = models.ForeignKey(
        "ErrorTypes",
        related_name="errortypes",
        on_delete=models.PROTECT,
        db_column="errorTypeId",
        null=True,
    )
    pmId = models.IntegerField(null=True)
    pocId = models.IntegerField(null=True)
    desktopPublisherId = models.IntegerField(null=True)
    proofreaderId = models.IntegerField(null=True)
    sentimentLevel = models.CharField(
        choices=SentimentLevel.choices, max_length=10, null=True
    )
    qualityLevel = models.CharField(
        choices=QualityLevel.choices, max_length=15, null=True
    )
    qualityPoint = models.FloatField(null=True)
    feedbackSourceId = models.ForeignKey(
        "SourceSheetMetaData",
        related_name="feedback_source",
        on_delete=models.SET_NULL,
        db_column="feedbackSourceId",
        null=True,
    )
    managementSourceId = models.ForeignKey(
        "SourceSheetMetaData",
        related_name="management_source",
        on_delete=models.SET_NULL,
        db_column="managementSourceId",
        null=True,
    )

    class Meta:
        db_table = "Feedbacks"

    # CHECK: wordCount와 entity를 통합하면서 errorTypeId, feedbackDate를 nullable로 설정함 -> 해당 column이 nullable해야 새로운 객체 생성 가능


class ErrorTypes(TimeStampMixin):  # type, measure, category enum 적용 고민
    type = models.CharField(max_length=25)
    measure = models.CharField(max_length=25)
    category = models.CharField(max_length=25)
    subcategory1 = models.CharField(max_length=50)
    subcategory2 = models.CharField(max_length=30, null=True)
    severityLevel = models.CharField(
        choices=SeverityLevel.choices, max_length=100, default=SeverityLevel.MINOR
    )
    positiveSeverityScore = models.IntegerField(null=True)
    negativeSeverityScore = models.IntegerField(null=True)

    class Meta:
        db_table = "ErrorTypes"


class SourceSheetMetaData(TimeStampMixin):
    sheetId = models.CharField(max_length=50)
    gid = models.CharField(max_length=10)
    type = models.CharField(max_length=10, default=WorkType.WEBTOON)

    class Meta:
        db_table = "SourceSheetMetaData"


class Characters(TimeStampMixin):
    titleId = models.ForeignKey(
        "ContentTitles",
        related_name="character_from_title",
        on_delete=models.PROTECT,
        db_column="titleId",
        default=1,
    )
    name = models.CharField(max_length=50)
    gender = models.CharField(choices=Gender.choices, max_length=6)
    age = models.IntegerField()
    job = models.CharField(max_length=100)

    class Meta:
        db_table = "Characters"


class TranslationWorks(TimeStampMixin):
    titleId = models.ForeignKey(
        "ContentTitles",
        related_name="content_titles",
        on_delete=models.PROTECT,
        db_column="titleId",
        null=True,
    )
    episodeNumber = models.IntegerField()
    sourceText = models.TextField(null=True)
    targetText = models.TextField(null=True)
    targetTextAfterQc = models.TextField(null=True)
    translatorId = models.IntegerField(null=True)
    qcerId = models.IntegerField(null=True)
    wordCount = models.IntegerField(null=True)
    wordCountSourceId = models.ForeignKey(
        "SourceSheetMetaData",
        related_name="word_count_source",
        on_delete=models.SET_NULL,
        db_column="wordCountSourceId",
        null=True,
    )

    class Meta:
        db_table = "TranslationWorks"


class TranslationSentences(TimeStampMixin):
    sentence = models.TextField()
    qcSentence = models.TextField(null=True)
    sourceSentence = models.TextField(null=True)
    translationWorkId = models.ForeignKey(
        "TranslationWorks",
        related_name="all_translation_text",
        on_delete=models.SET_NULL,
        db_column="translationWorkId",
        null=True,
    )
    characterId = models.ForeignKey(
        "Characters",
        related_name="characters",
        on_delete=models.SET_NULL,
        db_column="charactorId",
        null=True,
    )
    situation = models.CharField(max_length=20, null=True)
    detailSituation = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "TranslationSentences"
