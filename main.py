#/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import string
from bs4 import BeautifulSoup
from getpass import *
from os import listdir
from os.path import join, isfile
import sys

n=len(sys.argv)
if n!=3:
    print("invalid arguments\nmain [problem_id] [code_file]")
    exit()

problem_id = sys.argv[1]

file_name=sys.argv[2]

compiler_id="11"

if file_name.endswith("cpp"):
    compiler_id="1"
elif file_name.endswith("c"):
    compiler_id="6"

judge_site = 'https://iscoj.ckefgisc.org'

session = requests.Session()
def login():
    username = input("username:")
    password = input("password:")
    global session
    rel = session.get(judge_site + '/users/sign_in')
    soup = BeautifulSoup(rel.text, "html.parser")
    inputs = soup.find('form').find_all('input')
    rel = session.post(judge_site + '/users/sign_in', data = {
        inputs[0].attrs['name']: inputs[0].attrs['value'],
        'user[username]': username,
        'user[password]': password,
        'user[remember_me]': '1',
        'commit': 'Sign in'
        })

try:
    login()
    sign_up_get_url = judge_site + '/problems/%s/submissions/new' % problem_id
    sign_up_post_url = judge_site + '/problems/%s/submissions' % problem_id
except:
    print("login failed")
    exit()
try:
    rel = session.get(sign_up_get_url)
    soup = BeautifulSoup(rel.text, "html.parser")
    inputs = soup.find('form').find_all('input')
    rel = session.post(sign_up_post_url, data = {
        inputs[0].attrs['name']: inputs[0].attrs['value'],
        'submission[compiler_id]':compiler_id,
        'submission[code_content_attributes][code]': '',
        'commit': 'Create Submission'
    },files={
        'submission[code_file]':open(file_name,'rb')
    }
    )
except:
    print("Operation failed")
    exit()
if "200" == str(rel).split("[")[1].split("]")[0]:
    print("Operation success, waiting for judge result")
else:
    print("Operation failed")
