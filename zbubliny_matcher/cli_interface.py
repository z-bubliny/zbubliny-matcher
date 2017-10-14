import click
import os
import glob
import codecs


@click.command()
@click.option('-l', "--limit", default=-1, type=int)
@click.option('-v', "--vector_dir", required=True)
@click.option('-t', "--text_dir", required=True)
@click.option('-k', "--keyword_language", default="cs", required=True)
@click.option('-s', "--source_language", required=True)
@click.option('-d', "--debug", is_flag=True)
@click.argument("keywords", nargs=-1)
def run_it(keywords, vector_dir, text_dir, keyword_language, source_language, limit, debug):
    from zbubliny_matcher.matchers import SentenceVecMatcher

    m = SentenceVecMatcher(debug=debug)
    m.load_language_model(source_language, os.path.join(vector_dir, "wiki.{0}.vec".format(source_language)))

    for i, filename in enumerate(glob.glob(os.path.join(text_dir, "*.txt"))):
        with codecs.open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            score = m(text, keywords, source_language, keyword_language)
            print("{0}, {1}".format(filename, score))

        if limit > 0 and i >= limit - 1:
            break


def run():
    run_it(auto_envvar_prefix="ZBUBLINY")



@click.command()
@click.option('-l', "--limit", default=-1, type=int)
@click.option('-v', "--vector_dir", required=True)
@click.option('-t', "--text_dir", required=True)
@click.option('-k', "--keyword_language", default="cs", required=True)
@click.option('-s', "--source_language", required=True)
@click.option('-d', "--debug", is_flag=True)
@click.argument("keywords", nargs=-1)
def run_it_multi(keywords, vector_dir, text_dir, keyword_language, source_language, limit, debug):
    from zbubliny_matcher.matchers import SentenceVecMatcher, NgramVecMatcher

    m = SentenceVecMatcher(debug=debug)
    m.load_language_model(source_language, os.path.join(vector_dir, "wiki.{0}.vec".format(source_language)))

    matchers = [m]
    for i in range(1, 6):
        n_matcher = NgramVecMatcher(i, debug=debug)
        n_matcher.add_language_model(source_language, m.models[source_language])
        matchers.append(n_matcher)

    for i, filename in enumerate(glob.glob(os.path.join(text_dir, "*.txt"))):
        with codecs.open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            scores = [m(text, keywords, source_language, keyword_language) for m in matchers]
            print("{0}, {1}".format(filename, ", ".join([str(score) for score in scores])))

        if limit > 0 and i >= limit - 1:
            break


def run_multi():
    run_it_multi(auto_envvar_prefix="ZBUBLINY")