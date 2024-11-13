from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from back import model_manager
from back.forms import EditProfileForm, ChangePasswordForm, AskForm
from back.models import PostFile, Subscription, Profile, PostLike, Post


def index(request):
    context = model_manager.pagination(request, 'index')
    context['pop_tags'] = model_manager.get_popular_tags()
    context['pop_users'] = model_manager.get_popular_users()
    return render(request, 'index.html', context)


def hot(request):
    context = model_manager.pagination(request, 'hot')
    context['pop_tags'] = model_manager.get_popular_tags()
    context['pop_users'] = model_manager.get_popular_users()
    return render(request, 'hot.html', context)


def question(request, question_id):
    context = model_manager.this_question(request, question_id)
    form = model_manager.get_answer_form(request)
    context['form'] = form
    context['pop_tags'] = model_manager.get_popular_tags()
    context['pop_users'] = model_manager.get_popular_users()

    # if question.access_mode == 'subscribers':
    #     if not request.user.is_authenticated or not Subscription.objects.filter(follower=request.user.profile,
    #                                                                             followed=question.author).exists():
    #         return HttpResponseForbidden("Доступ только для подписчиков")

    if request.method == 'POST':
        model_manager.answer(request, question_id)
        return redirect('question', question_id=question_id)

    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = model_manager.pagination(request, 'tag', tag_name=tag_name)
    context['pop_tags'] = model_manager.get_popular_tags()
    context['pop_users'] = model_manager.get_popular_users()
    context['tag'] = tag_name
    return render(request, 'tag.html', context)


@login_required(login_url='login')
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(author=request.user.profile)

            # Process each uploaded file
            for file in request.FILES.getlist('files'):
                if file:
                    PostFile.objects.create(post=post, file=file)

            return redirect(reverse('question', kwargs={'question_id': post.id}))

    else:
        form = AskForm()

    return render(request, "ask.html", {
        'form': form,
        'pop_tags': model_manager.get_popular_tags(),
        'pop_users': model_manager.get_popular_users()
    })


def log_in(request):
    form = model_manager.get_login_form(request)
    if request.method == 'POST':
        user = authenticate(request, username=form['username'].value(), password=form['password'].value())
        if user is not None and form.is_valid():
            login(request, user)
            return redirect(reverse('index'))
        form.add_error('username', 'Username or Password is incorrect')
        form.add_error('password', 'Username or Password is incorrect')
    return render(request, "login.html", {'form': form, 'pop_tags': model_manager.get_popular_tags(),
                                          'pop_users': model_manager.get_popular_users()})


def signup(request):
    form = model_manager.get_signup_form(request)
    if request.method == 'POST':
        print(form)
        if form.is_password_valid():
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(reverse('index'))
        else:
            form.add_error('password', 'Пароли должны совпадать')
            form.add_error('repeat_password', 'Пароли должны совпадать')
    return render(request, "signup.html", context={'form': form, 'pop_tags': model_manager.get_popular_tags(),
                                                   'pop_users': model_manager.get_popular_users()})


@login_required(login_url='login')
def settings(request):
    profile_form = EditProfileForm(instance=request.user)
    password_form = ChangePasswordForm(user=request.user)

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
            password_form = ChangePasswordForm(user=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect(reverse('index'))
        elif 'password_form' in request.POST:
            profile_form = EditProfileForm(instance=request.user)
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get('new_password')
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Обновить сессию, чтобы не разлогинить пользователя
                return redirect(reverse('index'))

    return render(
        request,
        "settings.html",
        context={
            'profile_form': profile_form,
            'password_form': password_form,
            'pop_tags': model_manager.get_popular_tags(),
            'pop_users': model_manager.get_popular_users()}
    )


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required(login_url='login')
def like(request):
    count = model_manager.like(request)

    return JsonResponse({'count': count})


def profile(request, username=None):
    # Get the profile by username or fallback to current user if username is None
    profile_user = get_object_or_404(Profile, user__username=username) if username else request.user.profile

    # Retrieve all posts by this user
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_time')

    # Determine if the current user follows the profile user
    is_following = Subscription.objects.filter(follower=request.user.profile, followed=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers': profile_user.followers.count(),
        'following': profile_user.following.count(),
        'pop_tags': model_manager.get_popular_tags(),
        'pop_users': model_manager.get_popular_users(),
    }

    return render(request, 'profile.html', context)


@login_required
def follow_user(request, username):
    followed_user = get_object_or_404(Profile, user__username=username)
    if followed_user != request.user.profile:
        Subscription.objects.get_or_create(follower=request.user.profile, followed=followed_user)
    return redirect('user_profile', username=username)


@login_required
def unfollow_user(request, username):
    followed_user = get_object_or_404(Profile, user__username=username)
    Subscription.objects.filter(follower=request.user.profile, followed=followed_user).delete()
    return redirect('user_profile', username=username)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user.profile)
    if request.method == 'POST':
        form = AskForm(request.POST, instance=post)
        if form.is_valid():
            # Удаляем комментарии и оценки к старой версии
            post.answer_set.all().delete()
            PostLike.objects.filter(question_id=post).delete()
            form.save()
            return redirect('question', question_id=post.id)
    else:
        form = AskForm(instance=post)
    return render(request, 'layouts/elements/edit_post.html',
                  {'form': form,
                   'pop_tags': model_manager.get_popular_tags(),
                   'pop_users': model_manager.get_popular_users()},
                  )


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user.profile)
    if request.method == 'POST':
        # Удаляем комментарии и оценки
        post.answer_set.all().delete()
        PostLike.objects.filter(question_id=post).delete()
        post.delete()
        return redirect('/')
    return render(request, 'layouts/elements/delete_post_confirm.html',
                  {'post': post,
                   'pop_tags': model_manager.get_popular_tags(),
                   'pop_users': model_manager.get_popular_users()},
                  )


def followers_list(request, username=None):
    profile_user = get_object_or_404(Profile, user__username=username)
    followers = profile_user.followers.all()

    context = {
        'profile_user': profile_user,
        'followers': followers,
    }

    return render(request, 'followers_list.html', context)