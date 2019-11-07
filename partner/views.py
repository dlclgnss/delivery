from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout

from client.views import common_login,common_signup
from .forms import PartnerForm,MenuForm
from .models import Partner,Menu


URL_LOGIN = '/partner/login/'
def partner_group_check(user):
    return 'partner' in [ group.name for group in user.groups.all()]


#기본페이지 (로그인한 업체정보를 보여준다.) 8000:/partner 부분
def index(request):
    if request.method == 'POST':
        partner_form = PartnerForm(request.POST)
        if partner_form.is_valid():
            partner=partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("index")
    else:
        partner_form = PartnerForm()

    ctx={
        'partner_form':partner_form
        }
    return render(request,'index.html',ctx)



#업체정보 수정 (정보를 가져오는 인스턴스 값을 추가하면된다.)
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def edit_info(request):
    if request.method == 'POST':
        partner_form = PartnerForm(request.POST,instance=request.user.partner)
        if partner_form.is_valid():
            partner=partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("index")
    else:
        partner_form = PartnerForm(instance=request.user.partner)

    ctx={
        'partner_form':partner_form
        }

    return render(request,'edit_info.html',ctx)


# partner 로그인 하는 페이지(client로그인과 반복하므로 common_login함수를 인용)
def signin(request):
    ctx={}
    return common_login(request,ctx,"partner")



# 로그아웃 하는 페이지
def signout(request):
    logout(request)
    return redirect("index")


# partner 회원가입 하는 페이지 (client 회원가입과 반복하므로 common_signup함수를 인용)
def signup(request):
    ctx={}
    return common_signup(request,ctx,"partner")


#메뉴페이지 ,카테고리
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def menu(request):
    category = request.GET.get("category")
    # menu_list = Menu.objects.filter(partner = request.user.partner)
    if not category:
        menu_list = Menu.objects.filter(partner = request.user.partner)
    elif category:
        menu_list = Menu.objects.filter(category = category)


    # 카테고리 리스트를 표시
    category_list = set([
    (menu.category,menu.get_category_display()) #튜플모양으로 전달, get_category_displays는 'dv','ps'를 뜻함
    for menu in menu_list
    ])

    ctx={
    'menu_list':menu_list,
    'category_list':category_list,
    }
    return render(request,'menu.html',ctx)



#메뉴 추가페이지
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def menu_add(request):
    if request.method == 'POST':
        menu_form = MenuForm(request.POST,request.FILES)
        if menu_form.is_valid():
            menu=menu_form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("menu")
    else:
        menu_form = MenuForm()

    ctx={
        'menu_form':menu_form
        }
    return render(request,'menuadd.html',ctx)



#메뉴 상세페이지
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def menu_detail(request, menu_id):
    menu=Menu.objects.get(id = menu_id)
    ctx={'menu': menu}
    return render(request,'menu_detail.html',ctx)


#메뉴 상세페이지에서 수정하기
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def menu_edit(request, menu_id):
    # menu=Menu.objects.get(id = menu_id)
    menu=get_object_or_404(Menu,id = menu_id)
    if request.method == 'POST':
        menu_form = MenuForm(request.POST,request.FILES, instance=menu)
        if menu_form.is_valid():
            menu=menu_form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("menu")
    else:
        menu_form = MenuForm(instance=menu)

    ctx={
        'menu_form':menu_form,
        'replace':'수정',
        }

    return render(request,'menuadd.html',ctx)


#메뉴목록하나 삭제하기
@login_required(login_url= URL_LOGIN )
@user_passes_test(partner_group_check, login_url= URL_LOGIN )
def menu_delete(request, menu_id):
    menu=get_object_or_404(Menu,id = menu_id)
    menu.delete()

    return redirect('menu')


# 고객이 주문한것 확인하는 페이지
def order(request):
    ctx={}
    return render(request,'ordermenu_for_partner.html',ctx)
