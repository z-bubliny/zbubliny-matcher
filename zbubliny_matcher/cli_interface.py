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
    from zbubliny_matcher.word2vec_matcher import SimpleWord2VecMatcher

    m = SimpleWord2VecMatcher(debug=debug)
    print("Loading model...")
    m.load_language_model("it", os.path.join(vector_dir, "wiki.{0}.vec".format(source_language)))
    print("Model loaded.")

    for i, filename in enumerate(glob.glob(os.path.join(text_dir, "*.txt"))):
        with codecs.open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            score = m(text, keywords, source_language, keyword_language)
            print("{0}: {1}".format(filename, score))

        if limit > 0 and i >= limit - 1:
            break


def run():
    run_it(auto_envvar_prefix="ZBUBLINY")