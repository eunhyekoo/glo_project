import ast
import json
from typing import Iterable
from xmlrpc.client import ResponseError
import pysrt
import re
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .response import (
    MESSAGE_400,
    MESSAGE_404,
    error_response,
    word_count_response,
    completed_response,
)
from .serializers import (
    clientFeedbackRegistrySerializer,
    feedbackSerializer,
    getAllFeedbackSerializer,
    healthcheckSerializer,
    managementSerializer,
    translationInfoSerializer,
    translationSerializer,
    wordCountSerializer,
)
from .function import (
    check_translation_work_exist,
    check_word_count_and_update,
    convert_to_standard_language_code,
    create_external_resource,
    create_feedback,
    create_new_content_title,
    create_new_pm_poc_resource,
    create_notion_page,
    create_or_update_content_title,
    create_or_update_translation_work,
    create_source_sheet,
    create_translation_information,
    create_word_count,
    delete_notion_data,
    read_notion_database,
    seperate_target_language,
    update_notion_data,
    update_pm_poc_id,
    get_memsource_data,
    get_new_memsource_data,
)
from .models import Feedbacks, Role, StakeholdersType, TranslationWorks
from rest_framework import viewsets, mixins, status


class ApiHealthCheckView(GenericAPIView):
    serializer_class = healthcheckSerializer

    def get(self, request):
        return HttpResponse("{}")


class CreateClientFeedbackRegistry(GenericAPIView):
    serializer_class = clientFeedbackRegistrySerializer
    permission_classes = ()

    def post(self, request):
        serializer = clientFeedbackRegistrySerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = create_feedback(request)

            except ObjectDoesNotExist as e:
                print("error:", e)
                return Response(error_response(404), status=status.HTTP_404_NOT_FOUND)

            if isinstance(data, Iterable):
                serializer = feedbackSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            serializer = feedbackSerializer(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(error_response(400), status=status.HTTP_400_BAD_REQUEST)


class GetAllNotionFeedbacks(GenericAPIView):
    serializer_class = getAllFeedbackSerializer
    permission_classes = ()

    def get(self, request, databaseId):
        notion_feedback_data = read_notion_database(database_id=databaseId)
        return JsonResponse(notion_feedback_data, status=status.HTTP_200_OK, safe=False)


class CreateManagement(GenericAPIView):
    serializer_class = managementSerializer
    permission_classes = ()

    def post(self, request):
        serializer = managementSerializer(data=request.data)
        if serializer.is_valid():
            sheet_id = request.data["sheetId"]
            gid = request.data["gid"]

            # 1. title 더블체크
            # 1-1. title 있으면 가져오기
            title_id = create_or_update_content_title(request)

            # 2. Resource 더블체크
            # pm, poc
            pm_poc_id = create_new_pm_poc_resource(request)

            # translator
            # TODO: translator, qcer resource 생성 후 Feedbacks가 아니라 TranslationWorks에 update!
            translator_name = request.data["translatorName"]
            translator_email = request.data["translatorEmail"]
            translator_id = create_external_resource(
                translator_name, translator_email, Role.TRANSLATOR
            )

            # qcer
            qcer_name = request.data["qcerName"]
            qcer_email = request.data["qcerEmail"]
            qcer_id = create_external_resource(qcer_name, qcer_email, Role.QCER)

            # desktop publisher
            desktop_publisher_name = request.data["desktopPublisherName"]
            desktop_publisher_email = request.data["desktopPublisherEmail"]
            desktop_publisher_id = create_external_resource(
                desktop_publisher_name, desktop_publisher_email, Role.DESKTOP_PUBLISHER
            )

            # 3. translation work 더블체크(can multiple objects)
            # 4. translator, qcer 정보 업데이트
            episode_number = request.data["episodeNumber"]
            translation_work_id = create_or_update_translation_work(
                title_id, int(episode_number), translator=translator_id, qcer=qcer_id
            )

            # 5. feedback 더블체크
            feedbacks = Feedbacks.objects.filter(translationWorkId=translation_work_id)

            if len(feedbacks) == 0:
                # 6-1. feedback 없으면 새로운 데이터 만들기
                source_sheet_id = create_source_sheet(sheet_id, gid)

                new_feedback = Feedbacks(
                    desktopPublisherId=desktop_publisher_id,
                    managementSourceId=source_sheet_id,
                    translationWorkId=translation_work_id,
                )
                new_feedback.save()
                new_feedback = update_pm_poc_id(new_feedback, pm_poc_id)

                # 7. 데이터 반환
                serializer = feedbackSerializer(new_feedback)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # 6-2. feedback 있으면 데이터 update
            elif len(feedbacks) == 1:
                source_sheet_id = create_source_sheet(sheet_id, gid)

                existed_feedback = feedbacks[0]
                existed_feedback.managementSourceId = source_sheet_id
                existed_feedback.desktopPublisherId = desktop_publisher_id
                existed_feedback.save()

                updated_feedbacks = update_pm_poc_id(existed_feedback, pm_poc_id)

                if isinstance(updated_feedbacks, Iterable):
                    serializer = feedbackSerializer(updated_feedbacks, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                serializer = feedbackSerializer(updated_feedbacks)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                source_sheet_id = create_source_sheet(sheet_id, gid)
                feedbacks.update(
                    desktopPublisherId=desktop_publisher_id,
                    managementSourceId=source_sheet_id,
                )
                updated_feedbacks = update_pm_poc_id(feedbacks, pm_poc_id)

                serializer = feedbackSerializer(updated_feedbacks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            print(serializer.errors)
            return Response(
                {"message": "Serializer is not valid. error occured!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# TODO: feedback update가 진행 안 됨 -> 이슈 해결 필요


class GetTranslationInfoViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = TranslationWorks.objects.all()
    serializer_class = translationInfoSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # doublecheck
            existed_translation_work = check_translation_work_exist(request.data)

            if existed_translation_work:
                serializer = translationSerializer(existed_translation_work)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # create
            new_translation_work = create_translation_information(request.data)
            serializer = translationSerializer(new_translation_work)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                error_response(400, MESSAGE_400), status=status.HTTP_400_BAD_REQUEST
            )


# Memsource 전체 데이터 Gathering
class GetAllMemousrceData(GenericAPIView):
    def get(self, request):
        try:
            get_memsource_data()
            return Response(completed_response(200), status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            print("error:", e)
            return Response(error_response(404), status=status.HTTP_404_NOT_FOUND)


# DB에 존재하는 데이터 외에 신규 데이터 Insert
class GetNewestMemsourceData(GenericAPIView):
    def get(self, request):
        try:
            get_new_memsource_data()
            return Response(completed_response(200), status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            print("error:", e)
            return Response(error_response(404), status=status.HTTP_404_NOT_FOUND)


# TODO: client로 필터링
# TODO: resource 정보 수정용 API 필요(source language, target language) - 추가, 삭제
