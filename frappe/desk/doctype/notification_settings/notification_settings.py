# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class NotificationSettings(Document):
	def on_update(self):
		from frappe.desk.notifications import clear_notification_config
		clear_notification_config(frappe.session.user)


def is_notifications_enabled(user):
	enabled = frappe.db.get_value('Notification Settings', user, 'enabled')
	if enabled is None:
		return True
	return enabled

def is_email_notifications_enabled(user):
	enabled = frappe.db.get_value('Notification Settings', user, 'enable_email_notifications')
	if enabled is None:
		return True
	return enabled

def is_email_notifications_enabled_for_type(user, notification_type):
	fieldname = 'enable_email_' + frappe.scrub(notification_type)
	enabled = frappe.db.get_value('Notification Settings', user, fieldname)
	if enabled is None:
		return True
	return enabled

@frappe.whitelist()
def create_notification_settings():
	_doc = frappe.new_doc('Notification Settings')
	_doc.name = frappe.session.user
	_doc.insert(ignore_permissions=True)
	frappe.db.commit()


@frappe.whitelist()
def get_subscribed_documents():
	try:
		doc = frappe.get_doc('Notification Settings', frappe.session.user)
		subscribed_documents = [item.document for item in doc.subscribed_documents]
	except (frappe.DoesNotExistError, ImportError):
		subscribed_documents = []

	return subscribed_documents


def get_permission_query_conditions(user):
	if not user: user = frappe.session.user

	return '''(`tabNotification Settings`.user = '{user}')'''.format(user=user)
