from subprocess import PIPE, Popen


def command(*args, stdin=PIPE, stdout=PIPE):
    with Popen(args, stdin=stdin, stdout=stdout, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"COMMAND ERRROR: {stderr.decode('utf-8')}")
        return stdout


svg_content = command("pdftocairo", "-svg", "-", "-", stdin=open(r"/volume/1.pdf"))

print(svg_content)
with open('ouput.html', "wb") as f:
    f.write(svg_content)
