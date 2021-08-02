import os

from django.core.exceptions import ImproperlyConfigured


def get_env_var(var, default=None):
	"""Returns os environment variable"""
	env_var = os.getenv(var, default)
	if env_var is None:
		raise ImproperlyConfigured(
			f"You need to set `{var}` environment variable"
		)
	elif env_var == 'True':
		return True
	elif env_var == 'False':
		return False

	return env_var
