import collections


_Language = collections.namedtuple('Language', ['name', 'code', 'native_name', 'iso_639_2B'])


class Languages(object):
    english = _Language(name=u'English', code=u'en', native_name=u'English', iso_639_2B=u'eng')
    french = _Language(name=u'French', code=u'fr', native_name=u'Français', iso_639_2B=u'fre')
    german = _Language(name=u'German', code=u'de', native_name=u'Deutsch', iso_639_2B=u'ger')
    spanish = _Language(name=u'Spanish', code=u'es', native_name=u'Español', iso_639_2B=u'spa')

    chinese = _Language(name=u'Chinese', code=u'zh', native_name=u'中国人', iso_639_2B=u'chi')
    japanese = _Language(name=u'Japanese', code=u'ja', native_name=u'日本', iso_639_2B=u'jpn')
    indonesia = _Language(name=u'Indonesia', code=u'id', native_name=u'bahasa Indonesia', iso_639_2B=u'ind')
    korean = _Language(name=u'Korean', code=u'ko', native_name=u'한국어', iso_639_2B=u'kor')

    hindi = _Language(name=u'Hindi', code=u'hi', native_name=u'हिंदी', iso_639_2B=u'hin')
    bengali = _Language(name=u'Bengali', code=u'bn', native_name=u'বাংলা', iso_639_2B=u'ben')
    marathi = _Language(name=u'Marathi', code=u'mr', native_name=u'मराठी', iso_639_2B=u'mar')
    telugu = _Language(name=u'Telugu', code=u'te', native_name=u'తెలుగు', iso_639_2B=u'tel')
    tamil = _Language(name=u'Tamil', code=u'ta', native_name=u'தமிழ்', iso_639_2B=u'tam')
    gujarati = _Language(name=u'Gujarati', code=u'gu', native_name=u'ગુજરાતી', iso_639_2B=u'guj')
    urdu = _Language(name=u'Urdu', code=u'ur', native_name=u'اردو', iso_639_2B=u'urd')
    kannada = _Language(name=u'Kannada', code=u'kn', native_name=u'ಕನ್ನಡ', iso_639_2B=u'kan')
    oriya = _Language(name=u'Oriya', code=u'or', native_name=u'ଓଡ଼ିଆ', iso_639_2B=u'ori')
    malayalam = _Language(name=u'Malayalam', code=u'ml', native_name=u'മലയാളം', iso_639_2B=u'mal')
    punjabi = _Language(name=u'Punjabi', code=u'pa', native_name=u'ਪੰਜਾਬੀ', iso_639_2B=u'pan')

    _members = (
        english,
        french,
        german,
        spanish,
        hindi,
        bengali,
        marathi,
        telugu,
        tamil,
        gujarati,
        urdu,
        kannada,
        oriya,
        malayalam,
        punjabi,
    )

    _lookup = {m.code: m.name for m in _members}
    _iso_639_2B_lookup = {m.code: m.iso_639_2B for m in _members}
    _language_code_native_name_mapping = {m.code: m.native_name for m in _members}

    @classmethod
    def get_native_name(cls, language_code):
        return cls._language_code_native_name_mapping[language_code]

    @classmethod
    def get_name(cls, language_code):
        return cls._lookup[language_code]

    @classmethod
    def get_all(cls):
        return [language._asdict() for language in cls._members]

    @classmethod
    def get_all_codes(cls):
        return [language.code for language in cls._members]

    @classmethod
    def get_iso_639_2b_code(cls, language_code):
        return cls._iso_639_2B_lookup[language_code]
