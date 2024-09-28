from invoke import task


@task
def start(ctx):
    ctx.run("py -u src/main.py")


@task
def test(ctx):
    ctx.run("pytest src -p no:warnings")


@task
def lint(ctx):
    ctx.run("pylint src/")


@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
