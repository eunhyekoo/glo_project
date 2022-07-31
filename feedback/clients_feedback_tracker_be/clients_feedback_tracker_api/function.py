import ast
import datetime
from datetime import datetime
from typing import Tuple
import requests, json
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
from time import sleep
from urllib.error import HTTPError
import datetime

from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    ContentTitles,
    ErrorTypes,
    Feedbacks,
    ResourceRoles,
    Resources,
    Role,
    SourceSheetMetaData,
    StakeholdersType,
    TranslationSentences,
    TranslationWorks,
    WorkType,
)

LANGUAGE_CODE_STANDARD = {
    "KO": "ko",
    "ko-kr": "ko",
    "en": "en-US",
    "EN": "en-US",
    "ES": "es",
    "es-419": "es",
    "FR": "fr",
    "fr-fr":"fr",
    "AR": "ar",
    "DE": "de",
    "PRT": "pt",
}

token = ""  # os.environ.get('NOTION_API_TOKEN')
database_id = ""  # os.environ.get('DATABASE_ID')
page_id = ""  # os.environ.get('PAGE_ID')


headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}
webnovel_clients = [
    "TAPAS",
    "NAVER",
    "NHN",
    "KKE",
    "NUON",
    "EINEBLUME",
    "STORYX",
    "KANAFEEL",
    "LEZHIN",
    "RIDI CORPORATION",
]


class Contenttitle:
    def __init__(self, request):
        self.title = seperate_target_language(request.data["title"])
        self.client = request.data["client"]
        self.source_language = convert_to_standard_language_code(
            request.data["sourceLanguage"]
        )
        self.target_language = convert_to_standard_language_code(
            request.data["targetLanguage"]
        )


def get_quality_level(quality_point: float):

    if quality_point < 57:
        quality_level = "Not Acceptable"
    elif quality_point >= 57 and quality_point < 68:
        quality_level = "Low"
    elif quality_point >= 68 and quality_point < 78:
        quality_level = "Acceptable"
    elif quality_point >= 78 and quality_point < 84:
        quality_level = "Intermediate"
    elif quality_point >= 84 and quality_point < 90:
        quality_level = "Good"
    elif quality_point >= 90 and quality_point < 95:
        quality_level = "Great"
    else:
        quality_level = "Expert"

    return quality_level


def get_quality_point(word_count: int, error_type: object, sentiment_level: str):

    try:
        if sentiment_level == "Positive":
            quality_point = (
                (word_count + error_type.positiveSeverityScore) / word_count
            ) * 100

        elif sentiment_level == "Neutral":
            quality_point = ((word_count + 0) / word_count) * 100

        else:
            quality_point = (
                (word_count + error_type.negativeSeverityScore) / word_count
            ) * 100
    except TypeError as e:
        print("word count 정보가 존재하지 않습니다.")
        return None

    return round(quality_point, 2)


def convert_to_standard_language_code(language_code):
    try:
        return LANGUAGE_CODE_STANDARD[language_code]
    except KeyError as e:
        print(e)
        return language_code


def convert_to_int_episode_number(episode_number):
    episode_number = episode_number.strip()
    try:
        episode_number = episode_number.replace("(19+)", "")
        episode_number = int(re.sub("[^0-9]", "", episode_number))
        return episode_number

    except AttributeError as e:
        return False


def filter_only_feedback(feedback_list):
    for feedback in feedback_list:
        if "---" in feedback:
            idx = feedback_list.index(feedback)
            feedback_list.pop(idx)

    return feedback_list


def get_error_type_id(subcategory2, subcategory1):
    subcategory2 = subcategory2.strip()
    subcategory1 = subcategory1.strip()

    if subcategory2 != "" and subcategory1 != "":
        print("subcategory2가 존재합니다.")
        try:
            error_type_id = ErrorTypes.objects.get(
                subcategory1__iexact=subcategory1, subcategory2__iexact=subcategory2
            )
        except ObjectDoesNotExist as e:
            print(e, subcategory1, subcategory2)
            print("Error type이 존재하지 않습니다.")
            return False

    else:
        print("subcategory2가 존재하지 않습니다.")
        try:
            error_type_id = ErrorTypes.objects.get(subcategory1__iexact=subcategory1)
        except ObjectDoesNotExist as e:
            print(e, subcategory1)
            print("Error type이 존재하지 않습니다.")
            return False

    return error_type_id


def create_source_sheet(sheet_id, gid):
    try:
        feedback_source = SourceSheetMetaData.objects.get(sheetId=sheet_id, gid=gid)
    except ObjectDoesNotExist as e:
        new_feedback_source = SourceSheetMetaData(sheetId=sheet_id, gid=gid)
        new_feedback_source.save()
        return new_feedback_source

    return feedback_source


def seperate_target_language(title):
    # title에서 target language를 제거해야 할 경우 사용
    p = re.compile(".+(?=\()")
    try:
        m = p.search(title)
        return m.group()
    except AttributeError as e:
        return title.strip()


def update_korean_title(request: object):
    title = seperate_target_language(request.data["englishTitle"])
    korean_title = request.data["koreanTitle"]

    content_title_objects = ContentTitles.objects.filter(
        englishTitle=title, koreanTitle=None
    )

    if len(content_title_objects) != 0:
        content_title_objects.update(koreanTitle=korean_title)


def create_or_update_content_title(request: object):

    update_korean_title(request)

    title = seperate_target_language(request.data["englishTitle"])
    target_language = convert_to_standard_language_code(request.data["targetLanguage"])
    source_language = convert_to_standard_language_code(request.data["sourceLanguage"])
    korean_title = request.data["koreanTitle"]
    genre = request.data["genre"]

    content_title, created = ContentTitles.objects.get_or_create(
        englishTitle=title,
        sourceLanguage=source_language,
        targetLanguage=target_language,
    )

    content_title.koreanTitle = korean_title
    content_title.genre = genre
    content_title.save()

    return content_title


def create_new_content_title(request):
    title = seperate_target_language(request.data["englishTitle"])
    target_language = convert_to_standard_language_code(request.data["targetLanguage"])
    source_language = convert_to_standard_language_code(request.data["sourceLanguage"])
    korean_title = request.data["koreanTitle"]
    genre = request.data["genre"]

    if target_language != "":
        try:  # TODO: content title이 겹칠 경우
            # queryset 나올 수 있음
            content_title = ContentTitles.objects.get(englishTitle=title)

            if content_title.targetLanguage == "" or content_title.koreanTitle == None:
                content_title.targetLanguage = target_language
                content_title.sourceLanguage = source_language
                content_title.koreanTitle = korean_title
                content_title.genre = genre
                content_title.save()
                return content_title

        except ObjectDoesNotExist as e:
            new_content_title = ContentTitles(
                englishTitle=title,
                koreanTitle=korean_title,
                targetLanguage=target_language,
                sourceLanguage=source_language,
                genre=genre,
            )
            new_content_title.save()
            return new_content_title

        return content_title

    else:
        try:
            content_title = ContentTitles.objects.get(
                englishTitle=title, targetLanguage=target_language
            )

        except ObjectDoesNotExist as e:
            new_content_title = ContentTitles(
                englishTitle=title, targetLanguage=target_language
            )
            new_content_title.save()

            return new_content_title

        return content_title


def check_title_is_rrated(request: object):
    if request.data["isRrated"] == "":
        return request, False
    return request, True


def create_rrated_title(title: str, content_title: object):
    # TODO: source language / target language에 상관없이 title이 같으면 모두 update!
    source_language = content_title.source_language
    target_language = content_title.target_language
    client = content_title.client

    try:
        content_title = ContentTitles.objects.get(
            englishTitle=title,
            # sourceLanguage=source_language,
            # targetLanguage=target_language,
        )
        content_title.isRrated = True
        content_title.save()

    except ObjectDoesNotExist as e:
        print("content title이 존재하지 않습니다. 새로운 title을 생성합니다.")
        content_title = ContentTitles(
            englishTitle=title,
            sourceLanguage=source_language,
            targetLanguage=target_language,
            client=client,
            isRrated=True,
        )
        content_title.save()

    return content_title


def check_rrated_title_exist(request: object):
    new_content_title = Contenttitle(request)
    # title = seperate_target_language(request.data["title"])
    # source_language = convert_to_standard_language_code(request.data["sourceLanguage"])
    # target_language = convert_to_standard_language_code(request.data["targetLanguage"])
    title = new_content_title.title

    try:
        p = re.compile(".+(?=\()")
        m = p.search(title)
        filtered_title = m.group()

        content_title = create_rrated_title(filtered_title, new_content_title)

    except AttributeError as e:
        content_title = create_rrated_title(title, new_content_title)

    return content_title


def check_not_rrated_title_exist(request: object):
    new_content_title = Contenttitle(request)
    title = new_content_title.title
    source_language = new_content_title.source_language
    target_language = new_content_title.target_language
    client = new_content_title.client
    # title = seperate_target_language(request.data["title"])
    # source_language = convert_to_standard_language_code(request.data["sourceLanguage"])
    # target_language = convert_to_standard_language_code(request.data["targetLanguage"])

    try:
        p = re.compile(".+(?=\()")
        m = p.search(title)
        filtered_title = m.group()

        content_title, created = ContentTitles.objects.get_or_create(
            englishTitle=filtered_title,
            sourceLanguage=source_language,
            targetLanguage=target_language,
            client=client,
        )

    except AttributeError as e:
        content_title, created = ContentTitles.objects.get_or_create(
            englishTitle=title,
            sourceLanguage=source_language,
            targetLanguage=target_language,
            client=client,
        )
    return content_title


def create_new_content_title_by_translation_info(request: object):

    request, is_rrated = check_title_is_rrated(request)

    if is_rrated:
        content_title = check_rrated_title_exist(request)
        return content_title

    content_title = check_not_rrated_title_exist(request)
    return content_title


def add_resource_role(resource, role):

    resource_role_object, created = ResourceRoles.objects.get_or_create(
        resourceId=resource, role=role
    )
    return resource_role_object


def create_internal_resource(name, new_role):

    try:
        existed_resource = Resources.objects.get(name=name)
        resource_role_list = ResourceRoles.objects.filter(resourceId=existed_resource)

        for resource_role in resource_role_list:
            if resource_role.role == new_role:
                print("{}는 이미 {} role을 가지고 있습니다.".format(name, new_role))
                return existed_resource

            add_resource_role(existed_resource, new_role)
            print("{}의 {} role이 생성되었습니다.".format(name, new_role))
            return existed_resource

    except ObjectDoesNotExist as e:
        print("{}가 resource에 등록되어 있지 않습니다.".format(name))
        new_resource = Resources(name=name, stakeholdersType=StakeholdersType.INTERNAL)
        new_resource.save()

        add_resource_role(new_resource, new_role)
        print("{}의 {} role이 생성되었습니다.".format(name, new_role))

        return new_resource


def create_new_pm_poc_resource(request):
    pm_poc = request.data["pmPoc"]

    if "&" in pm_poc:
        pm_poc_list = pm_poc.split("&")
        pm, poc = pm_poc_list[0], pm_poc_list[-1]

        pm_id = create_internal_resource(pm, Role.PROJECT_MANAGER)
        poc_id = create_internal_resource(poc, Role.POINT_OF_CONTACT)

        return pm_id, poc_id

    pm_id = create_internal_resource(pm_poc, Role.PROJECT_MANAGER)
    return pm_id


def check_resource_is_internal(name, new_role):
    if name == "Internal":
        print("External role이 {}입니다.".format(name))
        create_internal_resource(name, new_role)
        return False
    return name


def create_external_resource(name, email, new_role):
    if check_resource_is_internal(name, new_role):
        try:
            existed_resource = Resources.objects.get(
                name=name, email=email, stakeholdersType=StakeholdersType.EXTERNAL
            )
            resource_role_list = ResourceRoles.objects.filter(
                resourceId=existed_resource
            )

            for resource_role in resource_role_list:
                if resource_role.role == new_role:
                    print("{}는 이미 {} role을 가지고 있습니다.".format(name, new_role))
                    return existed_resource.id

                add_resource_role(existed_resource, new_role)
                print("{}의 {} role이 생성되었습니다.".format(name, new_role))
                return existed_resource.id

        except ObjectDoesNotExist as e:
            print("{}가 resource에 등록되어 있지 않습니다.".format(name))

            try:
                new_resource = Resources(
                    name=name, email=email, stakeholdersType=StakeholdersType.EXTERNAL
                )
                new_resource.save()

                add_resource_role(new_resource, new_role)
                print("{}의 {} role이 생성되었습니다.".format(name, new_role))

            except Exception as e:
                print("{}에 resource가 존재하지 않습니다.".format(new_role))
                return None

            return new_resource.id


def update_pm_poc_id(feedback_object, pm_poc_id):
    if isinstance(feedback_object, QuerySet):
        if isinstance(pm_poc_id, Tuple):
            pm_id, poc_id = pm_poc_id
            feedback_object.update(pmId=pm_id.id, pocId=poc_id.id)
            return feedback_object

        feedback_object.update(pmId=pm_poc_id.id)
        return feedback_object

    else:
        if isinstance(pm_poc_id, Tuple):
            pm_id, poc_id = pm_poc_id
            feedback_object.pmId = pm_id.id
            feedback_object.pocId = poc_id.id

            feedback_object.save()
            return feedback_object

        feedback_object.pmId = pm_poc_id.id

        feedback_object.save()
        return feedback_object


def filter_episode_number_info(episode_number_data: str):
    try:
        p = re.compile(".+(?=\()")
        m = p.search(episode_number_data)
        only_episode_number = m.group()

    except AttributeError as e:
        return episode_number_data

    return only_episode_number


def create_feedback(request):
    # 1. request data 처리
    feedback_date = request.data["feedbackDate"]
    subcategory1 = request.data["subcategory1"]
    subcategory2 = request.data["subcategory2"]
    feedback_comments = request.data["feedbackComments"]
    sentiment_level = request.data["sentimentLevel"]
    episode_number = filter_episode_number_info(request.data["episodeNumber"])
    gid = request.data["gid"]
    sheet_id = request.data["sheetId"]

    # 2. 새로운 data 생성
    title_id = create_new_content_title_by_translation_info(request)
    feedback_date = datetime.strptime(feedback_date, "%B %Y").date()
    feedback_source_id = create_source_sheet(sheet_id, gid)
    error_type_id = get_error_type_id(subcategory2, subcategory1)

    if "-" in episode_number:
        # check translation work already existed
        exist_episode_number = TranslationWorks.objects.filter(
            titleId=title_id
        ).values_list("episodeNumber", flat=True)

        # episode number 처리
        episode_numbers = episode_number.strip().split("-")
        start_episode_number, last_episode_number = int(episode_numbers[0]), int(
            episode_numbers[-1]
        )
        episode_number_list = [
            i for i in range(start_episode_number, last_episode_number + 1)
        ]

        # extract non-exist episode number only
        new_episode_number_list = list(
            set(episode_number_list).difference(set(exist_episode_number))
        )

        if not new_episode_number_list:
            print("모든 translationWork가 DB에 존재합니다.")

            try:
                translation_work_objects = TranslationWorks.objects.filter(
                    titleId=title_id, episodeNumber__in=episode_number_list
                )

                word_count_dict = {
                    work.id: work.wordCount for work in translation_work_objects
                }
                quality_point_dict = {
                    k: get_quality_point(v, error_type_id, sentiment_level)
                    for k, v in word_count_dict.items()
                }
                quality_level_dict = {
                    k: get_quality_level(v) for k, v in quality_point_dict.items()
                }

                feedback_objects_list = [
                    Feedbacks(
                        translationWorkId=translation_work_objects[i],
                        feedbackDate=feedback_date,
                        feedbackComments=feedback_comments,
                        sentimentLevel=sentiment_level,
                        errorTypeId=error_type_id,
                        feedbackSourceId=feedback_source_id,
                        qualityPoint=quality_point_dict[translation_work_objects[i].id],
                        qualityLevel=quality_level_dict[translation_work_objects[i].id],
                    )
                    for i in range(len(translation_work_objects))
                ]

                new_feedback_objects = Feedbacks.objects.bulk_create(
                    feedback_objects_list
                )

            except TypeError as e:
                print("word count 정보가 존재하지 않습니다.")

                feedback_objects_list = [
                    Feedbacks(
                        translationWorkId=translation_work_objects[i],
                        feedbackDate=feedback_date,
                        feedbackComments=feedback_comments,
                        sentimentLevel=sentiment_level,
                        errorTypeId=error_type_id,
                        feedbackSourceId=feedback_source_id,
                    )
                    for i in range(len(translation_work_objects))
                ]

                new_feedback_objects = Feedbacks.objects.bulk_create(
                    feedback_objects_list
                )

            # TODO: feedback 덮어쓰기 이슈 없애기
            # TODO: 조건문 포함(translation work id가 quality level/point list의 key와 일치할 경우)
            # TODO: 기존에 존재하는 object가 있을 경우 모두 다 해당 로직 포함시킴

            return new_feedback_objects

        else:
            object_list = [
                TranslationWorks(
                    titleId=title_id, episodeNumber=new_episode_number_list[i]
                )
                for i in range(len(new_episode_number_list))
            ]

            translation_work_objects = TranslationWorks.objects.bulk_create(object_list)

            feedback_objects_list = [
                Feedbacks(
                    translationWorkId=translation_work_objects[i],
                    feedbackDate=feedback_date,
                    feedbackComments=feedback_comments,
                    sentimentLevel=sentiment_level,
                    errorTypeId=error_type_id,
                    feedbackSourceId=feedback_source_id,
                )
                for i in range(len(translation_work_objects))
            ]
            new_feedback_objects = Feedbacks.objects.bulk_create(feedback_objects_list)

            return new_feedback_objects

    elif "," in episode_number:
        exist_episode_number = TranslationWorks.objects.filter(
            titleId=title_id
        ).values_list("episodeNumber", flat=True)
        episode_numbers = episode_number.strip().split(",")
        episode_number_list = list(map(int, episode_numbers))

        # extract non-exist episode number only
        new_episode_number_list = list(
            set(episode_number_list).difference(set(exist_episode_number))
        )

        if not new_episode_number_list:
            print("모든 translationWork가 DB에 존재합니다.")

            try:
                translation_work_objects = TranslationWorks.objects.filter(
                    titleId=title_id, episodeNumber__in=episode_number_list
                )

                word_count_dict = {
                    work.id: work.wordCount for work in translation_work_objects
                }
                quality_point_dict = {
                    k: get_quality_point(v, error_type_id, sentiment_level)
                    for k, v in word_count_dict.items()
                }
                quality_level_dict = {
                    k: get_quality_level(v) for k, v in quality_point_dict.items()
                }

                feedback_objects_list = [
                    Feedbacks(
                        translationWorkId=translation_work_objects[i],
                        feedbackDate=feedback_date,
                        feedbackComments=feedback_comments,
                        sentimentLevel=sentiment_level,
                        errorTypeId=error_type_id,
                        feedbackSourceId=feedback_source_id,
                        qualityPoint=quality_point_dict[translation_work_objects[i].id],
                        qualityLevel=quality_level_dict[translation_work_objects[i].id],
                    )
                    for i in range(len(translation_work_objects))
                ]

                new_feedback_objects = Feedbacks.objects.bulk_create(
                    feedback_objects_list
                )

            except TypeError as e:
                print("word count 정보가 존재하지 않습니다.")
                feedback_objects_list = [
                    Feedbacks(
                        translationWorkId=translation_work_objects[i],
                        feedbackDate=feedback_date,
                        feedbackComments=feedback_comments,
                        sentimentLevel=sentiment_level,
                        errorTypeId=error_type_id,
                        feedbackSourceId=feedback_source_id,
                    )
                    for i in range(len(translation_work_objects))
                ]

                new_feedback_objects = Feedbacks.objects.bulk_create(
                    feedback_objects_list
                )

            # new_feedback_objects = Feedbacks.objects.filter(
            #     translationWorkId__in=translation_work_objects
            # ).update(
            #     feedbackDate=feedback_date,
            #     feedbackComments=feedback_comments,
            #     sentimentLevel=sentiment_level,
            #     errorTypeId=error_type_id,
            #     feedbackSourceId=feedback_source_id,
            # )

            # new_feedback_objects = Feedbacks.objects.filter(
            #     translationWorkId__in=translation_work_objects
            # )

            # for i in len(new_feedback_objects):
            #     new_feedback_objects[i].feedbackDate = feedback_date
            #     new_feedback_objects[i].feedbackComments = feedback_comments
            #     new_feedback_objects[i].sentimentLevel = sentiment_level
            #     new_feedback_objects[i].errorTypeId = error_type_id
            #     new_feedback_objects[i].feedbackSourceId = feedback_source_id

            #     new_feedback_objects[i].qualityLevel = quality_level_list[i]
            #     new_feedback_objects[i].qualityPoint = quality_point_list[i]

            # Feedbacks.objects.bulk_update(
            #     new_feedback_objects,
            #     [
            #         "feedbackDate",
            #         "feedbackComments",
            #         "sentimentLevel",
            #         "errorTypeId",
            #         "feedbackSourceId",
            #         "qualityLevel",
            #         "qualityPoint",
            #     ],
            # )

            return new_feedback_objects

        else:
            object_list = [
                TranslationWorks(
                    titleId=title_id, episodeNumber=new_episode_number_list[i]
                )
                for i in range(len(new_episode_number_list))
            ]

            translation_work_objects = TranslationWorks.objects.bulk_create(object_list)

            feedback_objects_list = [
                Feedbacks(
                    translationWorkId=translation_work_objects[i],
                    feedbackDate=feedback_date,
                    feedbackComments=feedback_comments,
                    sentimentLevel=sentiment_level,
                    errorTypeId=error_type_id,
                    feedbackSourceId=feedback_source_id,
                )
                for i in range(len(translation_work_objects))
            ]
            new_feedback_objects = Feedbacks.objects.bulk_create(feedback_objects_list)

            return new_feedback_objects

    else:
        print(title_id)
        translation_work_id, created = TranslationWorks.objects.get_or_create(
            titleId=title_id, episodeNumber=int(float(episode_number))
        )

        if created:
            new_feedback_object = Feedbacks(
                translationWorkId=translation_work_id,
                feedbackDate=feedback_date,
                feedbackComments=feedback_comments,
                sentimentLevel=sentiment_level,
                errorTypeId=error_type_id,
                feedbackSourceId=feedback_source_id,
            )
        else:
            word_count = translation_work_id.wordCount

            try:
                quality_point = get_quality_point(
                    word_count, error_type_id, sentiment_level
                )
                quality_level = get_quality_level(quality_point)

                new_feedback_object = Feedbacks(
                    translationWorkId=translation_work_id,
                    feedbackDate=feedback_date,
                    feedbackComments=feedback_comments,
                    sentimentLevel=sentiment_level,
                    errorTypeId=error_type_id,
                    feedbackSourceId=feedback_source_id,
                    qualityPoint=quality_point,
                    qualityLevel=quality_level,
                )

            except TypeError as e:
                new_feedback_object = Feedbacks(
                    translationWorkId=translation_work_id,
                    feedbackDate=feedback_date,
                    feedbackComments=feedback_comments,
                    sentimentLevel=sentiment_level,
                    errorTypeId=error_type_id,
                    feedbackSourceId=feedback_source_id,
                )

        new_feedback_object.save()
        print("데이터 저장이 완료되었습니다.")
        return new_feedback_object


def check_word_count_and_update(
    title_object, episode_number, target_text, word_count, word_count_sheet_id
):
    print(title_object, word_count_sheet_id)
    feedback = Feedbacks.objects.filter(
        titleId=title_object, episodeNumber=episode_number
    )

    if len(feedback) > 0:
        feedback.update(
            targetText=target_text,
            wordCount=word_count,
            wordCountSourceId=word_count_sheet_id,
        )

        return feedback

    new_feedback_data = Feedbacks(
        titleId=title_object,
        episodeNumber=episode_number,
        targetText=target_text,
        wordCount=word_count,
        wordCountSourceId=word_count_sheet_id,
    )
    new_feedback_data.save()
    return new_feedback_data


def create_word_count(one_episode_data):
    one_episode_data = one_episode_data.data

    # 1. title 추출
    title = one_episode_data["title"]
    # 2. target language 추출
    target_language = ""  # 차후 title에 정규표현식 적용 필요

    # 3. 기타 데이터 추출
    sheet_id = one_episode_data["sheetId"]
    gid = one_episode_data["gid"]
    episode_number = int(one_episode_data["episodeNumber"])
    target_text = ast.literal_eval(one_episode_data["targetText"])
    target_text = " ".join(target_text)
    word_count = len(target_text.split())

    # 4. sourceSheetData 확인
    source_sheet_id = create_source_sheet(sheet_id, gid)

    # 5. ContentTitles에 있는지 확인(englishTitle)
    title_id = create_new_content_title(title, target_language)

    # 6. 새로운 xxfeedback 객체 생성
    new_feedback_data = check_word_count_and_update(
        title_id, episode_number, target_text, word_count, source_sheet_id
    )
    return new_feedback_data


def extract_episode_number_range(translation_sheets_name: str):
    f = re.compile("(?<=EP.).+")
    episode_number_range = f.search(translation_sheets_name).group()
    return episode_number_range


def seperate_data_from_title(translation_sheets_name: str):

    # target language
    underscore_idices = [
        i
        for i in range(len(translation_sheets_name))
        if translation_sheets_name[i] == "_"
    ]
    source_language = translation_sheets_name[
        underscore_idices[0] + 1 : underscore_idices[1]
    ]
    target_language = translation_sheets_name[
        underscore_idices[1] + 1 : underscore_idices[-1]
    ]
    source_language_code = convert_to_standard_language_code(source_language)
    target_language_code = convert_to_standard_language_code(target_language)

    # content title
    content_title = translation_sheets_name[: underscore_idices[0]]

    # last episode number
    # EP. 뒤
    episode_number_range = extract_episode_number_range(translation_sheets_name)
    # - 뒤
    f = re.compile("(?<=-).+")
    last_episode_number = f.search(episode_number_range).group()

    return (
        content_title,
        source_language_code,
        target_language_code,
        last_episode_number,
    )


def check_translation_work_exist(data: dict):
    # TODO: 만약 객체가 이미 존재하고 있으나 이전에 없는 정보가 있을 경우 update
    # update로 인해 고려해야 할 가짓수가 많아짐
    translation_sheets_name = data["title"]
    episode_number = int(float(data["episodeNumber"]))

    (
        content_title,
        source_language_code,
        target_language_code,
        last_episode_number,
    ) = seperate_data_from_title(translation_sheets_name)
    content_title_object = ContentTitles.objects.get_or_create(
        englishTitle=content_title,
        targetLanguage=target_language_code,
        sourceLanguage=source_language_code,
    )

    try:
        translation_work = TranslationWorks.objects.get(
            titleId=content_title_object[0], episodeNumber=episode_number
        )
        return translation_work

    except ObjectDoesNotExist as e:
        return False


def create_or_update_translation_work(
    title: object, episode_number: int, translator: object = None, qcer: object = None
):
    if translator == None and qcer == None:
        translation_work = TranslationWorks.objects.get_or_create(
            titleId=title, episodeNumber=episode_number
        )

        translation_work = translation_work[0]

        return translation_work

    try:
        translation_work = TranslationWorks.objects.get(
            titleId=title, episodeNumber=episode_number
        )
        translation_work.translatorId = translator
        translation_work.qcerId = qcer
        translation_work.save()

        return translation_work

    except ObjectDoesNotExist as e:
        translation_work = TranslationWorks(
            titleId=title,
            episodeNumber=episode_number,
            translatorId=translator,
            qcerId=qcer,
        )
        translation_work.save()

        return translation_work


def convert_json_to_list(data: str):
    result = ast.literal_eval(data)
    return result


def sent_list_to_string_word_count(data: str):
    sent_list = convert_json_to_list(data)
    sent_string = " ".join(map(str, sent_list))
    # get wordcount
    # target text string split
    sent_words = sent_string.split()

    # length count
    word_count = len(sent_words)
    return sent_string, word_count


def create_translation_information(data: dict):
    # print("데이터를 확인합니다:", data)
    # print(
    #     "targetTextAfterQc & existedQcValueInfo:",
    #     data["targetTextAfterQc"],
    #     data["existedQcValueInfo"],
    # )
    if data["targetTextAfterQc"] == None or data["targetTextAfterQc"] == "":
        print("QC 데이터가 존재하지 않습니다.")

        translation_sheets_name = data["title"]
        sheet_id = data["sheetId"]
        gid = data["gid"]
        episode_number = int(float(data["episodeNumber"]))
        target_text = convert_json_to_list(data["targetText"])
        target_text_string, word_count = sent_list_to_string_word_count(
            data["targetText"]
        )

        # 0. 데이터 생성
        # title에서 content title, target language, last episode number 분리
        (
            content_title,
            source_language_code,
            target_language_code,
            last_episode_number,
        ) = seperate_data_from_title(translation_sheets_name)

        # title 객체 title, episode number, target language로 조회 # class 변경?
        content_title_object = ContentTitles.objects.get_or_create(
            englishTitle=content_title,
            sourceLanguage=source_language_code,
            targetLanguage=target_language_code,
        )

        # get wordcountsource id
        word_count_source_sheet = create_source_sheet(sheet_id, gid)

        # create translation work
        # TODO: quality point, quality level 계산
        translation_work = TranslationWorks(
            titleId=content_title_object[0],
            episodeNumber=episode_number,
            targetText=target_text_string,
            wordCount=word_count,
            wordCountSourceId=word_count_source_sheet,
        )
        translation_work.save()

        # create translation sentences
        sentence_length = len(target_text)
        sentenct_object_list = [
            TranslationSentences(
                translationWorkId=translation_work, sentence=target_text[i]
            )
            for i in range(sentence_length)
        ]
        translation_sentences = TranslationSentences.objects.bulk_create(
            sentenct_object_list
        )

        return translation_work

    # TODO: class 활용하기 : models의 TranslationWorks나 다른 class를 만들어 처리하면 된다. serializer의 class를 사용할 수도 있음!
    # TODO: 중복 코드 제거하기

    else:
        translation_sheets_name = data["title"]
        sheet_id = data["sheetId"]
        gid = data["gid"]
        episode_number = int(float(data["episodeNumber"]))
        target_text = convert_json_to_list(data["targetText"])
        target_text_string, word_count = sent_list_to_string_word_count(
            data["targetText"]
        )
        target_text_qc_string = sent_list_to_string_word_count(
            data["targetTextAfterQc"]
        )[0]
        exist_qc_data_info = convert_json_to_list(data["existedQcValueInfo"])
        existed_qc_idices = [
            target_text.index(k) for k in exist_qc_data_info.keys() if k != ""
        ]
        print(exist_qc_data_info)
        print(existed_qc_idices)

        # 0. 데이터 생성
        # title에서 content title, target language, last episode number 분리
        (
            content_title,
            source_language_code,
            target_language_code,
            last_episode_number,
        ) = seperate_data_from_title(translation_sheets_name)

        # title 객체 title, episode number, target language로 조회 # class 변경?
        content_title_object = ContentTitles.objects.get_or_create(
            englishTitle=content_title,
            sourceLanguage=source_language_code,
            targetLanguage=target_language_code,
        )

        # get wordcountsource id
        word_count_source_sheet = create_source_sheet(sheet_id, gid)

        # create translation work
        translation_work = TranslationWorks(
            titleId=content_title_object[0],
            episodeNumber=episode_number,
            targetText=target_text_string,
            targetTextAfterQc=target_text_qc_string,
            wordCount=word_count,
            wordCountSourceId=word_count_source_sheet,
        )
        translation_work.save()

        # create translation sentences
        sentence_length = len(target_text)
        sentenct_object_list = [
            TranslationSentences(
                translationWorkId=translation_work,
                sentence=target_text[i],
                qcSentence=exist_qc_data_info[target_text[i]],
            )
            if i in existed_qc_idices
            else TranslationSentences(
                translationWorkId=translation_work, sentence=target_text[i]
            )
            for i in range(sentence_length)
        ]
        translation_sentences = TranslationSentences.objects.bulk_create(
            sentenct_object_list
        )

        return translation_work


def read_notion_database(database_id=database_id, headers=headers):
    """Read/Get notion database's data

    Args:
        database_id (_string_, optional): _Notion database id_. Defaults to database_id.
        headers (_string_, optional): _request header_. Defaults to headers.
    """
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

    payload = {"page_size": 10}
    response = requests.request("POST", read_url, json=payload, headers=headers)

    db_data = json.loads(response.text)
    print(type(db_data))
    result = json.dumps(db_data, indent=4)
    # print(result)

    return db_data


def create_notion_page(request_post, database_id=database_id, headers=headers):
    """Insert data to Notion database.

    Args:
        request_post (_dict_): _Data set from POST request_
        database_id (_string_, optional): _Notion database id_. Defaults to database_id.
        headers (_string_, optional): _request header_. Defaults to headers.
    """

    url = f"https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {"title": [{"text": {"content": request_post["title"]}}]},
            "Feedback Date": {"date": {"start": request_post["feedbackDate"]}},
            "Delivery Date": {"date": request_post["deliveryDate"]},
            "Client": {"multi_select": [{"name": request_post["client"]}]},
            "Ep.No.": {
                "rich_text": [{"text": {"content": request_post["episodeNumber"]}}]
            },
            "Language": {
                "rich_text": [{"text": {"content": request_post["language"]}}]
            },
            "Genre": {"rich_text": [{"text": {"content": request_post["genre"]}}]},
            "PM/POC": {"rich_text": [{"text": {"content": request_post["pmPoc"]}}]},
            "Resource Email": {
                "rich_text": [{"text": {"content": request_post["resourceEmail"]}}]
            },
            "Resource Name": {
                "rich_text": [{"text": {"content": request_post["resourceName"]}}]
            },
            "Resource Role": {
                "rich_text": [{"text": {"content": request_post["resourceRole"]}}]
            },
            "Source Language": {
                "rich_text": [{"text": {"content": request_post["sourceLanguage"]}}]
            },
            "Target Language": {
                "rich_text": [{"text": {"content": request_post["targetLanguage"]}}]
            },
            "Feedback Comments": {
                "rich_text": [{"text": {"content": request_post["feedbackComments"]}}]
            },
        },  #
    }

    new_data = json.dumps(payload, indent=4, sort_keys=True, default=str)
    response = requests.request("POST", url, headers=headers, data=new_data)
    print(response.text)
    return response.text


def delete_notion_data(page_id):
    """delete data from Notion database.

    Args:
        page_id (_string_): _Data's page id_
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}"
    headers = {
        "Authorization": "Bearer " + token,
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }

    response = requests.request("DELETE", url, headers=headers)
    print(response.text)


def update_notion_data(request_post, page_id):
    """update Notion database's data.

    Args:
        page_id (_string_): _Data's page id_
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {
        "properties": {
            "Title": {"title": [{"text": {"content": request_post["title"]}}]},
            "Feedback Date": {"date": {"start": request_post["feedbackDate"]}},
            "Delivery Date": {"date": {"start": request_post["deliveryDate"]}},
            "Client": {"multi_select": [{"name": request_post["client"]}]},
            "Ep.No.": {
                "rich_text": [{"text": {"content": request_post["episodeNumber"]}}]
            },
            "Language": {
                "rich_text": [{"text": {"content": request_post["language"]}}]
            },
            "Genre": {"rich_text": [{"text": {"content": request_post["genre"]}}]},
            "PM/POC": {"rich_text": [{"text": {"content": request_post["pmPoc"]}}]},
            "Resource Info": {
                "rich_text": [{"text": {"content": request_post["resourceInfo"]}}]
            },
        },
        "archived": False,
    }

    response = requests.request("PATCH", url, json=payload, headers=headers)
    print(response.text)


# Memsource Data gathering 로직 추가
# s3 저장소 이용하는 방법 찾아보기
def check_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error : Creating Directory" + path)


def get_memsource_data():
    path = "../TMData"
    check_dir(path)
    headers = get_header()
    datatype = 0 # 기존 : 0, 신규 : 1
    # for문을 사용하는 이유
    # Memsource api 파라미터에서 pagenumber값을 넣어서 55개씩 데이터를 끊어서 가져올수있음.
    # 현재 홈페이지에 대략 120개 데이터가 있기때문에 0~2까지 포문으로 넣어줌.(0~55, 56~100,101~)
    # 자동으로 페이지값을 읽어오는 기능이 필요할 듯.
    #for i in range(0, 4):
        #download_memsource_data(headers, i, path)  # 파일 쓰기
    insert_to_db(path,datatype)  # 테이블 데이터와 중복체크해서 데이터 읽기
    return True


# memsource token 가져오는 함수
def get_header():
    url = "https://cloud.memsource.com/web/api2/v1/auth/login"

    logininfo = {"userName": "projects@glozinc.com", "password": "gloqwer!!"}
    response = requests.post(url, json=logininfo)
    token = response.json()["token"]
    headers = {"Authorization": "ApiToken " + token}

    return headers


# Memsource API를 호출해서 .tmx 파일로 다운로드.
def download_memsource_data(headers, pagenumber, path):
    url = "https://cloud.memsource.com/web/api2/v1/transMemories"
    params = {"pageNumber": str(pagenumber)}
    response = requests.get(url, params=params, headers=headers)
    token = response.json()
    # 파일 관리
    for transmemory in token["content"]:

        print(
            "transmemoryID:",
            transmemory["internalId"],
            ",",
            "uid:",
            transmemory["uid"],
            ",",
            "name:",
            transmemory["name"],
            "targetlang",
            transmemory["targetLangs"][0],
            "dateCreated",
            transmemory['dateCreated']
        )
        uid = transmemory["uid"]
        name = transmemory["name"].replace("/", "")
        export_memsourcememory(headers, name, uid, path)


def export_memsourcememory(headers, filename, uid, path):
    url = "https://cloud.memsource.com/web/api2/v2/transMemories/" + uid + "/export"

    payload = {"callbackUrl": "http://localhost/"}
    response = requests.post(url, json=payload, headers=headers)

    # 비동기요청 id 값으로 파일을 다운로드.
    asyncdata = response.json()["asyncRequest"]["id"]
    sleep(5)
    download_exportdata(headers, filename, asyncdata, path, uid)


def download_exportdata(headers, filename, asyncdata, path, uid):
    exportfilename = filename
    url = (
        "https://cloud.memsource.com/web/api2/v1/transMemories/downloadExport/"
        + asyncdata
    )
    data = {"format": "TMX"}
    # 404 응답이 오는 경우가 있어서 try 구문 추가
    try:
        response = requests.get(url, data=data, headers=headers)
        response.raise_for_status()
        # 오류가 발생하지않은 경우에만 파일로 Write
        with open(path + "/" + exportfilename + ".tmx", "wb") as output:
            output.write(response.content)  # 로컬에 다운
            # return filename

    except requests.exceptions.Timeout as e:
        print("Timeout Error : ", e)

    except requests.exceptions.ConnectionError as e:
        print("Error Connecting : ", e)

    except requests.exceptions.HTTPError as e:
        print(exportfilename + "Http Error : ", e)

    # Any Error except upper exception
    except requests.exceptions.RequestException as e:
        print("AnyException : ", e)
        raise SystemExit(e)


def insert_to_db(path,datatype):
    # path  = '../TMData'
    file_list = os.listdir(path)
    for file in file_list:
        filename = file.replace(".tmx", "")
        print(filename)
        # client 추출하는 부분 추가
        client, webnovel_title = export_client_data(filename)
        if client in webnovel_clients:
            title_lang = check_title_language(webnovel_title)
            if title_lang == 1:  # 영어
                check = ContentTitles.objects.filter(englishTitle=webnovel_title)
            else:  # 한국어
                check = ContentTitles.objects.filter(koreanTitle=webnovel_title)

            if check.exists():
                print(filename, "이미 db에 존재")
            else:
                if filename != ".DS_Store":
                    print(filename, "신규데이터")
                    data = read_tmxfile(filename, path,datatype)


# 파일 이름 한글/영어 구분
# 정규표현식을 이용해서 특수문자, 숫자 제거하기
def check_title_language(title):
    title = re.sub("[^A-Za-z가-힣]", "", title)
    reg = re.compile(r"[a-zA-Z]")
    if reg.match(title):  # 영어 title
        return 1

    else:  # 한글 title
        return 0


def read_tmxfile(filename, path,datatype):
    print('testtest',path + "/" + filename + ".tmx",filename)
    try:
        tree = ET.parse(path + "/" + filename + ".tmx")
        root = tree.getroot()
        TM = []

        for node in root.find("body"):
            # TM ID 값 추출
            data = []
            attr = node.attrib
            for x in node:
                attr = x.attrib
                lang = attr.get("{http://www.w3.org/XML/1998/namespace}lang")
                completed_date = attr.get("changedate")
                if completed_date != None:
                    completed_date =  completed_date.split('T')[0]
                    completed_date = datetime.datetime.strptime(completed_date,"%Y%m%d")
                    data.append(completed_date)
                
                data.append(lang)

                for y in x:
                    if y.attrib.get("type") == "filename":
                        data.append(y.text)

                    if y.tag == "seg":  # 소스 타겟 텍스트
                        data.append(y.text)

            TM.append(data)  # [sourcelang,targetlang,sourcetext,targettext,fileanme]
        
        
        insert_translations_data(filename, TM,datatype)
    except HTTPError as e:
        print(e)
        

# translationworks 테이블에 담기위해 각 문장을 merge.
def convert_to_sentence(sentence):
    key = sentence.keys()
    data = []
    for filename in key:
        arr = sentence[filename]  # 각 문장
        for i in range(0, len(arr)):
            if arr[i] == None:
                arr[i] = ""  # None 값 처리
        sentences = " ".join(arr)
        data.append([filename, sentences])
    return data


def export_client_data(filename):
    idx = filename.find("]")
    # filename 예시 : [NAVER] Title Ep.1-5
    if idx > 0:
        client = filename[1:idx].upper()
        webnovel_title = filename[idx + 1 :]
    else:
        client = ""
        webnovel_title = filename
    return client, webnovel_title


def create_sentence(df, translation):
    for index, row in df.iterrows():
        try:
            if row["targettext"] is not None:
                TranslationSentences_object = TranslationSentences(
                    translationWorkId=translation,
                    sentence=row["targettext"],
                    sourceSentence=row["sourcetext"],
                )  # row['id'],  # contenttitle값
                TranslationSentences_object.save()
        except ValueError as e:
            print(e)


# 신규 데이터만 가져오는 로직 추가
# db contenttitle 에서 create 된 마지막 데이터를 읽어오기
# 날짜를 current date 에 담고, 그거보다 이후에 들어온 데이터들만 읽어오기
def get_new_memsource_data():
    # current_data = ContentTitles.objects.latest('updatedAt')
    today = datetime.today().strftime("%Y%m%d")
    path = "../TMData/" + today  # 다운로드 날짜로 폴더 만들기
    check_dir(path)
    headers = get_header()
    datatype= 1 #(신규 : 1, 기존: 0)
    # 신규 데이터만 로컬에 다운받기
    for i in range(0, 4):
        download_memsource_new_data(headers, i, path)  # 파일 쓰기
    insert_to_db(path,datatype)
    return True


# Memsource API를 호출해서 .tmx 파일로 다운로드.
# 파일 네이밍 규칙 영문 타이틀_source language code_target language code_EP.시작 에피소드 번호-끝 에피소드 번호
def download_memsource_new_data(headers, pagenumber, path):
    url = "https://cloud.memsource.com/web/api2/v1/transMemories"
    params = {"pageNumber": str(pagenumber)}
    response = requests.get(url, params=params, headers=headers)
    token = response.json()
    currentdate = ContentTitles.objects.order_by("createdAt")[0]
    currentdate = currentdate.createdAt

    # 파일 관리
    for transmemory in token["content"]:
        format = "%Y-%m-%dT%H:%M:%S%z"
        tm_createdAt = datetime.strptime(transmemory["dateCreated"], format)

        # 이미 수집한 데이터를 제외하고 신규 데이터 수집.
        if str(currentdate) <= str(tm_createdAt):  # db에 들어온 이후 날짜부터 insert.
            uid = transmemory["uid"]
            name = transmemory["name"].replace("/", "")
            export_memsourcememory(headers, name, uid, path)
            print(
                "createdAt:",
                transmemory["dateCreated"],
                "transmemoryID:",
                transmemory["internalId"],
                ",",
                "uid:",
                transmemory["uid"],
                ",",
                "name:",
                transmemory["name"],
                "targetlanguage",
                transmemory["targetLangs"][0],
                "dateCreated",
                transmemory['dateCreated']
            )

# 신규 데이터는 해당 함수로 담아줘야함.(첫번째 적재 테스트 진행하는 함수)
def insert_translations_data(filename, tmdata,datatype):
    old_new_type = datatype
    try:
        df = pd.DataFrame(
            tmdata,
            columns=[
                "sourcelang",
                "sourcetext",
                "completeddate",
                "targetlang",
                "filename",
                "targettext",
            ],
        )

        if df.empty == False:
            # 표준언어코드  추가
            sourelanguage = convert_to_standard_language_code(df["sourcelang"][0])
            targetlanguage = convert_to_standard_language_code(df["targetlang"][0])
            completed_date = df["completeddate"][0]
            # 파일 이름 한글/영어 구분
            title_lang = check_title_language(filename)
            # client 추출하는 부분 추가
            client, webnovel_title = export_client_data(filename)
            # print(client,webnovel_title)
            if title_lang == 1:  # 영어 title
                content_object = ContentTitles(
                    sourceLanguage=sourelanguage,
                    targetLanguage=targetlanguage,
                    englishTitle=webnovel_title,
                    client=client,
                    workType="webnovel",
                    completedAt = completed_date
                )

                content_object.save()
            else:  # 한글 title
                content_object = ContentTitles(
                    sourceLanguage=sourelanguage,
                    targetLanguage=targetlanguage,
                    koreanTitle=webnovel_title,
                    client=client,
                    workType="webnovel",
                    completedAt = completed_date
                )
                # client='Memsource') # client값 넘어오지않음.
                content_object.save()

            # TranslationWork 테이블에 담기위한 merge 작업.
            targetsentence = dict(df.groupby("filename")["targettext"].apply(list))
            sourcesentence = dict(df.groupby("filename")["sourcetext"].apply(list))

            targetdata = convert_to_sentence(targetsentence)
            sourcedata = convert_to_sentence(sourcesentence)

            df_target = pd.DataFrame(targetdata, columns=["filename", "targetdata"])
            df_source = pd.DataFrame(sourcedata, columns=["filename", "sourcedata"])

            translation_data = pd.merge(df_target, df_source, on="filename")

            for index, row in translation_data.iterrows():
                # 신규 데이터부터 파일 네이밍 규칙 적용(2022.06.28)
                # 영문 타이틀_source language code_target language code_EP.시작 에피소드 번호-끝 에피소드 번호
                job_filename = str(row["filename"])
                number = job_filename.split("_EP.")
                # 에피소드별로 sentence 담기
                df_sentence = df[df["filename"] == job_filename]

                # print("에피소드 넘버:", number)
                if old_new_type == 1 : # 신규
                    if len(number) > 1:  # Split 되었을때
                        Episodenumber = re.sub(r"[^0-9]", "", number[1])
                    else:
                        Episodenumber = 0
                else:
                    Episodenumber = re.sub(r"[^0-9]", "", job_filename)
                    if Episodenumber == "" or int(Episodenumber) > 100:
                        Episodenumber = 0
                    

                # 신규데이터
                try:
                    # targettext (영어) 공백기준으로 wordcount
                    if str(type(row["targetdata"])) == "<class 'str'>":
                        wordCount = len(row["targetdata"].split())
                    else:
                        wordCount = 0

                    transmemory_obejct = TranslationWorks(
                        titleId=content_object,
                        episodeNumber=Episodenumber,
                        sourceText=row["sourcedata"],
                        targetText=row["targetdata"],
                        wordCount=wordCount,
                    )  # row['id'],  # contenttitle값
                    transmemory_obejct.save()
                    create_sentence(
                        df_sentence, transmemory_obejct
                    )  # translationsentences 테이블

                except ValueError as e:
                    print(e, type(e))

        return True
    except ValueError as e:
        print("컬럼 개수가 맞지 않습니다.")
        return False

'''
# old 데이터는 해당 함수로 담아줘야함.(첫번째 적재 테스트 진행하는 함수)
def insert_translations_old_data(filename, tmdata):
    try:
        df = pd.DataFrame(
            tmdata,
            columns=[
                "sourcelang",
                "sourcetext",
                "targetlang",
                "filename",
                "targettext",
            ],
        )

        if df.empty == False:
            # 표준언어코드  추가
            sourelanguage = convert_to_standard_language_code(df["sourcelang"][0])
            targetlanguage = convert_to_standard_language_code(df["targetlang"][0])

            # 파일 이름 한글/영어 구분
            title_lang = check_title_language(filename)
            # client 추출하는 부분 추가
            client, webnovel_title = export_client_data(filename)

            # print(client,webnovel_title)
            if title_lang == 1:  # 영어 title
                content_object = ContentTitles(
                    sourceLanguage=sourelanguage,
                    targetLanguage=targetlanguage,
                    englishTitle=webnovel_title,
                    client=client,
                    workType="webnovel",
                )

                content_object.save()
            else:  # 한글 title
                content_object = ContentTitles(
                    sourceLanguage=sourelanguage,
                    targetLanguage=targetlanguage,
                    koreanTitle=webnovel_title,
                    client=client,
                    workType="webnovel",
                )
                # client='Memsource') # client값 넘어오지않음.
                content_object.save()

            # TranslationWork 테이블에 담기위한 merge 작업.
            targetsentence = dict(df.groupby("filename")["targettext"].apply(list))
            sourcesentence = dict(df.groupby("filename")["sourcetext"].apply(list))

            targetdata = convert_to_sentence(targetsentence)
            sourcedata = convert_to_sentence(sourcesentence)

            df_target = pd.DataFrame(targetdata, columns=["filename", "targetdata"])
            df_source = pd.DataFrame(sourcedata, columns=["filename", "sourcedata"])

            translation_data = pd.merge(df_target, df_source, on="filename")

            for index, row in translation_data.iterrows():
                # 영문 타이틀_source language code_target language code_EP.시작 에피소드 번호-끝 에피소드 번호
                job_filename = str(row["filename"])
                df_sentence = df[df["filename"] == job_filename]
                # EP가 있다면 EP로 split 하는 방법도 있음
                Episodenumber = re.sub(r"[^0-9]", "", job_filename)
                if Episodenumber == "" or int(Episodenumber) > 100:
                    Episodenumber = 0

                # 신규데이터
                try:
                    # targettext (영어) 공백기준으로 wordcount
                    if str(type(row["targetdata"])) == "<class 'str'>":
                        wordCount = len(row["targetdata"].split())
                    else:
                        wordCount = 0

                    transmemory_obejct = TranslationWorks(
                        titleId=content_object,
                        episodeNumber=Episodenumber,
                        sourceText=row["sourcedata"],
                        targetText=row["targetdata"],
                        wordCount=wordCount,
                    )  # row['id'],  # contenttitle값
                    transmemory_obejct.save()
                    create_sentence(
                        df_sentence, transmemory_obejct
                    )  # translationsentences 테이블

                except ValueError as e:
                    print(e, type(e))

        return True
    except ValueError as e:
        print("컬럼 개수가 맞지 않습니다.")
        return False

'''