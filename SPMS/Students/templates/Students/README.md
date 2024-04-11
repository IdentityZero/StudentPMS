# We store templates related to STUDENTS here
## These are usually html files

To access static files inside the html templates:
Like css, images, and js
### {% load static %} - Put this on top of the html file

To access them:
    {% static 'Students/js/filename.js' %}
Examples:
    JS:
        <script src="{% static 'Students/js/register.js' %}"></script>
    css:
        <link rel="stylesheet" href="{% static 'Students/css/register.css' %}">
    Images:
        <img  src="{% static 'Students/images/register.png' %}" alt="{{user.username}}'s Profile Picture">

They should be case sensitive

If possible make the template name, js, and css names to be the same