from django.db.utils import Error
from django.test import TestCase
from django.core.exceptions import *
from .models import *
from django.contrib.auth.models import AnonymousUser, User
from datetime import datetime

# Create your tests here.


class Custom_GroupTestCase(TestCase):

    def setUp(self):
        Custom_Group.objects.create(
            name="Group1", description="Test for a group")
        Custom_Group.objects.create(name="Group2", description=True)
        Custom_Group.objects.create(name=3)
        Custom_Group.objects.create(description="Group without name")

    def test_Custom_Group_are_valid(self):
        # Test if groups are corectly defined
        Valid_Group = Custom_Group.objects.get(name="Group1")
        Invlid_Group1 = Custom_Group.objects.get(name="Group2")
        Invlid_Group2 = Custom_Group.objects.get(name=3)
        try:
            Invlid_Group3 = Custom_Group.objects.get(
                description="Group without name")
        except ValueError as error:
            print(error)
            pass


class AccessTestCase(TestCase):

    def setUp(self):
        user_jacob = User.objects.create_user(
            username="jacob", email="jacob@gmail.com", password="top_secret")
        group_test = Custom_Group.objects.create(
            name="Group1", description="Test for a group")
        Access.objects.create(user=user_jacob, group=group_test,
                              is_staff=True, is_admin=True, is_developper=True)
        User.objects.create_user(
            username="titi", email="titi@gmail.com", password="top_secret")

    def test_Access_ValueError(self):
        # Test if access are corectly defined
        Valid_Access = Access.objects.get(
            user=User.objects.get(username="jacob"))

        try:
            Access.objects.create(user=User.objects.get(username="toto"), group=Custom_Group.objects.get(name="Group1"),
                                  is_staff=True, is_admin=True, is_developper=True)
        except User.DoesNotExist as error:
            self.assertTrue('User matching query does not exist.' in str(error))

    def test_Access_DoesNotExist(self):
        # Test If username are not link to the access
        user = User.objects.get(username='titi')
        try:
            Access.objects.get(user=user)
        except Access.DoesNotExist as error:
            self.assertTrue(
                'Access matching query does not exist.' in str(error))


class StatusTestCase(TestCase):
    # Class identique aux Custom_Group
    def setUp(self):
        Status.objects.create(name="Status1", description="Test for a status")
        Status.objects.create(
            name="Status2", description="Test for a second status")

    def test_Status_are_valid(self):
        # Test if groups are corectly defined
        Valid_Group = Status.objects.get(name="Status1")
        try:
            Status.objects.create(
                description="Must be an error because name isn't optionnal")
        except ValueError as error:
            print(error)
            pass


class TaskTestCase(TestCase):

    def setUp(self):
        my_user = User.objects.create_user(
            username="jacob", email="jacob@gmail.com", password="top_secret")
        delta = datetime(2022, 2, 22)
        Custom_Group.objects.create(
            name="Group1", description="Test for a group")
        Project.objects.create(name="Project1", description="It's a simple test",
                               end_date=delta, group=Custom_Group.objects.get(name="Group1"))
        Status.objects.create(name="Status1", description="Test for a status")
        Task.objects.create(project=Project.objects.get(name="Project1"), name="Task1",
                            end_date=delta, status=Status.objects.get(
                                name="Status1"),
                            owner=my_user)
        Task.objects.create(project=Project.objects.get(name="Project1"), name="Task2",
                            end_date=delta, status=Status.objects.get(
                                name="Status1"),
                            owner=my_user)

    def test_Task_are_valid(self):
        Task.objects.get(name="Task1")
        Task.objects.get(name="Task2")

    def test_Task_project_DoesNotExist(self):
        try:
            delta = datetime(2022, 2, 22)
            Task.objects.create(project="Wrong_Project", name="Task",
                                end_date=delta, priority=0, status=Status.objects.get(name="Status1"), estimation=0,
                                owner=User.objects.get(username="jacob"))
        except ValueError as error:
            self.assertTrue(
                '"Task.project" must be a "Project" instance.' in str(error))

    def test_Task_name_DoesNotExist(self):
        try:
            delta = datetime(2022, 2, 22)
            Task.objects.create(project=Project.objects.get(name="Project1"),
                                end_date=delta, status=Status.objects.get(
                                    name="Status1"),
                                owner=User.objects.get(username="jacob"))
        except ValueError as error:
            print(error)
            pass

    def test_Task_prio_and_esti_NotPositiv(self):
        delta = datetime(2022, 2, 22)
        try:
            Task.objects.create(project=Project.objects.get(name="Project1"), name="Task",
                                end_date=delta, priority=-1, status=Status.objects.get(name="Status1"), estimation=0,
                                owner=User.objects.get(username="jacob"))
        except ValueError as error:
            print(error)
            pass
        try:
            Task.objects.create(project=Project.objects.get(name="Project1"), name="Task",
                                end_date=delta, priority=0, status=Status.objects.get(name="Status1"), estimation=120,
                                owner=User.objects.get(username="jacob"))
        except ValueError as error:
            print(error)
            pass

    def test_Task_Owner_DoesNotExist(self):
        delta = datetime(2022, 2, 22)
        try:
            Task.objects.create(project=Project.objects.get(name="Project1"), name="Task",
                                end_date=delta, status=Status.objects.get(
                                    name="Status1"),
                                owner=User.objects.get(username="Wrong_User"))
        except User.DoesNotExist as error:
            self.assertTrue(
                'User matching query does not exist.' in str(error))

    def test_Task_Status_DoesNotExist(self):
        delta = datetime(2022, 2, 22)
        try:
            Task.objects.create(project=Project.objects.get(name="Project1"), name="Task",
                                end_date=delta, status=Status.objects.get(
                                    name="Wrong_Status"),
                                owner=User.objects.get(username="jacob"))
        except Status.DoesNotExist as error:
            self.assertTrue(
                'Status matching query does not exist.' in str(error))

    def test_Task_Invalid_Parent_Task(self):
        delta = datetime(2022, 2, 22)
        try:
            Task.objects.create(project=Project.objects.get(name="Project1"), name="Task",
                                end_date=delta, status=Status.objects.get(
                                    name="Status1"),
                                owner=User.objects.get(username="jacob"),
                                parent_task=Task.objects.get(name="Wrong_Task"))
        except Task.DoesNotExist as error:
            self.assertTrue(
                'Task matching query does not exist.' in str(error))


class ProjectTestCase(TestCase):

    def setUp(self):
        delta = datetime(2022, 2, 22)
        Custom_Group.objects.create(
            name="Group1", description="Test for a group")
        Project.objects.create(name="Project1", description="It's a simple test",
                               end_date=delta, percentage=0, 
                               group=Custom_Group.objects.get(name="Group1"))
        Project.objects.create(name="Project2", description="It's a second test",
                               end_date=delta, percentage=2,
                               group=Custom_Group.objects.get(description="Test for a group"))


    def test_Project_are_valid(self):
        Project.objects.get(name="Project1")
        Project.objects.get(percentage=2)
        
    def test_Project_name_DoesNotExist(self):
        try:
            delta = datetime(2022, 2, 22)
            Project.objects.create(description="There is no name",
                                end_date=delta, percentage=13,
                                group=Custom_Group.objects.get(name="Group1"))
        except ValueError as error:
            print(error)
            pass

    def test_Project_description_DoesNotExist(self):
        try:
            delta = datetime(2022, 2, 22)
            Project.objects.create(name="There is no description",
                                end_date=delta, percentage=13,
                                group=Custom_Group.objects.get(name="Group1"))
        except ValueError as error:
            print(error)
            pass

    def test_Project_percentage_NotPositiv(self):
        delta = datetime(2022, 2, 22)
        try:
            Project.objects.create(name="Project_test", description="It's a simple test",
                                end_date=delta, percentage=-16,
                                group=Custom_Group.objects.get(name="Group1"))
        except ValueError as error:
            print(error)
            pass
        try:
            Project.objects.create(name="Project_test", description="It's a simple test",
                                end_date=delta, percentage=156,
                                group=Custom_Group.objects.get(name="Group1"))
        except ValueError as error:
            print(error)
            pass
    
    def test_Project_Group_DoesNotExist(self):
        delta = datetime(2022, 2, 22)
        try:
            Project.objects.create(name="Project_test", description="It's a simple test",
                                end_date=delta, percentage=42,
                                group=Custom_Group.objects.get(name="Wrong_Group"))
        except Custom_Group.DoesNotExist as error:
            self.assertTrue(
                'Custom_Group matching query does not exist.' in str(error))