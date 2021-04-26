import os


# Load all commands from folder
def load(client):
    for file in os.listdir('./commands/'):
        if file.endswith('.py'):
            try:
                client.load_extension(f'commands.{file[:-3]}')
            except (Exception, ArithmeticError) as e:
                print("Could not load " + file)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                print(template.format(type(e).__name__, e.args))
