from django.db import models


# Create customer model
class User(models.Model):
    # user_id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True)

    # Meta data
    class Meta:
        db_table = 'User'  # set database name
        ordering = ['username']  # set ordering


# Create folder model
class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=60)
    username = models.ForeignKey(User, db_column='username', on_delete=models.CASCADE)

    # Meta data
    class Meta:
        db_table = 'Folder'  # set database name
        ordering = ['folder_id']  # set ordering


# Create set model
class Set(models.Model):
    set_id = models.AutoField(primary_key=True)
    set_name = models.CharField(max_length=100)
    # delete the object if the folder is deleted
    folder_id = models.ForeignKey(Folder, db_column='folder_id', on_delete=models.CASCADE)

    # Meta data
    class Meta:
        db_table = 'Set'  # set database name
        ordering = ['set_id']  # set ordering

# Create question model
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1500, null=True)
    level = models.IntegerField(default=1)
    set_id = models.ForeignKey(Set, db_column='set_id', on_delete=models.CASCADE)

    # Meta data
    class Meta:
        db_table = 'Question'  # set database name
        ordering = ['question_id']  # set ordering
