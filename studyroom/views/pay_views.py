{% extends 'base.html' %}
{% load studyroom_filter %}
{% block content %}

<div class="container my-3">
    <div>
        <h1>
            <span class="badge badge-info">수납 목록</span>
        </h1>
    </div>
    <div class="row">
        <div class="col-xs-2">
            <button class="btn " type="button" >이름</button>
        </div>
        <div class="col-xs-2">
            <input id="input_search" type="text" class="form-control name" value="{{ name|default_if_none:'' }}">
        </div>
        <div class="col-xs-2">
            <button class="btn btn-outline-secondary" type="button" id="btn_search">찾기</button>
        </div>
        <div class="col-xs-2">
        </div>        
    </div>
    <table class="table">
        <thead>
        <tr class="text-center thead-light">
            <th>수납일</th>
            <th>구분</th>
            <th>납부자</th>
            <th>학생</th>
            <th>수납금액</th>
            <th>상태</th>
        </tr>
        </thead>
        <tbody>
        {% if pay_list %}
        {% for pay in pay_list %}
        <tr class="text-center">
            <td>{{ pay.pay_date }}</td>
            <td>{{ pay.pay_type }}</td>
            <td>{{ pay.payer }}</td>
            <td>{{ pay.account.student.name }}</td>
            <td>{{ pay.pay_amt }}</td>
            <td>{{ pay.pay_status }}</td>
        </tr>
        {% endfor %}
        {% else %}
        <tr>
            <td colspan="3">수납 내역이 없습니다.</td>
        </tr>
        {% endif %}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        {% if pay_list.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page={{ pay_list.previous_page_number }}">이전</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">이전</a>
        </li>
        {% endif %}
        <!-- 페이지리스트 -->
        {% for page_number in pay_list.paginator.page_range %}
        {% if page_number >= pay_list.number|add:-5 and page_number <= pay_list.number|add:5 %}
            {% if page_number == pay_list.number %}
            <li class="page-item active" aria-current="page">
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
            {% else %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
            {% endif %}
        {% endif %}
        {% endfor %}
        <!-- 다음페이지 -->
        {% if pay_list.has_next %}
        <li class="page-item">
            <a class="page-link" href="?page={{ pay_list.next_page_number }}">다음</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">다음</a>
        </li>
        {% endif %}
    </ul>
    <!-- 페이징처리 끝 -->

</div>
<form id="searchForm" method="get" action="{% url 'studyroom:pay_list' %}">
    <input type="hidden" id="name" name="name" value="{{ name|default_if_none:'' }}">
    <input type="hidden" id="page" name="page" value="{{ page }}">
</form>
{% endblock %}
{% block script %}
<script type='text/javascript'>
$(document).ready(function(){
    $(".page-link").on('click', function() {
        $("#page").val($(this).data("page"));
        $("#searchForm").submit();
    });

    $("#btn_search").on('click', function() {
        $("#name").val($(".name").val());
        $("#page").val(1);  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
        $("#searchForm").submit();
    });
    $("#input_search").keydown(function(key) {
        if (key.keyCode == 13) {
            $("#name").val($(".name").val());
            $("#page").val(1);  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
            $("#searchForm").submit();
    }});
});
</script>
{% endblock %}
