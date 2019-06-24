import os

from panda import panda as app


home_directory = os.environ['HOME']
configuration_file_name=f'{home_directory}/.config/panda.yml'


app.configure(filename=configuration_file_name)
app.initialize_orm()

