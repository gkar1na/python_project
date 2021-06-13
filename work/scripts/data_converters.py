from work import config


class BasicConverter:
    """Basic class to configure default parameters"""

    _d = config.default_font.split('.')
    defaults = {
        'font': _d[0],
        'size': _d[1],
        'bold': str(int(_d[2] != 'normal')),
        'italic': str(int(_d[3] != 'roman')),
        'underline': _d[4],
        'overstrike': _d[5],
        'f_color': config.default_foreground_color,
        'b_color': config.default_background_color
    }


class Parser(BasicConverter):
    """Class to convert text from file into character list"""

    d_font = config.default_font
    d_f_color = config.default_foreground_color
    d_b_color = config.default_background_color

    parser_tags = {
        'f': ['font', config.families],
        's': ['size', config.sizes],
        'b': ['bold', config.weights],
        'i': ['italic', config.slants],
        'u': ['underline', config.underlines],
        'o': ['overstrike', config.overstrikes],
        'cb': ['b_color', config.colors],
        'cf': ['f_color', config.colors]
    }

    def params_to_tags(self, params: dict):
        """Convert parameters dict into set of string tags"""
        _params = dict(params)
        tags = set()
        _params['bold'] = 'bold' if _params['bold'] == '1' else 'normal'
        _params['italic'] = 'italic' if _params['italic'] == '1' else 'roman'
        font = '.'.join(map(str, [_params[k] for k in list(_params)[:-2]]))
        if font != self.d_font:
            tags.add(font)
        if _params['f_color'] != self.d_f_color:
            tags.add(_params['f_color'] + '_fore')
        if _params['b_color'] != self.d_b_color:
            tags.add(_params['b_color'] + '_back')
        return tags

    def update_params(self, tag: str, params: dict):
        """Change character parameters according to given tag"""
        try:
            key, value = tag.split(':')
            if key == 'b':
                if value == '1':
                    v = 'bold'
                elif value == '0':
                    v = 'normal'
                else:
                    v = 'wrong'
            elif key == 'i':
                if value == '1':
                    v = 'italic'
                elif value == '0':
                    v = 'roman'
                else:
                    v = 'wrong'
            else:
                v = value
            param, variants = self.parser_tags[key]
            if v not in variants:
                return 0
            params[param] = value
        except (KeyError, ValueError) as e:
            return 0
        return 1

    def parse(self, text: str):
        """Convert text into character list"""
        char_list = []
        params = dict(self.defaults)
        i, j = 1, 0
        k = 0
        while k < len(text):
            if text[k] == '<':
                if text[k + 1] == '<' or text[k + 1] == '>':
                    char_el = {
                        'char': text[k + 1],
                        'index': str(i) + '.' + str(j),
                        'tags': self.params_to_tags(params)
                    }
                    char_list.append(char_el)
                    k += 1
                    j += 1
                else:
                    m = k + 1
                    while text[k] != '>':
                        k += 1
                    if not self.update_params(text[m: k], params):
                        return None
            elif text[k] == '>':
                if k == 0 or text[k - 1] != '<':
                    return None
            else:
                char = text[k]
                char_el = {
                    'char': char,
                    'index': str(i) + '.' + str(j),
                    'tags': self.params_to_tags(params)
                }
                char_list.append(char_el)
                j += 1
                if char == '\n':
                    i += 1
                    j = 0
            k += 1
        return char_list

    def parse_from_txt(self, text: str):
        """Convert text from txt files into character list"""
        char_list = []
        tags = self.params_to_tags(self.defaults)
        i, j = 1, 0
        for char in text:
            char_el = {
                'char': char,
                'index': str(i) + '.' + str(j),
                'tags': tags
            }
            char_list.append(char_el)
            j += 1
            if char == '\n':
                i += 1
                j = 0
        return char_list


class Serializer(BasicConverter):
    """Class to convert character list into text for file"""

    serializer_tags = {
        'font': '<f:%s>',
        'size': '<s:%s>',
        'bold': '<b:%s>',
        'italic': '<i:%s>',
        'underline': '<u:%s>',
        'overstrike': '<o:%s>',
        'b_color': '<cb:%s>',
        'f_color': '<cf:%s>'
    }

    def tags_to_params(self, tags: set):
        """Convert set of string tags into parameters dict"""
        params = dict(self.defaults)
        for tag in tags:
            if tag == 'sel':
                continue
            elif tag.startswith('#'):
                color, pos = tag.split('_')
                if pos == 'fore':
                    params['f_color'] = color
                else:
                    params['b_color'] = color
            else:
                p = tag.split('.')
                params['font'] = p[0]
                params['size'] = p[1]
                params['bold'] = str(int(p[2] != 'normal'))
                params['italic'] = str(int(p[3] != 'roman'))
                params['underline'] = p[4]
                params['overstrike'] = p[5]
        return params

    def serialize(self, char_list: list):
        """Convert character list into text"""
        cur_params = self.tags_to_params(set())
        text = []
        for char_el in char_list:
            char_params = self.tags_to_params(char_el['tags'])
            for param in char_params:
                if char_params[param] != cur_params[param]:
                    cur_params[param] = char_params[param]
                    text.append(self.serializer_tags[param] % char_params[param])
            char = char_el['char']
            if char == '<' or char == '>':
                text.append('<')
            text.append(char)
        text = ''.join(text)
        return text

    def serialize_to_txt(self, char_list: list):
        """Convert character list into text for txt files"""
        text = ''.join([char['char'] for char in char_list])
        return text
