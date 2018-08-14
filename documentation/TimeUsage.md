Daily time usage
================

## Week 1, 23.-27.7.2018

**Total: 15h 45 min**

* Mon 1h 30 min
  * beginning lecture
* Tue 2h
  * setting up the development environment
* Wed 6h 30 min
  * project definition
  * making user stories
  * downloading additional software
  * following the tutorial and coding
* Thu 3h
  * following the tutorial and coding
* Fri 3h
  * following the tutorial coding

## Week 2, 30.-34.7.2018

**Total: 23h 30 min**

* Mon 4h
  * hashing passwords
* Tue 5h
  * trying to make tests and failing
  * adding tables to database
  * getting to know the language and libraries
  * feature: adding people
* Wed 4h
  * learning how the forms are supposed to work
  * feature: listing people and editing their names
  * making a database diagram
* Thu 3h 30 min
  * getting to know jinja and macros
  * feature: register an account and change account info
* Fri 7h
  * refactoring
  * updating database diagram
  * merge to master
  * wondering why heroku crashes if I add a test user to its database
  * writing user stories
  * 3 hours: fighting with things working locally but not on server

## Week 3, 6.-10.8.2018

**Total: 21h**

* Mon: 5h
  * helping others
  * refactoring
  * no links to unpermitted features
  * importing things in the corrent order can be hard!
  * learning more complicated flask sqlalchemy use
* Tue: 3h
  * figuring out how to make a form with dynamic select field
  * figuring out how to show different content depending on if user is logged in or not
  * realizing these are easy things to do if you don't try to do them in the wrong way
  * feature: show articles the logged-in user is writing on the index page (writer's name still showing only as an id number)
* Wed: 4h 30 min
  * Making article writer's name appear in the article listing
  * feature: assign an editor-in-charge for an article
  * learning about more complicated sql queries
  * feature: show editor-in-charge in the article listing
  * refactoring
  * do not show empty tables
  * do not show mark-as-ready button for ready articles
  * show ready status as a color
* Thu: 4h 15 min
  * Making tables appear prettier
  * Feature: there are magazine issues
  * Feature: articles belong to an issue
  * Feature: you can see all the articles of a certain issue
  * Trying to figure out how to show the current issue on the nav bar. Failing.
* Friday: 4h 15 min
  * Merging feature branches to master. Fixing code when it broke on server.
  * Finally figuring out how to show the current issue on the nav bar. It was never not-working.
  * Feature: link for adding an article to an issue.
  * Learning about ways to use Bootstrap. Making add article form prettier with flask-bootstrap.

## Week 4, 13.-17.8.2018

**Total: 7h 55 min**

* Mon: 3h 25 min
  * feature: showing one article's info on a single page
  * feature: user can be an admin and admin can delete articles
  * feature: new table synopsis. Article can have a synopsis. Synopsis is shown on article's own page. 
  Synopsis is deleted when article is deleted.
  * do not show add article button to non-editors
  * merging brances to master and fixing bugs
  * TODO: the add article form's 'ready' checkbox does nothing, fix this.
* Tue: 4h 40 min
  * merged a lot of branches to master
  * more test data; separate test data to local db and to heroku db
  * simple solution to different db syntax locally and on heroku
  * feature: article info can be edited
  * dropdown menus on navbar
  * small improvements here and there
  * TODO: own css that makes conditional usage of flask bootstrap easier?
  * TODO: figure out how to implement the different statuses
  * TODO: refactoring, more macros etc. to make coding faster
  * TODO: adding issues (validate name format and uniqueness )
  * TODO: update username ( validate uniqueness )
  * TODO: list dummy users separately