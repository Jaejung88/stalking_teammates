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
    project_progress = models.IntegerField(null = True)
    admin_user = models.ForeignKey(User, related_name = "projects", on_delete = models.CASCADE)
    member = models.ManyToManyField(User, related_name = "projects_member")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProjectManager()
    
    def __repr__(self):
        print(f" member: {self.member}")

class TaskManager(models.Manager):
    def task_validator(self, postData):
        errors = {}
        if len(postData['task_name']) < 3:
            errors['task_name'] = "Task name should be at least 3 characters"
        if len(postData['task_desc']) == 0:
            errors['task_desc'] = "Task description is needed"
        return errors

class Task(models.Model):
    task_name = models.CharField(max_length = 255)
    task_desc = models.TextField(max_length = 255)
    task_owner = models.TextField(max_length = 255, default = "TBD")
    task_start_date = models.DateField()
    task_due_date = models.DateField()
    task_progress = models.IntegerField()
    task_urgency = models.CharField(max_length = 45, default = "Just Start")
    task_status = models.CharField(max_length = 45, default = "Just Start")
    project = models.ForeignKey(Project, related_name = "tasks", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "tasks", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TaskManager()

class Message(models.Model):
    message = models.TextField()
    users = models.ForeignKey(User, related_name = "post_message", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name = "post_comment", on_delete= models.CASCADE)
    message = models.ForeignKey(Message, related_name = "include_comment", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)