# Generated by Django 3.2.9 on 2021-12-07 05:29

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
            ],
        ),
        migrations.CreateModel(
            name='Supervisior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3)])),
                ('lname', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3)])),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('teacher', models.ManyToManyField(related_name='enrolled', to='student.Supervisior')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3)])),
                ('lname', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3)])),
                ('address', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='static/uploads/')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator])),
                ('DOB', models.DateField()),
                ('age', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MinValueValidator(25)])),
                ('grade', models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MinValueValidator(12)])),
                ('roll_no', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled', to='student.faculty')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='faculty',
            name='subject',
            field=models.ManyToManyField(related_name='contains', to='student.Subject'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='teacher',
            field=models.ManyToManyField(related_name='supervisor', to='student.Supervisior'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
