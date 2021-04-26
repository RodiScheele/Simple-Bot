import os


# Load all commands from folder
def load(client):
    for f in os.listdir('./commands/'):
        if f.endswith('.py'):
            try:
                client.load_extension(f'commands.{f[:-3]}')
            except (Exception, ArithmeticError) as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                print(template.format(type(e).__name__, e.args))
