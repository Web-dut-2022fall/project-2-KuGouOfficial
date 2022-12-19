import django
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

import auctions
from .models import User, Item, WatchList, Comment


def index(request):
    items = []
    content = {'title': 'Active Listings', 'items': items}
    for each in Item.objects.all():
        items.append({})
        items[-1]['title'] = each.title
        items[-1]['cur_bid'] = each.cur_bid
        items[-1]['description'] = each.description
        items[-1]['item_type'] = each.item_type
        items[-1]['base_bid'] = each.base_bid
        items[-1]['img'] = each.img
        items[-1]['create_date'] = each.create_date
        items[-1]['mod_date'] = each.mod_date

    return render(request, "auctions/index.html", content)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if req.method == 'GET':
        return render(req, 'auctions/create_list.html')
    else:
        content = {}
        itemBase_bid = None
        itemType = req.POST.get('type').strip()
        itemTitle = req.POST.get('title').strip()
        try:
            itemBase_bid = float(req.POST.get('price').strip())
            if itemBase_bid <= 0:
                raise ValueError
        except ValueError:
            print('Price not valid!')
            content['error2'] = 'Price not valid!'
        itemDescription = req.POST.get('description').strip()
        pic = req.FILES.get("pic", None)
        if pic is None:
            content['error4'] = 'No picture uploaded'

        if itemType == '':
            print('Type Blank Error')
            content['error3'] = 'Type is Blank'
        if itemTitle == '':
            print('Title Blank Error')
            content['error1'] = 'Title is Blank'
        if len(itemDescription) < 10:
            print('Description too short')
            content['error5'] = 'Description less than 10 character'

        content['v1'] = itemTitle
        content['v2'] = itemBase_bid
        content['v3'] = itemType
        content['v4'] = itemDescription

        if len(content) == 4:
            try:
                Item(item_type=itemType, title=itemTitle, img=pic.name, base_bid=itemBase_bid,
                     cur_bid=itemBase_bid, description=itemDescription, owner=req.user.username).save()
                with open("./auctions/static/imgs/%s" % pic.name, 'wb+') as f:
                    for chunk in pic.chunks():
                        f.write(chunk)
                content['hint1'] = 'Create success!'
                print('Create success!')
            except django.db.utils.OperationalError:
                content['error0'] = 'Error, Database is locked!'
            # except django.db.utils.IntegrityError:
            #     content['error0'] = 'Error, Title not unique!'
        return render(req, 'auctions/create_list.html', content)


def listing_page(req, title):
    context = {}
    item_id = None
    item = None
    won = False
    try:
        item = Item.objects.get(title=title)
        item_id = item.item_id
        WatchList.objects.get(owner=req.user.username, item_id=item_id)
        context['has'] = 'true'
    except auctions.models.WatchList.DoesNotExist:
        context['has'] = ''
    except auctions.models.Item.DoesNotExist:
        return HttpResponse('404 \nauctions.models.Item.DoesNotExist')
    context['own'] = 'true' if item.owner == req.user.username else ''
    if item.winner != None:
        won = True
        if item.winner == req.user.username:
            context['hint1'] = 'You have won the auctions'
        else:
            context['hint1'] = 'Come a little late'

    context['title'] = item.title
    context['owner'] = item.owner
    context['item_type'] = item.item_type
    context['description'] = item.description
    context['cur_bid'] = item.cur_bid
    context['img'] = item.img
    context['create_date'] = item.create_date
    context['mod_date'] = item.mod_date
    context['coms'] = []
    for each in Comment.objects.filter(item_id=item_id):
        context['coms'].append({})
        context['coms'][-1]['user'] = each.user
        context['coms'][-1]['com'] = each.com
        context['coms'][-1]['create_date'] = each.create_date

    # 添加到watchlist
    if req.method == 'POST' and not won:
        if req.POST.get('add') == 'true':
            WatchList(item_id=item_id, owner=req.user.username).save()
            context['has'] = 'true'
        elif req.POST.get('add') == 'false':
            WatchList.objects.get(item_id=item_id).delete()
            context['has'] = ''
        if req.POST.get('bid') is not None:
            try:
                bid = float(req.POST.get('bid').strip())
                if bid <= item.cur_bid:
                    context['error1'] = 'Bid should be higher than current bid'
                else:
                    item.cur_bid = bid
                    item.save()
                    context['hint1'] = 'Success!'
                    context['cur_bid'] = bid
            except ValueError:
                context['error1'] = 'Bid not valid'
        # 添加评论
        if req.POST.get('comment') is not None:
            comment = Comment(item_id=item_id, user=req.user.username, com=req.POST.get('comment'))
            comment.save()
            context['coms'].append({'user': comment.user, 'com': comment.com, 'create_date': comment.create_date})

    return render(req, 'auctions/listing_page.html', context)


def watchlist(req):
    if req.user.username is None:
        return HttpResponseRedirect(reverse('login'))
    items = []
    content = {'title': 'Watch List', 'items': items}
    for pair in WatchList.objects.filter(owner=req.user.username):
        each = Item.objects.get(item_id=pair.item_id)
        items.append({})
        items[-1]['title'] = each.title
        items[-1]['cur_bid'] = each.cur_bid
        items[-1]['description'] = each.description
        items[-1]['item_type'] = each.item_type
        items[-1]['base_bid'] = each.base_bid
        items[-1]['img'] = each.img
        items[-1]['create_date'] = each.create_date
        items[-1]['mod_date'] = each.mod_date
    return render(req, 'auctions/index.html', context=content)


def categories(req):
    category = req.GET.get('category')
    items = []
    content = {'items': items, 'opts': []}
    for each in Item.objects.all():
        if each.item_type not in content['opts']:
            content['opts'].append(each.item_type)
    print(category)
    for pair in Item.objects.filter(item_type=category) if \
            category != '' and category is not None else Item.objects.all():
        each = Item.objects.get(item_id=pair.item_id)
        items.append({})
        items[-1]['title'] = each.title
        items[-1]['cur_bid'] = each.cur_bid
        items[-1]['description'] = each.description
        items[-1]['item_type'] = each.item_type
        items[-1]['base_bid'] = each.base_bid
        items[-1]['img'] = each.img
        items[-1]['create_date'] = each.create_date
        items[-1]['mod_date'] = each.mod_date
    return render(req, 'auctions/categories.html', context=content)
