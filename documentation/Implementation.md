On implementation
=================

The forms in the project make POST request mostly to the **same address they appear in**. Hidden input fields with descriptive names tell the request handler what the request is in question.

There application uses a macros called ```articlecard_macro.html``` and ```picturecard_macro.html```. They represent the cards that can be seen on different pages of the website. They are used throughout the different pages. They include forms, and for that reason, the same request can be directed to different addresses, there is a centralized POST request handler called ```react_to_post_request.py```. The handler handles other request besides the one coming from the cards as well.

Many of the more complicated database queries are located in the ```help.py``` module. It also contains various methods used throughout the application.

I have tried to refactor longer methods into smaller ones, and in some cases, the result of that has created the ```views_helper.py``` modules.