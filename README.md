<h1 align="center">VirtualCoin</h1>
<pre>
VirtualCoin is web application of trading or asset market. Here client buy or sell to assets. Assets means GOLD, SILVER, PLATINUM etc. 
And Here we have to create rest api for that application.

For more information of rest api. read this api
</pre>
<h3>Build a git clone of this project. </h3>

<h3>Ready your virtual env. </h3> <pre>pip install -r requirment.txt </pre>

<h3> Then go to the manage.py directory. </h3>

<h3> RUN </h3> <pre>python manage.py makemigrations investment</pre>

<h3> RUN </h3> <pre>python manage.py makemigrations user</pre>

<h3> RUN </h3><pre>python manage.py migrate</pre>

<h3> Open Django Shell to create superuser</h3>

<h3> Before creating super user first create user from post collections user-API.</h3>

<pre><code>
>>>  from django.contrib.auth import get_user_model
>>>  User = get_user_model()
>>>  i = User.objects.get(pk=1)
>>>  i.is_superuser = True
>>>  i.is_staff = True
>>>  i.is_active = True
>>>  i.get_all_permissions()
>>>  i.save()
</code>
</pre>
