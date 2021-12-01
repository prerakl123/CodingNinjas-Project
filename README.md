# Coding Ninjas Programs

## Random Password Generator
Generates a password based on user input as well as generates a computer generated password

## Spin a Yarn
Spin a Yarn (aka MadLibs) is a fun game where simple words are inputted and replaced in an already created story resulting in a funny story.

----

----

Although I haven't completed the Spin a Yarn program but the spin a yarn story creator becomes self explanatory, if the JSON file is read and also the code is read and run once.

The simple idea behind it's creation is that the Name entered for an entry type or a combo box drop down item type when placed inside dunders, capitalized with special characters
remove becomes valid for ID and string replacement inside the story string. So in the story `__NAME__` acts as the ID and replacement string, to be used in regex.

The JSON pattern for storing the story is somewhat like:


```json
{
  "STORY NAME": {
    "story_path": "./...",
    "input_and_values": {
      "name1": {
        "type": "entry",
        "value": "",
        "replacement_id": "__NAME1__"
      },
      "name2": {
        "type": "combo",
        "value": [],
        "replacement_id": "__NAME2__"
      }
    }
  }
}
```
