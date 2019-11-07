from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from partner.models import Partner,Menu #다른쪽 모델을 가져올때
from .models import Client,Order,OrderItem


# Create your views here.
def index(request):
    partner_list=Partner.objects.all()
    ctx={
    'partner_list':partner_list
    }
    return render(request,'main.html',ctx)


#반복되는 login을 하나로 통일
def common_login(request,ctx,group):
    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: # 유저가 존재 한다면
            if group not in [ group.name for group in user.groups.all()]: # 클라이언트 인지 파트너인지
                ctx.update({"error":'접근권한이 없습니다.'})
            else:
                login(request, user)
                #url접근, 로그인화면 에서 로그인 하면 바로 그페이지로 이동
                #http://127.0.0.1:8000/partner/login/?next=/partner/menu/add/
                next_value = request.GET.get("next")
                if next_value:
                    return redirect(next_value)
                else:
                    if group == 'partner': #그룹이 partner이면 업체페이지로 / 아니면 고객페이지로
                        return redirect("index")
                    else:
                        return redirect("client:main")
        else:
            ctx.update({"error":'아이디 및 비밀번호가 잘못되었습니다.'})
    return render(request,'login.html',ctx)



# client 로그인 하는 페이지
def signin(request):
    ctx={
    "is_client":True,
    'replace':'회원 로그인',
    }
    return common_login(request,ctx,"client")

# signup반복되는 부분을 통합
def common_signup(request,ctx,group):
    if request.method == 'POST':
        username =request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #create_user를 이용해서 아이디 이메일 비번을 저장한다.
        user = User.objects.create_user(username,email,password)
        target_group = Group.objects.get(name=group)# 그룹(클라이언트/파트너)의 이름을 가져온다.
        user.groups.add(target_group) # 만든 user에 그룹을 정해준다.

        if group == "client":
            Client.objects.create(user=user, name=username)

        return redirect('client:main')

    return render(request,'signup.html',ctx)



# client 회원가입 하는 페이지
def signup(request):
    ctx = {
    "is_client":True,
    'replace': '일반회원가입'
     }
    return common_signup(request,ctx,"client")



# 메뉴에서 주문하기
def order(request,partner_id):
    partner = Partner.objects.get(id=partner_id)
    menu_list = Menu.objects.filter(partner=partner)

    if request.method == "POST":
        order = Order.objects.create(
            client = request.user.client,
            address = "text",
        )

        for menu in menu_list:
            menu_count =request.POST.get(str(menu.id))
            menu_count = int(menu_count)
            if menu_count > 0:
                item = OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    count = menu_count,
                )
                # order.items.add(item)

        return redirect('client:main')

    ctx={
    'menu_list':menu_list,
    'partner':partner
    }
    return render(request,'ordermenu.html',ctx)
