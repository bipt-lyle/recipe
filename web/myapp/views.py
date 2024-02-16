from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import filterrecipe, myrecipe,therecipes,flavor,filterrecipe2,user,Post,coments,det
from django.db.models import Q
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
# Create your views here.
def indexfood(request):
    oc = flavor.objects
    oc1 = flavor.objects.count()
    ht = oc.all()
    if oc1 >0:
        ht.delete()
            
    saveflavor()
    
    return render(request,"myapp/users/page1.html")
    

def indexmarket(request):
    return render(request,"myapp/users/page2.html")

def indexusers(request):
    return render(request,"myapp/users/signup.html")
    
def indexusers2(request):
    return render(request,"myapp/users/signup2.html")

def insertusers(request):
    try:
        if int(request.POST['Password']) == int(request.POST["Confirm password"]):
            ob = user()
            ob.Uname = request.POST['Username']
            #将当前员工信息的密码做md5处理
            import hashlib,random
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = request.POST['Password']+str(n) #从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8')) #将要产生md5的子串放进去
            ob.password_hash = md5.hexdigest() #获取md5值
            ob.password_salt = n
            ob.status = 1
            ob.signdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            context = {'info1':"注册"}
        else:
            return HttpResponse('验证密码与输入密码不同！')
    except Exception as err:
        print(err)
        context = {'info':"添加失败！"}
        return render(request,"myapp/users/info.html",context)
    return render(request,"myapp/users/info1.html",context)

def dologin(request):
    try:        
        #根据登录账号获取登录者信息
        userd = user.objects.get(Uname=request.POST['Username'])
        #判断当前用户是否是管理员
        if userd.status == 1:
            #判断登录密码是否相同
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass']+userd.password_salt #从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8')) #将要产生md5的子串放进去
            if userd.password_hash == md5.hexdigest(): #获取md5值
                print('登录成功')
                #将当前登录成功的用户信息以adminuser为key写入到session中
                request.session['adminuser'] = userd.toDict()
                #重定向到后台管理首页                
                # return redirect(reverse("indexfood"))
                context = {"info1":"登录"}
                return render(request,"myapp/users/page1.html",context)
            else:
                context = {"info":"登录密码错误！"}
        else:
            context = {"info":"无效的登录账号！"}
    except Exception as err:
        print(err)
        context = {"info":"登录账号不存在"}
    return render(request,"myapp/users/info.html",context)


def recipe(request):
    try:
        ob = myrecipe()
        oc = myrecipe.objects
        ob1 = myrecipe.objects.count()
        oa = filterrecipe()
        od = filterrecipe.objects
        ht = oc.all()
        fd = od.all()
        if ob1 >0:
            ht.delete()
            fd.delete()
        #从表单中获取要添加的信息并封装到ob对象中
        st = request.POST.getlist('likes')
        i=0
        for i in range(len(st)):
            ob.Ingredients = st[i]
            ob.pk = None
            ob.save() #执行保存    
        # ob.Ingredients = request.POST.getlist('likes')
        # ob.save()
        # print(ob.Ingredients)
        rlist = myrecipe.objects.all()
        #查询菜谱zhuliao字段
        # rw = []
        # for u in rlist:
        #     if rw != '':
        #         print(u.Ingredients)
        #         rw.append(u.Ingredients)
        context = {}
        
        for kw in range(len(st)):
            nlist = therecipes.objects.filter(Ingre__contains = st[kw])
            for re in nlist:
                oa.Dname =  re.Dname
                oa.flavor = re.flavor
                oa.gongyi = re.gongyi
                oa.zuofa = re.zuofa
                oa.Ingre = re.Ingre
                oa.pk = None
                oa.save()
            # context.update({"kw%s"%(kw):nlist})
        hlist = filterrecipe.objects.all()
        print(987)
        print(st)
        context.update({"filterrecipe":hlist})
        context.update({"recipelist":rlist})
        oblist = flavor.objects.all()
        context.update({"obflavor":oblist})
        print(context)
        if len(st)>0:
            return render(request,"myapp/users/recipe.html",context) #加载模板
        else:
            return HttpResponse("no ingredients！")
    except:
        return HttpResponse("no ingredients！")
    
def delIngredients(request,uid=0):    
    try:
        context = {}
        oa = filterrecipe()
        od = filterrecipe.objects
        fd = od.all()
        fd.delete()
        ob = myrecipe.objects.get(id=uid) #获取要删除的数据
        ob.delete() #执行删除操作
        rlist = myrecipe.objects.all()
        st = []
        for u in rlist:
            if st != '':
                print(u.Ingredients)
                st.append(u.Ingredients)
        context.update({"recipelist":rlist})
        for kw in range(len(st)):
            nlist = therecipes.objects.filter(Ingre__contains = st[kw])
            for re in nlist:
                oa.Dname =  re.Dname
                oa.flavor = re.flavor
                oa.gongyi = re.gongyi
                oa.zuofa = re.zuofa
                oa.Ingre = re.Ingre
                oa.pk = None
                oa.save()
            # context.update({"kw%s"%(kw):nlist})
        hlist = filterrecipe.objects.all()
        context.update({"filterrecipe":hlist})
        oblist = flavor.objects.all()
        context.update({"obflavor":oblist})
        # context = {"info":"successfully deleted！"}
    except:
        context = {"info":"failed to delete！"}
    return render(request,"myapp/users/recipe.html",context)

def add(request):
    return render(request,"myapp/users/add.html")

def add2(request):
    ob = myrecipe()
    oa = filterrecipe()
    #从表单中获取要添加的信息并封装到ob对象中
    st = request.POST.getlist('likes')
    i=0
    for i in range(len(st)):
        ob.Ingredients = st[i]
        ob.pk = None
        ob.save() #执行保存    
    # ob.Ingredients = request.POST.getlist('likes')
    # ob.save()
    # print(ob.Ingredients)
    context = {}
    
    for kw in range(len(st)):
        nlist = therecipes.objects.filter(Ingre__contains = st[kw])
        for re in nlist:
            oa.Dname =  re.Dname
            oa.flavor = re.flavor
            oa.gongyi = re.gongyi
            oa.zuofa = re.zuofa
            oa.Ingre = re.Ingre
            oa.pk = None
            oa.save()
        # context.update({"kw%s"%(kw):nlist})
    hlist = filterrecipe.objects.all()
    context.update({"filterrecipe":hlist})
    rlist = myrecipe.objects.all
    context.update({"recipelist":rlist})
    oblist = flavor.objects.all()
    context.update({"obflavor":oblist})
    if len(st)>0:
        return render(request,"myapp/users/recipe.html",context) #加载模板
    else:
        return HttpResponse("no ingredients！")


def filter(request):
    od = filterrecipe2.objects
    ob1 = filterrecipe2.objects.count()
    fd = od.all()
    if ob1 >0:
        fd.delete()
    st = request.POST.getlist('flavor')
    print(st)
    context = {}
    oa = filterrecipe2()
    if st != []:
        # for i in st:
        #     st[i] = (st[i])[:-1]
        # print(st)
        for kw in range(len(st)):
            rlist = filterrecipe.objects.filter(flavor = st[kw])
            for re in rlist:
                oa.Dname =  re.Dname
                oa.flavor = re.flavor
                oa.gongyi = re.gongyi
                oa.zuofa = re.zuofa
                oa.Ingre = re.Ingre
                oa.pk = None
                oa.save()
        hlist = filterrecipe2.objects.all()
    else:
        hlist = filterrecipe.objects.all()
        
    
    context.update({"filterrecipe":hlist})
    oblist = flavor.objects.all()
    context.update({"obflavor":oblist})
    rlist = myrecipe.objects.all()
    context.update({"recipelist":rlist})
    return render(request,"myapp/users/recipe.html",context)

def saveflavor():
    # 获取所有flavor
    ob = flavor()
    olist = therecipes.objects.values_list("flavor",flat=True).distinct()
    for re in olist:
        ob.flavor = re
        ob.pk = None
        ob.save()


def details(request, uid):
    Postlist = Post.objects.all()
    ls = {}
    ls.update({"Postlist": Postlist})
    st = det.objects.all()
    st.delete()
    oa = det()
    try:
        filter = filterrecipe.objects.get(id=uid)
        f_Dname = filter.Dname

        oa.Dname =  filter.Dname
        oa.flavor = filter.flavor
        oa.gongyi = filter.gongyi
        oa.zuofa = filter.zuofa
        oa.Ingre = filter.Ingre
        oa.pk = None
        oa.save()
    except:
        filter = filterrecipe2.objects.get(id=uid)
        f_Dname = filter.Dname
        oa.Dname =  filter.Dname
        oa.flavor = filter.flavor
        oa.gongyi = filter.gongyi
        oa.zuofa = filter.zuofa
        oa.Ingre = filter.Ingre
        oa.pk = None
        oa.save()
    artc = therecipes.objects.get(Dname=f_Dname)
    if request.method == 'POST':
        name = request.POST.get("username")
        com = request.POST.get("coment")
        # if com == "":
        #     msg = 'there are nothing '
        # else:

        comm = coments(name=name, com=com, To=artc)
        comm.save()
    commls = coments.objects.filter(To=artc.id)

    ls.update(({"comm": commls}))
    try:
        article = filterrecipe.objects.get(id=uid)
    except:
        article = filterrecipe2.objects.get(id=uid)
    ls.update({"article": article})

    return render(request, "myapp/users/details.html", ls)  # 加载模板

def details2(request, uid):
    Postlist = Post.objects.all()
    ls = {}
    ls.update({"Postlist": Postlist})
    
    try:
        filter = filterrecipe.objects.get(id=uid)
        f_Dname = filter.Dname
    except:
        filter = filterrecipe2.objects.get(id=uid)
        f_Dname = filter.Dname
    artc = therecipes.objects.get(Dname=f_Dname)
    if request.method == 'POST':
        name = request.POST.get("username")
        com = request.POST.get("coment")
        # if com == "":
        #     msg = 'there are nothing '
        # else:

        comm = coments(name=name, com=com, To=artc)
        comm.save()
    commls = coments.objects.filter(To=artc.id)

    ls.update(({"comm": commls}))
    try:
        article = filterrecipe.objects.get(id=uid)
    except:
        article = filterrecipe2.objects.get(id=uid)
    ls.update({"article": article})

    return render(request, "myapp/users/details.html", ls)  # 加载模板

def details3(request):
    Postlist = Post.objects.all()
    ls = {}
    ls.update({"Postlist": Postlist})
    

    filter = det.objects.all()
    for re in filter:    
        f_Dname = re.Dname
    
    artc = therecipes.objects.get(Dname=f_Dname)
    if request.method == 'POST':
        name = request.POST.get("username")
        com = request.POST.get("coment")
        # if com == "":
        #     msg = 'there are nothing '
        # else:

        comm = coments(name=name, com=com, To=artc)
        comm.save()
    commls = coments.objects.filter(To=artc.id)

    ls.update(({"comm": commls}))
    article = det.objects.all()
    ls.update({"article": article})

    return render(request, "myapp/users/details.html", ls)  # 加载模板
    
def dologin2(request):
    try:        
        #根据登录账号获取登录者信息
        userd = user.objects.get(Uname=request.POST['Username'])
        #判断当前用户是否是管理员
        if userd.status == 1:
            #判断登录密码是否相同
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass']+userd.password_salt #从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8')) #将要产生md5的子串放进去
            if userd.password_hash == md5.hexdigest(): #获取md5值
                print('登录成功')
                #将当前登录成功的用户信息以adminuser为key写入到session中
                request.session['adminuser'] = userd.toDict()
                #重定向到后台管理首页                
                # return redirect(reverse("indexfood"))
                details3()
            else:
                context = {"info":"登录密码错误！"}
        else:
            context = {"info":"无效的登录账号！"}
    except Exception as err:
        print(err)
        context = {"info":"登录账号不存在"}
    return render(request,"myapp/users/info.html",context)


def recipe2(request):
    try:
        
        rlist = myrecipe.objects.all()
        #查询菜谱zhuliao字段
        # rw = []
        # for u in rlist:
        #     if rw != '':
        #         print(u.Ingredients)
        #         rw.append(u.Ingredients)
        context = {}
        

        hlist = filterrecipe.objects.all()
        
        context.update({"filterrecipe":hlist})
        context.update({"recipelist":rlist})
        oblist = flavor.objects.all()
        context.update({"obflavor":oblist})
        print(context)
        return render(request,"myapp/users/recipe.html",context) #加载模板
    except:
        return HttpResponse("error")

def logout(request):
    if 'adminuser' not in request.session:
        return HttpResponse("you have not logged in")
    else:
        del request.session['adminuser']
        return render(request,"myapp/users/signup.html")

def recipe3(request):
    try:
        ob = myrecipe()
        oc = myrecipe.objects
        ob1 = myrecipe.objects.count()
        oa = filterrecipe()
        od = filterrecipe.objects
        ht = oc.all()
        fd = od.all()
        
       
        # ob.Ingredients = request.POST.getlist('likes')
        # ob.save()
        # print(ob.Ingredients)
        rlist = myrecipe.objects.all()
        #查询菜谱zhuliao字段
        # rw = []
        # for u in rlist:
        #     if rw != '':
        #         print(u.Ingredients)
        #         rw.append(u.Ingredients)
        context = {}

        hlist = filterrecipe.objects.all()
        print(987)
        
        context.update({"filterrecipe":hlist})
        context.update({"recipelist":rlist})
        oblist = flavor.objects.all()
        context.update({"obflavor":oblist})
        print(context)
        
        return render(request,"myapp/users/recipe.html",context) #加载模板
        
    except:
        return HttpResponse("no ingredients！")