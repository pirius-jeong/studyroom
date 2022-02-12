from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

from ..models import Sms, Account
import logging
import hashlib, hmac, base64, requests, time, json

logger = logging.getLogger('studyroom')

# naver cloud platform SMS API
sid = "ncp:sms:kr:280385014707:kizacademy"

sms_uri = "/sms/v2/services/{}/messages".format(sid)
sms_url = "https://sens.apigw.ntruss.com{}".format(sms_uri)

acc_key_id = "Hvhi0tnLbZGRow5s6352"
acc_sec_key = b"yidS0gTc0q3GxGs2G5fhsfwwPVXFvj51UaKAlqNP"
from_no = "01090787297"

@login_required(login_url='common:login')
def sms_list(request):
    logger.info("INFO 레벨로 출력")
    """
    SMS 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    name = request.GET.get('name', '')  # 검색어

    # 조회
    sms_list = Sms.objects.order_by('-requestTime')
    if name:
        sms_list = sms_list.filter(
            Q(account__student__name__icontains=name)   # 학생이름검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(sms_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'sms_list': page_obj, 'page': page, 'name': name}
    return render(request, 'studyroom/sms_list.html', context)

@login_required(login_url='common:login')
def sms_send(request):

    account_list = Account.objects.order_by('id')

    context = {'account_list': account_list}
    return render(request,'studyroom/sms_send.html', context)

def get_signature(request_type, param, timestamp):
    # naver cloud platform SMS API
    hash_str = "{} {}\n{}\n{}".format(request_type, sms_uri+param, timestamp, acc_key_id)
    digest = hmac.new(acc_sec_key, msg=hash_str.encode('utf-8'), digestmod=hashlib.sha256).digest()
    d_hash = base64.b64encode(digest).decode()
    return d_hash

def get_request(request_type, key, value, data=''):
    # 파라미터가 있을 경우 url 구하기
    param_str =''

    timestamp = str(int(time.time() * 1000))

    if key =='messageId':
        messageId = '/' + value
        response = requests.get(
            sms_url + messageId,
            headers={"Content-Type": "application/json; charset=utf-8",
                     "x-ncp-apigw-timestamp": timestamp,
                     "x-ncp-iam-access-key": acc_key_id,
                     "x-ncp-apigw-signature-v2": get_signature(request_type, messageId, timestamp)
                     }
        )
    elif key =='requestId':
        requestId = '?' + 'requestId' + '=' + value
        response = requests.get(
            sms_url + requestId,
            headers={"Content-Type": "application/json; charset=utf-8",
                     "x-ncp-apigw-timestamp": timestamp,
                     "x-ncp-iam-access-key": acc_key_id,
                     "x-ncp-apigw-signature-v2": get_signature(request_type, requestId, timestamp)
                     }
        )
    else:
        response = requests.post(
            sms_url, data=data,
            headers={"Content-Type": "application/json; charset=utf-8",
                     "x-ncp-apigw-timestamp": timestamp,
                     "x-ncp-iam-access-key": acc_key_id,
                     "x-ncp-apigw-signature-v2": get_signature(request_type, '', timestamp)
                     }
        )

    print('=== request : ', response.url, param_str)
    print('=== response.status_code : ', response.status_code)
    print('=== response.txt : ', response.text)

    return {'status_code':response.status_code, 'data':json.loads(response.text)}

def get_messageId(requestId):
    # sms 발송 요청 조회
    timestamp = str(int(time.time() * 1000))
    request_type = 'GET'
    response = requests.get(
        sms_url, params={'requestId': requestId},
        headers={"x-ncp-apigw-timestamp": timestamp,
                 "x-ncp-iam-access-key": acc_key_id,
                 "x-ncp-apigw-signature-v2": get_signature(request_type, timestamp)
                 }
    )
    print('=== request : ', response.url)
    print('=== response.status_code : ', response.status_code)
    data = json.loads(response.text)
    print('=== response.txt : ', response.text)


@login_required(login_url='common:login')
def send_sms(request):

    content = request.POST.getlist('content')[0]
    if len(content) <= 80:
        smstype = 'SMS'
    else:
        smstype = 'LMS'

    account_id_list = request.POST.getlist('account_id')

    # 선택된 전화번호 갯수가 없으면 원래 페이지 Return
    if len(account_id_list) == 0:
        account_list = Account.objects.order_by('id')

        context = {'account_list': account_list}
        return render(request, 'studyroom/sms_send.html', context)

    for account_id in account_id_list:
        account = Account.objects.get(pk=account_id)
        sms = Sms()
        sms.content = content
        sms.smstype = smstype
        sms.account = account
        sms.to = account.sms_phone_num
        to_no = sms.to
        msg_data = {
            'type': sms.smstype,
            'countryCode': '82',
            'from': "{}".format(from_no),
            'contentType': 'COMM',
            'content': "{}".format(sms.content),
            'messages': [{'to': "{}".format(to_no)}]
        }
        data = json.dumps(msg_data)

        # SMS 발송 요청
        res = get_request('POST','','', data)
        print("=== sms 발송요청 응답 :", res['status_code'], res['data'])
        # SMS 발송 요청 응답이 오류인 경우
        if res['status_code'] != 202:
            errorCode = res['data']['error']['errorCode']
            message = res['data']['error']['message']
            details = res['data']['error']['details']
            context = {'account':account, 'errorCode':errorCode, 'message':message, 'details':details}
            return render(request, 'studyroom/sms_error.html', context)
        # SMS 발송 요청 응답이 오류인 경우
        else:
            # sms 발송 후 결과 db에 저장
            sms.statusCode = res['data']['statusCode']
            sms.statusName = res['data']['statusName']
            requestId = res['data']['requestId']
            sms.requestId = requestId
            sms.requestTime = res['data']['requestTime']
            sms.create_date = timezone.now()
            sms.save()

        # SMS 발송 요청 조회(messgeId 받기)
        res = get_request('GET', 'requestId', requestId, '')
        print("=== sms 발송요청 조회 응답 :", res['status_code'], res['data'])

        # sms 발송 요청조회 응답 db에 저장
        sms = Sms.objects.get(requestId=requestId)
        sms.statusCode = res['data']['statusCode']
        sms.statusName = res['data']['statusName']

        if sms.statusName == 'processing':
            time.sleep(5)
            res = get_request('GET', 'requestId', requestId, '')
            print("=== sms 발송요청 조회(재요청) 응답 :", res['status_code'], res['data'])
            sms.statusCode = res['data']['statusCode']
            sms.statusName = res['data']['statusName']

        messageId = res['data']['messages'][0]['messageId']
        print("===== messageId :", messageId)
        sms.messageId = messageId
        sms.save()

        if messageId:
            # sms 발송 결과 조회
            res = get_request('GET', 'messageId', messageId, '')
            print("=== sms 발송 결과조회 응답 :", res['status_code'], res['data'])

            # sms 발송 결과조회 응답 db에 저장
            sms = Sms.objects.get(requestId=requestId)
            sms.statusCode = res['data']['statusCode']
            sms.statusName = res['data']['statusName']
            sms.messageStatus = res['data']['messages'][0]['status']

            if sms.messageStatus != 'COMPLETED':
                time.sleep(5)
                res = get_request('GET', 'messageId', messageId, '')
                print("=== sms 발송 결과조회(재요청) 응답 :", res['status_code'], res['data'])
                sms.messageStatus = res['data']['messages'][0]['status']
            sms.save()
    
    # sms 발송 후 sms 발송이력 화면으로 돌아가기
    sms_list = Sms.objects.order_by('-requestTime')

    paginator = Paginator(sms_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(1)

    context = {'sms_list': page_obj, 'page': 1, 'name': ''}
    return render(request, 'studyroom/sms_list.html', context)
