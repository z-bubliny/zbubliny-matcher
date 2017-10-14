import click
import os
import glob


@click.command()
@click.option('-l', "--limit", default=-1, type=int)
@click.option('-v', "--vector_dir", required=True)
@click.option('-t', "--text_dir", required=True)
@click.option('-s', "--source_language", default="cs", required=True)
@click.option('-d', "--destination_language", required=True)
@click.argument("keywords", nargs=-1)
def run_it(keywords, vector_dir, text_dir, source_language, destination_language, limit):
    from zbubliny_matcher.word2vec_matcher import SimpleWord2VecMatcher

    m = SimpleWord2VecMatcher(debug=True)
    m.load_language_model("it", os.path.join(vector_dir, "wiki.{0}.vec".format(destination_language)))

    for i, filename in enumerate(glob.glob(os.path.join(text_dir, "*.txt"))):
        with open(filename, "r") as f:
            text = f.read()
            print("Testing file {0}...".format((filename)))
            score = m(text, keywords, destination_language, source_language)

        if limit > 0 and i >= limit - 1:
            break


def run():
    run_it(auto_envvar_prefix="ZBUBLINY")