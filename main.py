# -*- coding: utf-8 -*-

from wox import Wox

import textwrap
import re
import html
import urllib.request
import urllib.parse


agent = {'User-Agent': "Mozilla/5.0 (Android 9; Mobile; rv:67.0.3) Gecko/67.0.3 Firefox/67.0.3"}


def translate(to_translate, to_language="auto", from_language="auto", wrap_len="80"):
    base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
    to_translate = urllib.parse.quote(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="result-container">(.*?)<'
    re_result = re.findall(expr, data)
    if len(re_result) == 0:
        result = ""
    else:
        result = html.unescape(re_result[0])
    return "\n".join(textwrap.wrap(result, int(wrap_len) if wrap_len.isdigit() else 80))


class WoxTranslator(Wox):

    # noinspection PyMethodMayBeStatic
    def query(self, query):
        results = []

        if len(query.strip()) == 0:
            results.append({
                "Title": "No input",
                "SubTitle": "type: 'h en:pt an english sentence' to translate from english to portuguese",
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData"
            })
        else:
            if len(query) > 3 and ":" in query[0]:
                from_language = "auto"
                to_language = query[1:3]
                query = query[3:]
            elif len(query) > 5 and ":" in query[2]:
                from_language = query[:2]
                to_language = query[3:5]
                query = query[5:]
            else:
                from_language = 'en'
                to_language = 'pt'

            results.append({
                "Title": translate(query, to_language, from_language, "80"),
                "SubTitle": query,
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData"
            })

        return results


if __name__ == "__main__":
    WoxTranslator()
