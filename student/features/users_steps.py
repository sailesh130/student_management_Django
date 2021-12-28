from aloe import before, step, world
from aloe.tools import guess_types
from aloe_django.steps.models import get_model
from ..models import CustomUser
from rest_framework.test import APIClient


@before.each_feature
def before_each_feature(feature):
    world.client = APIClient()


@step('I empty the "([^"]+)" table')
def step_empty_table(self, model_name):
    get_model(model_name).objects.all().delete()


@step('I create the following users:')
def step_create_users(self):
    world.register = world.client.post('/api/register/',data = guess_types(self.hashes)[0])
    

@step('I log in with email "([^"]+)" and password "([^"]+)"')
def step_log_in(self, email, password):
    world.is_logged_in = world.client.post('/api/login/',{"email":email,"password":password})
   
   

@step('I am logged in')
def step_confirm_log_in(self):
    assert world.is_logged_in