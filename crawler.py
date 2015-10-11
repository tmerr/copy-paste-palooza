import stackexchange
import re
import html
import itertools
import subprocess
import sys


max_requests_per_run = 20
api_key = 'R91Ul6Hz*Reptmjm52BPHQ(('
so = stackexchange.Site(stackexchange.StackOverflow, api_key)
so.include_body = True


languages = {
    'C#old': (['C#'], 'testcsharp.exe'),
    'C#' : (['C#'], 'roslyn_csharp.exe')
}


def fetch_code_blocks(lang, searchterms, max_requests=None):
    """
    loads stack overflow questions,
    and extracts all code blocks contained therein.
    yields [(source1, codeblock1), ..., (sourceM, codeblockM)]
    """
    tags, _ = languages[lang]
    questions = so.search(intitle=searchterms, tagged=';'.join(tags))
    if max_requests:
        # we only want to load max_requests - 1 questions since we already used
        # one for the search.
        questions = questions[:max_requests-1]
    for q in questions:
        q.fetch()
        for source in q.answers + [q]:
            found = re.findall(r'<code>(.*?)</code>', source.body, re.DOTALL)
            found = map(html.unescape, found)
            yield from [(source, c) for c in found]


def test_code_block(lang, block, regex):
    """
    Try to mangle the code block into something that compiles & runs then check
    the test cases against it. If it worked return the source code string that
    successfully passed the tests. Otherwise return None.
    """
    _, runstring = languages[lang]

    if sys.platform in ['linux', 'linux2', 'darwin']:
        runstring = './' + runstring
    else:
        runstring = runstring

    proc = subprocess.Popen([runstring, block, regex], stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 0:
        return out
    else:
        return None


def run_args(lang, keywords, regex):
    if lang not in languages:
        print('error: not a known language')
        return

    count = 0
    for src, block in fetch_code_blocks(lang, keywords, max_requests_per_run):
        result = test_code_block(lang, block, regex)
        if result is not None:
            result = result.decode('utf-8')
            print('// url: {}'.format(src.url))
            print('// code:\n{}'.format(result))
            return
        count += 1

    print("failed to find a match in any of {} code blocks".format(count))


def run_noargs():
    lang = input('language: ')
    if lang not in languages:
        print('error: not a known language')
        return
    keywords = input('keywords: ').split()
    regex = input('now enter a regex the console output must match: ')
    run_args(lang, keywords, regex)


if __name__ == '__main__':
    if len(sys.argv) >= 4:
        _, lang, keywords, regex, *_ = sys.argv
        run_args(lang, keywords, regex)
    elif len(sys.argv) == 1:
        run_noargs()
