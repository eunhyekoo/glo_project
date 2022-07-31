from os import set_inheritable
from rest_framework import fields, serializers
from clients_feedback_tracker_api.models import (
    Feedbacks,
    TranslationWorks,
    ClientName,
    SentimentLevel,
)
from clients_feedback_tracker_api.function import get_error_type_id
from clients_feedback_tracker_api.response import error_response


class healthcheckSerializer(serializers.Serializer):
    data = serializers.CharField(required=False, allow_blank=True)


class clientFeedbackRegistrySerializer(serializers.Serializer):
    title = serializers.CharField()
    feedbackDate = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField()
    subcategory1 = serializers.CharField()
    subcategory2 = serializers.CharField(allow_blank=True)
    feedbackComments = serializers.CharField(allow_blank=True)
    sentimentLevel = serializers.ChoiceField(choices=SentimentLevel)
    severityLevel = serializers.CharField(allow_blank=True)
    episodeNumber = serializers.CharField()
    sourceLanguage = serializers.CharField()
    targetLanguage = serializers.CharField()
    isRrated = serializers.CharField(allow_blank=True)
    sheetId = serializers.CharField()
    gid = serializers.CharField()
    client = serializers.ChoiceField(choices=ClientName)

    def validate(self, attrs):
        subcategory1 = self.initial_data.get("subcategory1")
        subcategory2 = self.initial_data.get("subcategory2")

        if not get_error_type_id(subcategory2, subcategory1):
            raise serializers.ValidationError(
                error_response(400, "Error Type is not found.")
            )

        return self.initial_data


class wordCountSerializer(serializers.Serializer):
    title = serializers.CharField()
    sheetId = serializers.CharField()
    gid = serializers.CharField()
    episodeNumber = serializers.CharField()
    targetText = serializers.CharField()


class managementSerializer(serializers.Serializer):
    id = serializers.CharField()
    koreanTitle = serializers.CharField()
    englishTitle = serializers.CharField()
    workType = serializers.CharField()
    genre = serializers.CharField(allow_blank=True)
    sourceLanguage = serializers.CharField()
    targetLanguage = serializers.CharField()
    pmPoc = serializers.CharField(allow_blank=True)
    episodeNumber = serializers.CharField()
    translatorName = serializers.CharField(allow_blank=True)
    translatorEmail = serializers.CharField(allow_blank=True)
    qcerName = serializers.CharField(allow_null=True)
    qcerEmail = serializers.CharField(allow_null=True)
    desktopPublisherName = serializers.CharField(allow_null=True)
    desktopPublisherEmail = serializers.CharField(allow_null=True)
    sheetId = serializers.CharField()
    gid = serializers.CharField()


class getAllFeedbackSerializer(serializers.Serializer):
    databaseId = serializers.CharField()


class feedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = "__all__"


class translationInfoSerializer(serializers.Serializer):
    title = serializers.CharField()
    sheetId = serializers.CharField()
    gid = serializers.CharField()
    episodeNumber = serializers.CharField()
    targetText = serializers.CharField()
    targetTextAfterQc = serializers.CharField(allow_blank=True)
    existedQcValueInfo = serializers.CharField(allow_blank=True)


class translationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationWorks
        fields = "__all__"
