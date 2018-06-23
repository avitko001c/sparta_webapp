# -*- coding: utf-8 -*-

DEVOPS = 1
STANDARD = 2
ROLE_CHOICES = (
	(DEVOPS, 'DevOps'),
	(STANDARD, 'Standard'),
)

KEY_TEMPLATE = '''
		<p><i class="far fa-edit"></i> <a href="{% url "userkey_edit" record.pk %}">Edit</a></p>
		<p><i class="far fa-trash-alt"></i> <a href="{% url "userkey_delete" record.pk %}">Delete</a></p>
	'''
