from django import forms
from studyroom.models import Student, Account, Sugang, Absence


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student  # 사용할 모델
        fields = ['name', 'grade', 'brother']  # StudentForm에서 사용할 Student 모델의 속성

        labels = {
            'name': '학생이름',
            'grade': '학년',
            'brother': '형제',
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account  # 사용할 모델
        fields = ['student', 'payer', 'payer_phone_num', 'sms_phone_num', 'recommend_dc_start', 'recommend_dc_end' ]
        # AccountForm에서 사용할 Account 모델의 속성

        labels = {
            'student': '학생',
            'payer': '납부자',
            'payer_phone_num': '납부자 폰번호',
            'sms_phone_num': 'SMS 폰번호',
            'recommend_dc_start' : '추천할인 시작월',
            'recommend_dc_end': '추천할인 종료월',
        }


class SugangForm(forms.ModelForm):
    class Meta:
        model = Sugang  # 사용할 모델
        fields = ['student', 'class_id', 'weekday', 'time', 'start_mt', 'end_mt']
        # SugangForm에서 사용할 Sugang 모델의 속성

        labels = {
            'student': '학생',
            'class_id': '강사',
            'weekday': '요일',
            'time': '시간',
            'start_mt': '시작월',
            'end_mt': '종료월',
        }


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence  # 사용할 모델
        fields = [ 'absence_mt', 'absence_days', 'absence_detail']
        # SugangForm에서 사용할 Sugang 모델의 속성

        labels = {
            'absence_mt': '결석월',
            'absence_days': '결석일수',
            'absence_detail': '결석사유',
        }
