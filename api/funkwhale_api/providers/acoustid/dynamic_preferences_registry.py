from dynamic_preferences.types import StringPreference, Section
from dynamic_preferences.registries import global_preferences_registry

acoustid = Section('providers_acoustid')


@global_preferences_registry.register
class APIKey(StringPreference):
    section = acoustid
    name = 'api_key'
    default = ''
    verbose_name = 'Acoustid API key'
    help_text = 'The API key used to query AcoustID. Get one at https://acoustid.org/new-application.'