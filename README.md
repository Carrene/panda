# Panda
A single sign-on application

![Panda](http://tadalafilforsale.net/data/media/1/51830280.jpg)

Setting up development Environment on Linux
----------------------------------

### Install Project (edit mode)

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

    $ panda db create --drop --mockup

And or

    $ panda db create --drop --basedata 

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ panda [-c path/to/config.yml] db --drop

#### Create database

    $ panda [-c path/to/config.yml] db --create

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ panda [-c path/to/config.yml] db create --drop

