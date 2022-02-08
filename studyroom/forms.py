from django import forms
from studyroom.models import Student, Account


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
        fields = ['student', 'sub_student_id', 'brother_dc_yn', 'payer', 'payer_phone_num', 'recommend_dc_start', 'recommend_dc_end' ]
        # AccountForm에서 사용할 Account 모델의 속성

        labels = {
            'student': '학생',
            'sub_student_id': '형제학생id',
            'brother_dc_yn': '형제할인 여부',
            'payer': '납부자',
            'payer_phone_num': '납부자 폰번호',
            'recommend_dc_start' : '추천할인 시작월',
            'recommend_dc_end': '추천할인 종료월',
        }