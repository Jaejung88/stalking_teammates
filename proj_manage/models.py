from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if len(postData["first_name"]) == 0:
            errors["first_name"] = "First Name Required"
        if len(postData["last_name"]) == 0:
            errors["last_name"] = "Last Name Required"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData["password"] != postData["confirm"]:
            errors["confirm"] = "Passwords doesn't match!"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["login_email"]):
            errors["login"] = "Invalid Email/Password"
        if len(postData["login_password"]) < 8:
            errors["login"] = "Invalid Email/Password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name}, Email: {self.email}"

class ProjectManager(models.Manager):
	def project_validator(self, postData):
		errors={}
		if len(postData['project_name']) < 3:
			errors['project_name'] = "Project name Must be atleast 3 charecters"
		if len(postData['project_desc']) == 0:
			errors['project_desc'] = "Project description is required"
		return errors

class Project(models.Model):
    project_name = models.CharField(max_length = 255)
    project_desc = models.TextField()
    project_due_date = models.DateField()
    admin_user = models.ForeignKey(User, related_name = "projects", on_delete = models.CASCADE)
    member = models.ManyToManyField(User, related_name = "projects_member")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProjectManager()

class Task(models.Model):
    task_name = models.CharField(max_length = 255)
    task_desc = models.TextField(max_length = 255)
    task_start_date = models.DateField()
    task_due_date = models.DateField()
    task_progress = models.IntegerField()
    project = models.ForeignKey(Project, related_name = "tasks", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "tasks", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)