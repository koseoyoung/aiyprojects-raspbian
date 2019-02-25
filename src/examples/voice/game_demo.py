#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging

from aiy.board import Board
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts



def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye')
    else:
        return ('구구단',
                '더하기',
                '업다운',
                '아재개그',
                '잘가',)

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default='ko-KR')
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        with Leds() as leds:
            while True:
                if hints:
                    logging.info('Say something, e.g. %s.' % ', '.join(hints))
                else:
                    logging.info('Say something.')
                text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                if text is None:
                    logging.info('You said nothing.')
                    continue

                logging.info('You said: "%s"' % text)
                text = text.lower()
                if '구구단' in text:
                    leds.update(Leds.rgb_on(Color.WHITE))
                    aiy.voice.tts.say('구구단을 시작합니다')
                elif '더하기' in text:
                    leds.update(Leds.rgb_on(Color.WHITE))
                    aiy.voice.tts.say('더하기 게임을 시작합니다')
                elif '업다운' in text:
                    leds.update(Leds.rgb_on(Color.WHITE))
                    aiy.voice.tts.say('업다운 게임을 시작합니다')
                elif '아재개그' in text:
                    leds.update(Leds.rgb_on(Color.WHITE))
                    aiy.voice.tts.say('아재개그 들려드릴게요')
                elif '잘가' in text:
                    break

if __name__ == '__main__':
    main()
