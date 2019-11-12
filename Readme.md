# Day5

- Django 시작하기

  - 프로젝트 만들기
    - 프로젝트 vs 어플리케이션(app)
    - MVC -> MVT
    - Model View Controller -> Model View(Controller) Template(View)
    - Django
      - 시작하기
      - `django-admin startproject projectname`
      - `cd myproject`
      - `python manage.py startapp appname`
      - django에서 app단위는 하나의 모델에 대한 모든 내용이 담겨있다. 예를 들어 게시판을 만든다고 하면, Post라는 app을 만들어서 그 안에서 모든 내용을 처리한다.

- 로또번호 생성기 + 번호 체크 + 번호를 몇개나 뽑을지

  - 메인 페이지(번호를 몇개 뽑을지, 생성버튼) -> '/lotto'
  - 결과 페이지(랜덤으로 뽑힌 번호, 뽑힌 번호가 가장 최근 당첨번호와 몇개가 맞았는지) -> '/lotto/winning'

  - app만드는 순서
    - `python manage.py startapp appname`
    - `settings.py`의 `INSTALLED_APPS`에 만든 app을 추가
    - 만든 app 폴더에 가서 `views.py`파일에 함수 등록
    - 해당 함수의 결과로 return할 template 선언
    - 위 template 파일 만들기
    - `urls.py`에 등록된 함수 연결

  - day5/settings.py

  - ```python
    INSTALLED_APPS = [
        'lotto', 
        ...
    ]
    ```

  - day5/urls.py

  - ```python
    from lotto import views as lotto_views
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('lotto/', lotto_views.lotto),
        path('lotto/winning', lotto_views.winning),
    ]
    ```

  - lotto/views.py

  - ```python
    from django.shortcuts import render
    import random
    import requests
    from bs4 import BeautifulSoup
    
    # Create your views here.
    def lotto(request):
        return render(request, 'lotto.html')
    def winning(request):
        # 1. 1~45까지의 숫자중에 n개의 숫자를 랜덤추출
        # 1-1. 1 ~ 45까지의 번호를 가진 배열을 만든다.
        num_list = list(range(1,46))
        num_count = request.GET['count']        
        # 1-2. 해당 배열에서 count만큼의 숫자를 샘플링
        result_list = random.sample(num_list, int(num_count))
        result_list.sort()
        # 2. 로또 당첨번호 공개 사이트로 가서 지난주 당첨번호 가져오기
        # - 몇회차인지, 언제 당첨번호인지, 1등 당첨금이 얼마인지
        url = 'https://dhlottery.co.kr/gameResult.do?method=byWin'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')
        winning_numbers = html.select('div.win span')
        winning_count = 0
        winning_list = []
        for number in winning_numbers:
            # result list 변수에 number가 포함되어 있나요?
            winning_list.append(int(number.text))
            if int(number.text) in result_list:
                winning_count += 1
        
        return render(request, 'winning.html', {'result': result_list,
                                                'winning_list': winning_list,
                                                'winning_count': winning_count})
    
    ```

- ascii art

  - 텍스트를 입력하고 폰트를 설정해서 예쁜 아스키 아트를 만들어보자

  - [아스키 아트 페이지](http://artii.herokuapp.com/)

  - `python mange.py startapp ascii`

  - settings.py

  - ```python
    INSTALLED_APPS = [
        'lotto', 
        'ascii',
        ...
    ]
    ```

  - urls.py

  - ```python
    from lotto import views as lotto_views
    from ascii import views as ascii_views
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('lotto/', lotto_views.lotto),
        path('lotto/winning', lotto_views.winning),
        path('ascii/', ascii_views.ascii),
        path('ascii/result', ascii_views.result),
        ...
    ]
    ```

  - views.py

  - ```python
    from django.shortcuts import render
    import requests
    
    # Create your views here.
    def ascii(request):
        # 입력하고자 하는 text를 받아야함
        # artii에서 제공하는 폰트 중 선택
        url = 'http://artii.herokuapp.com/fonts_list'
        response = requests.get(url)
        fonts_list = response.text.split('\n')
        context = {
            'fonts': fonts_list
        }
        return render(request, 'ascii.html', context)
    def result(request):
        # ascii에서 입력한 텍스트와 폰트를
        font = request.GET['font']
        text = request.GET['text']
        # artii에 보내서 결과값을 받아서 보여줌
        url = f'http://artii.herokuapp.com/make?font={font}&text={text}'
        response = requests.get(url)
        context = {
            'result': response.text
        }
        return render(request, 'result.html', context)
    ```

- fake opgg

  - 우리가 입력한 소환사 명에 따라 실제 op.gg에 요청을 보내 크롤링 해온 데이터로 전적을 검색한다.

  - `python manage.py startapp opgg`

  - settings.py

  - ```python
    INSTALLED_APPS = [
        'lotto', 
        'ascii',
        'opgg',
        ...
    ]
    ```

  - urls.py

  - ```python
    from lotto import views as lotto_views
    from ascii import views as ascii_views
    from opgg import views as opgg_views
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('lotto/', lotto_views.lotto),
        path('lotto/winning', lotto_views.winning),
        path('ascii/', ascii_views.ascii),
        path('ascii/result', ascii_views.result),
        path('opgg/', opgg_views.opgg),
        path('opgg/result', opgg_views.result),
    ]
    
    ```

  - views.py

  - ```python
    from django.shortcuts import render
    from bs4 import BeautifulSoup
    import requests
    
    # Create your views here.
    def opgg(request):
        # 소환사명을 입력할 입력창을 만든다.
        return render(request, 'opgg.html')
    
    def result(request):
        # 실제 op.gg를 크롤링해서 입력된 소환사에 대한
        name = request.GET['nickname']
        url = f'https://www.op.gg/summoner/userName={name}'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')
        # 1차적인 예외처리
        if html.select_one('span.WinLose .wins') is None:
            result = {
                'msg': '소환사가 없거나 언랭입니다.'
            }
        else:
            result = {
                'name': name,
                'win': html.select_one('span.WinLose .wins').text,
                'lose': html.select_one('span.WinLose .losses').text,
                'ratio': html.select_one('span.WinLose .winratio').text
            }
    
        # 전적 정보를 가져온다.
        return render(request, 'ratio.html', result)
    ```

    

