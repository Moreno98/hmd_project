[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![Generic badge](https://img.shields.io/badge/python-3.8%20-blue.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/version-v1.0-cc.svg)](https://github.com/Moreno98/hmd_project)

# Human Machine Dialogue Project
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
    └── GUI.html                      [this file launches the GUI]

---
## Installation
This project is based on Rasa so make sure to have it installed in the current python environment. 
<--- install rasa --->

## Usage
This repository contains the final model of the project, there is no need of training. 
```
    git clone https://github.com/Moreno98/hmd_project.git
    cd hmd_project
```
### GUI
The interaction between the user and the model can be tested using the GUI.  
This can be achieved by running the following commands using different terminals:
```
    rasa run
    rasa run actions
    sudo docker run -p 8000:8000 rasa/duckling
```
You may now access the GUI opening the ```GUI.html``` file, you can enter the chat by clicking the popup on the bottom left corner.
### Amazon Alexa Skill
If you want to try the amazon alexa skill you may follow the notebook presented during the lectures: [notebook](https://tinyurl.com/rasa-alexa)
#### APL
This project needs the Alexa Presentation Language (APL), in order to activate it go to the dashboard of your Amazon Alexa project, under ```Build > Interfaces``` check the Alexa Presentation Language option. Save and rebuild your model.  
#### APL Document
At this point we need to create a document which is able to interpret the ```alexa_connector``` response for displaying the products, to do so we can create a new document by going to ```Build > Multimodal Responses > Visual > Create with authoring tool``` and create a blank document. You may copy and past the document from ```apl_document.json``` in ```APL > Code view```. You can save and build the model. Now you are able to visualize the products using the APL.  
**_NOTE:_**  Make sure the APL document is saved with the following name: product_list.  
#### Run
The model can be launched running the following commands on different terminals:
```
    rasa run
    rasa run actions
    sudo docker run -p 8000:8000 rasa/duckling
    ngrok http 5005
```
**_NOTE:_**  Make sure the endpoint url saved under ```Build > Endpoint``` is the same used by ```ngrok```, otherwise update it, save and rebuild the model. Below a possible example:
```
https://1f3c-138-37-176-24.eu.ngrok.io/webhooks/alexa_assistant/webhook
```
You may access the chat by using the tab ```Test``` of the Alexa Skill project.  
Here at the left hand side there is the chat and at the right hand side the display.
