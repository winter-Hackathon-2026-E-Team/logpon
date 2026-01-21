from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminSignupForm, JoinCodeForm, PinSetForm, PinVerifyForm, AdminLoginForm, MemberForm, AdminPinForm, AvatarUpdateForm
from django.utils.crypto import get_random_string
from .models import Household, Users, JoinCode
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from django.http import HttpResponse
from .models import Users as Member

HK = "household_id"
MK = 'active_member_id'
LS = 'profile_last_seen'
PIN_MAX_TRIES = 5
PIN_LOCK_MINUTES =15

