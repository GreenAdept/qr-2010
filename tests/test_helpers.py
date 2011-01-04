
from django.contrib.auth.models import User

def check_context(testcase, context_items):
    try:
        for item in context_items:
            testcase.response.context[item]
    except KeyError:
        testcase.fail('%s not in context' % item)

def create_users(testcase):
    user1 = User.objects.create_user('user1','','user1')
    user1.save()
    user2 = User.objects.create_user('user2','','user2')
    user2.save()
    testcase.assertEqual(User.objects.all().count(), 2)

