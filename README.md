[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![Generic badge](https://img.shields.io/badge/python-3.8%20-blue.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/version-v1.0-cc.svg)](https://github.com/Moreno98/hmd_project)

# hmd_project
This is the repository for the final human machine dialogue project at the University of Trento (Italy).  
This repo leverages the [Rasa](https://rasa.com/) framework.  

## Project structure:

    hmd_project
    ├── actions
    |    └── actions.py               [custom action file]
    ├── data
    |    ├── nlu.yml                  [yaml file containg the nlu data]
    |    ├── rules.yml                [yaml file containg the rules applied by the model]
    |    └── stories.yml              [yaml file containg the training data about the conversations, namely stories]
    ├── data
    |    └── database.db              [SQLite database containing the domain data]
    ├── test
    |    └── test_stories.yml         [yaml file containing the test stories for evaluation]
    |
    ├── alexa_connector.py            [python file for connecting Rasa to the custom Alexa skill]
    ├── config.yml                    [yaml file containing the configuration of Rasa]
    ├── credentials.yml               [yaml file describes the credentials for Rasa x usage]
    ├── domain.yml                    [yaml file containing the domain information for Rasa]
    ├── endpoints.yml                 [yaml file for the Rasa endpoint]
    └── main.html                     [this file launches the GUI]


