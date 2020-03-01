# Create slack bday chat

Create birthday channel in slack using this bot. That means that you can create channel without one person.

Run local build:

```console
CREATE_SLACK_BDAY_CHAT_FLASK_CONFIG=$(pwd)/docker/flask_cfg.py FLASK_ENV=development FLASK_APP=create_slack_bday_chat:app poetry run flask run --debugger --reload
```

## Code formatting

To format code type the following:

```console
$ black create_slack_bday_chat
```

To sort imports:

```console
$ isort -rc create_slack_bday_chat
```

```

## Project structure:
├── docker                          <- Files related to deployment via docker
|   ├── Dockerfile
|   ├── flask_cfg.py
|   └── gunicorn_cfg.py
|
├── iac                             <- Files related to deployment via docker
|   ├── ci
|   |   ├── build.yaml              <- Describes how and on what event to build project
|   |   ├── deploy-prod.yaml        <- Describes how and on what event to deploy project to pord
|   |   └── deploy-test.yaml        <- Describes how and on what event to deploy project to test
|   └── template-nomad.hcl          <- Get and set env vars. Set other variables of app 
├── tests          
|   └── test_api.py                 <- Api tests
|
├── create_slack_bday_chat 
    ^--------------------------------- Name of service in snake case
|   ├── __init__.py                 <- Says that folder is module
|   ├── error_handlers.py           <- Caught errors handlers 
|   ├── errors.py                   <- Custom errors implementation
|   ├── log.py                      <- Loguru sink, formatter and logger patch for correlation_id
|   ├── main.py                     <- Main file with configuration
|   ├── py.typed                    <- Says that module is typed
|   ├── routes.py                   <- Application routes
|   └── validator.py                <- Implement your data validator here 
│
├── .env.sample                     <- Excample of .env file. You can use it to set environment variables.
├── .gitignore                      <- Git will ignore matching files and folders
├── .gitlab-ci.yml                  <- Combines instructions from iac folder
├── pyproject.toml                  <- Dependencies. execute in console `poetry install` to install them. `poetry add LIB_NAME` to add new dependency.
├── README.md                       <- file you are reading
└── setup.cfg                       <- linter and isort settings
```
