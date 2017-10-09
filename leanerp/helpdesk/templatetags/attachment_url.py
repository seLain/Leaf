"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

templatetags/admin_url.py - Very simple template tag allow linking to the
                            right auth user model urls.

{% url 'changelist'|user_admin_url %}
"""

from django import template

def attachment_url(url_text):
    
    static_url = "/".join(url_text.split("/")[2:])

    return static_url

register = template.Library()
register.filter(attachment_url)
