{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activision
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}
{{token}}
{% endblock %}