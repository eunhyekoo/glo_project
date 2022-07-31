MESSAGE_200 = 'Completed'
MESSAGE_404 = 'Error Type not found.'
MESSAGE_400 = 'Bad request!'


def word_count_response(feedback_text, word_count, work_type='feedback'):
    return {
        "data" : {
            "wordCount" : word_count,
            work_type : feedback_text,
        },
        "statusCode" : 200
    }
    
def error_response(status_code, message=MESSAGE_404):
    return {
        "message": message,
        "statusCode": status_code
    }


def completed_response(status_code, message=MESSAGE_200):
    return{
        "message":message,
        "statusCode":status_code
    }