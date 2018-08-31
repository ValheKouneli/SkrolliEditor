# SkrolliEditor

This is a school project for Helsinki University's course Database Application.

A web application to help the editorial process of Skrolli

https://skrollieditor.herokuapp.com/

**Test user**
* username: editor or admin
* password: [the Finnish word for test repeated twice in lower case]

## Documentation

[User stories](/documentation/UserStories.md)

[How to use](/documentation/HowToUse.md)

[Deployment](/documentation/Deployment.md)

[Database diagram](/documentation/Database/DatabaseDiagram.png)

[On implementation](/documentation/Implementation.md)

[Todo](/documentation/Todo.md)

[In Finnish, TSOHAA VARTEN](/documentation/SuomeksiKurssiaVarten.md)

## Project definition

The aim of this project is to create a web application for the editorial team of Skrolli magazine that can eventually replace the current system for managing the editorial process of Skrolli.

Users, who are the editors of Skrolli, can log in and add or update information about upcoming magazine content and view the current status of the magazine-in-the-making. The magazine consists of articles that have both text and pictorial content, whose progress from an idea to completion is simultanious.

The magazine editors have different roles, such as (text) editor, pictorial editor, layout artist (taittaja in Finnish), language consultant (kielenhuoltaja in Finnish), proofreader (vedoskorjaaja in Finnish), treasurer, managing editor and editor in chief. Different roles are interested in different kinds of information related to the status of the magazine.

Each editor is responsible for a set of tasks that are related to the articles. Each articles belongs to a certain magazine number, and articles can be cancelled or delayed to be published in a later number. The most important feature is to be able to add, update and view the information, especially the status information, and to filter the articles based on who is assigned to work on that article and also based on the completition status of the article.

------

There is a lot of other information related to the articles, such as

* magazine it belongs to
* writer(s)
* assigned editor(s)
* number of pages
* location in the magazine
* subject
* category
* title
* subtitle
* page of contents text
* cover text (if featured in the cover)
* synopsis
* text status
* picture status
* language check-up status
* pagination (layout) status
* proof-reading status
* corrections needed
* location of the text file
* deadline
* need for a 'title picture'
* title picture
* need for additional pictures
* additional pictures
* need for graphs
* graphs
* pictures provided by the writer or the editor
* existence of web content
* agreed compensation

Only the most important of these features will be implemented in the initial version of the application.

The additional pictures related to the articles are handled in groups, such as "additional pictures for article's pages 2-4", since the artist has a freedom of choosing the amount of pictures.

There is some infomation related to the picture ensembles, such as:

* type ('title picture' / graph / photo / illustation)
* pages covered
* article it is related to
* idea/specifications of content or size
* artist
* deadline
* completition status
* legend
* agreed compensation

Managing the pictorial content of the magazine is an important part of the application. Only the most important features will be implemented in the initial version of the application.

There are people in the system, and some of them are also users. There is some information related to the people in the system, such as:

* user account
* name
* nickaname
* e-mail
* other contact info
* whether they have signed a contract with Skrolli
* what year's income-tax card they have send to the treasurer
* whether they have send their bank account number to the treasurer
* what they are owed by Skrolli
* what tasks they are assigned to

The information about what has to be paid and to whom is important, and the initial version of the application will have some functionality related to that.


## User stories

[link](/documentation/UserStories.md)
