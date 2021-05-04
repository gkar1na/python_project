#!/usr/bin/env python
# coding: utf-8

import config


parser_tags = {
    'f': ['font', str],
    's': ['size', int],
    'b': ['bold', int],
    'i': ['italic', int],
    'u': ['underline', int],
    'o': ['overstrike', int],
    'cb': ['b_color', str],
    'cf': ['f_color', str]
}

serializer_tags = {
    'font': '<f:%s>',
    'size': '<s:%d>',
    'bold': '<b:%d>',
    'italic': '<i:%d>',
    'underline': '<u:%d>',
    'overstrike': '<o:%d>',
    'b_color': '<cb:%s>',
    'f_color': '<cf:%s>'
}


class FileOperator:
    """Basic class to configure default parameters"""

    _d = config.default_font.split('.')
    defaults = {
        'font': _d[0],
        'size': int(_d[1]),
        'bold': int(_d[2] != 'n'),
        'italic': int(_d[3] != 'r'),
        'underline': int(_d[4]),
        'overstrike': int(_d[5]),
        'f_color': config.default_foreground_color,
        'b_color': config.default_background_color
    }


class Parser(FileOperator):
    """Class to read text from file"""

    d_font = config.default_font
    d_f_color = config.default_foreground_color
    d_b_color = config.default_background_color

    def _params_to_tags(self, params: dict):
        """Converts parameters dict into set of string tags"""
        tags = set()
        params['bold'] = 'b' if params['bold'] else 'n'
        params['italic'] = 'i' if params['italic'] else 'r'
        font = '.'.join(map(str, [params[k] for k in list(params)[:-2]]))
        if font != self.d_font:
            tags.add(font)
        if params['f_color'] != self.d_f_color:
            tags.add(params['f_color'] + '_fore')
        if params['b_color'] != self.d_b_color:
            tags.add(params['b_color'] + '_back')
        return tags

    def _update_params(self, tag: str, params: dict):
        """Changes character parameters according to given tag"""
        key, value = tag.split(':')
        param, func = parser_tags[key]
        params[param] = func(value)

    def parse(self, f_name: str):
        """Reads text from file and converts it into character list"""
        f = open(f_name, 'r')
        char_list = []
        text = f.read()
        f.close()
        params = dict(self.defaults)
        i, j = 1, 1
        k = 0
        while k < len(text):
            if text[k] == '<':
                if text[k + 1] == '<' or text[k + 1] == '>':
                    char_el = {
                        'char': text[k + 1],
                        'index': str(i) + '.' + str(j),
                        'tags': self._params_to_tags(params)
                    }
                    char_list.append(char_el)
                    k += 1
                    j += 1
                else:
                    m = k + 1
                    while text[k] != '>':
                        k += 1
                    self._update_params(text[m: k], params)
            elif text[k] == '\n':
                i += 1
                j = 1
            else:
                char_el = {
                    'char': text[k],
                    'index': str(i) + '.' + str(j),
                    'tags': self._params_to_tags(params)
                }
                char_list.append(char_el)
                j += 1
            k += 1
        return char_list


class Serializer(FileOperator):
    """Class to save text to file"""

    def _tags_to_params(self, tags: set):
        """Converts set of string tags into parameters dict"""
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
                params['size'] = int(p[1])
                params['bold'] = int(p[2] != 'n')
                params['italic'] = int(p[3] != 'r')
                params['underline'] = int(p[4])
                params['overstrike'] = int(p[5])
        return params

    def serialize(self, f_name: str, char_list: list):
        """Converts character list into text and saves it to file"""
        f = open(f_name, 'w')
        line = 1
        cur_params = self._tags_to_params(set())
        for char_el in char_list:
            char_line = int(char_el['index'].split('.')[0])
            if char_line > line:
                for i in range(line, char_line):
                    line += 1
                    f.write('\n')
            char_params = self._tags_to_params(char_el['tags'])
            for param in char_params:
                if char_params[param] != cur_params[param]:
                    cur_params[param] = char_params[param]
                    f.write(serializer_tags[param] % char_params[param])
            char = char_el['char']
            if char == '<' or char == '>':
                f.write('<')
            f.write(char)
        f.close()


def test():
    """Function to test classes' operability"""
    s = Serializer()
    text = [{'char': 'a',
             'index': '3.1',
             'tags': {'Arial.16.b.i.1.1'}},
            {'char': 'b',
             'index': '3.2',
             'tags': {'Arial.16.b.i.1.1'}},
            {'char': 'c',
             'index': '3.3',
             'tags': {'Arial.14.b.i.0.1'}}]
    s.serialize('test.txt', text)
    p = Parser()
    assert p.parse('test.txt') == text


if __name__ == '__main__':
    test()
