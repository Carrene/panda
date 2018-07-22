# Panda
A single sign-on application

![Panda](http://tadalafilforsale.net/data/media/1/51830280.jpg)

Setting up development Environment on Linux
----------------------------------

### Setup Python environment

    $ sudo apt-get install python3-pip python3-dev
    $ sudo pip3.6 install virtualenvwrapper
    $ echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
    $ echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
    $ source ~/.bashrc
    $ v.activate
    $ mkvirtualenv --python=$(which python3.6) --no-site-packages panda

#### Activating virtual environment
    
    $ workon panda

#### Upgrade pip, setuptools and wheel to the latest version

    $ pip install -U pip setuptools wheel
  
### Installing Project (edit mode)

#### Working copy
    
    $ cd /path/to/workspace
    $ git clone git@github.com:Carrene/panda.git
    $ cd panda
    $ pip install -e .
    
### Setup Database

#### Configuration

Create a file named `~/.config/panda.yml`

```yaml

db:
  url: postgresql://postgres:postgres@localhost/panda_dev
  test_url: postgresql://postgres:postgres@localhost/panda_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres

messaging:
  default_messenger: restfulpy.messaging.SmtpProvider

smtp:
  host: mail.carrene.com
  port: 587
  username: nc@carrene.com
  password: <smtp-password>
  local_hostname: carrene.com
   
```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ panda admin create-db --drop --mockup
    
And or

    $ panda admin create-db --drop --basedata 

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ panda [-c path/to/config.yml] admin drop-db

#### Create database

    $ panda [-c path/to/config.yml] admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ panda [-c path/to/config.yml] admin create-db --drop

