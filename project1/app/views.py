from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.

def project1_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        data = authenticate(username=uname, password=password)
        if data:
            login(req, data)
            if data.is_superuser:
               req.session['shop'] = uname      
               return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(shop_home)
        
        

        else:
            messages.warning(req, 'Invalid username or password')
            return redirect(project1_login)
    else:
       return render(req, 'login.html')


def project1_shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(project1_login)


def shop_home(req):
    data = Product.objects.all()
    if 'shop' in req.session:
        return render(req, 'shop/home.html', {'Product': data})
    else:
        return redirect(project1_login)


def add_product(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            pid = req.POST['pid']
            name = req.POST['name']
            discrip = req.POST['descrip']
            price = req.POST['price']
            offer_price = req.POST['off_price']
            stock = req.POST['stock']
            file = req.FILES['img']

            data = Product.objects.create(
                pid=pid, name=name, dis=discrip, price=price,
                offer_price=offer_price, stock=stock, img=file
            )
            data.save()
            return redirect(shop_home)
        else:
            return render(req, 'shop/addproduct.html')
    else:
        return redirect(project1_login)


def edit_product(req, pid):
    if 'shop' in req.session:
        if req.method == 'POST':
            name = req.POST['name']
            discrip = req.POST['descrip']
            price = req.POST['price']
            offer_price = req.POST['off_price']
            stock = req.POST['stock']
            file = req.FILES.get('img')  
            if file:
                Product.objects.filter(pk=pid).update(pid=id,name=name,descrip=discrip,price=price,off_price=offer_price,stock=stock,img=file)
                data=Product.  objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=pid,name=name,descrip=discrip,price=price,offer_price=offer_price,stock=stock,img=file)
            return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit_product.html',{'data':data})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)


#-------------------------user----------------------------
def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,'invalid username or password')
            return redirect(register)   
        return redirect(project1_login) 
    else:
        return render(req,'user/register.html')    
    
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/user_home.html',{'Products':data})
    else:
        return redirect(project1_login)

def pro_dtl(req,pid):
    if 'user' in req.session:
        try:
            data=Product.objects.get(pk=pid)
        except:
            messages.warning(req,'sorry the details are not avaliable')
            return redirect(pro_dtl)  
         
        return render(req,'user/product_dtl.html',{'Products':data})
    else:
        return redirect(user_home)
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/user_home.html',{'products':data})
    else:
        return redirect(project1_login)
    
def view_product(req,pid):
        data = Product.objects.get(pk=pid)
        return render(req,'user/view_product.html',{'product':data})
           
def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
      data=Cart.objects.create(product=product,user=user,qty=1)
      data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})   

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)


def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(booking)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(booking)

def about(req):
    return render(req,'user/about.html')       

def booking(req):
    user=User.objetcs.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/booking.html',{'booking':buy})

def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/view_bookings.html',{'view_bookings':buy})