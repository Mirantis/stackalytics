# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import urllib2

from oslo.config import cfg
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_rank(uri):
    fd = urllib2.urlopen(uri)
    raw = fd.read()
    fd.close()
    return [i for i in json.loads(raw) if i['name'] != '*independent']


URL = ('http://localhost/data/companies?metric=loc&release=havana'
       '&project_type=core')
OPTS = [
    cfg.StrOpt('uri', short='D', default=URL,
               help='Stackalytics URI'),
]


def main():
    conf = cfg.CONF
    conf.register_cli_opts(OPTS)
    conf.register_opts(OPTS)
    conf()

    if not conf.uri:
        exit(not 0)

    data = get_rank(conf.uri)

    img = Image.open('static/images/metrics_canvas.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/images/PTS55F.ttf", 12)

    space = 15
    for n in range(0, 10):
        if n >= len(data):
            break
        draw.text((18, 25 + n * space), str(n + 1), fill=0x93908c, font=font)
        draw.text((48, 25 + n * space), data[n]['name'], fill=0x1e2bd3,
                  font=font)
        rank = str(data[n]['metric'])
        w, h = draw.textsize(rank, font)
        draw.text((220 - w, 25 + n * space), rank, fill=0x93908c, font=font)

    img.save('static/images/stackalytics_top_10_companies.png', 'PNG')


if __name__ == '__main__':
    main()
