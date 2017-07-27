from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..forms import MemberRegistrationForm
from ..models import Member


class RegisterView(View):
    @staticmethod
    def get_form(*args, **kwargs):
        return MemberRegistrationForm(*args, **kwargs)

    def render_form(self, form):
        return render(
            self.request,
            'klubevents/members/register.html',
            {'form': form}
        )

    def get(self, request):
        form = self.get_form()

        return self.render_form(form)

    def post(self, request):
        form = self.get_form(self.request.POST)

        if form.is_valid():
            # make the user, the member, and tie them together
            full_name = request.POST['full_name']
            if ' ' in full_name:
                first, last = full_name.split(' ')
            else:
                first, last = full_name, ''

            email = request.POST['email']

            user = User.objects.create_user(
                email,
                email,
                request.POST['password'],
                first_name=first,
                last_name=last
            )

            member = Member(
                # @TODO: This info can just come from the user, but we're
                # mostly playing now and this is contrived
                email=email,
                name=request.POST['full_name'],
                user=user
            )
            member.save()

            login(request, user)

            return render(
                self.request,
                'klubevents/members/welcome.html',
                { 'member': member }
            )
        else:
            return self.render_form(form)

