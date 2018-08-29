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

**Total: 22h 10 min**

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
  * TODO: update username ( validate uniqueness )
  * TODO: list dummy users separately
* Wed: 7h 30 min
  * feature: add issues
  * feature: admin can remove issues
  * feature: list oprhan issues
  * learning more stuff about flask bootstrap
  * major improvements to UI
  * refactoring
  * feature: status bar to show progress
  * feature: control status with sliders
* Thu: 4h 15 min
  * redesigning the list articles page with grids
  * merging a lot of branches to master
  * fixing small things, testing stuff, learning more about bootstrap
* Fri: 4h
  * UI designing
  * Playing with Bootstrap and redoing article list as an accordion

## Week 5, 20.-24.8.2018

**Total: 25h 45 min**

* Mon: 10h
  * Tweaking article list UI
  * Studying what is possible with Bootstrap
  * Fixing little things
  * Removing old stuff
  * Updating status redirects back to the same page
  * Article card stays open when updating status
  * When succesfully updating status, notification is shown for 2s
  * TODO: make it possible to possible to mark article ready again
  * TODO: make it possible to view single article again
  * FIX: when pressing browser's "back" button, alert is repeated if there was one
* Tue: 4h 45 min
  * Articles can be deleted again
  * Deleting or editing an article redirects to the page you came from
  * Lots of refactoring to make all this possible and clean-ish
  * TODO: article updating on the same page the card is shown
  * TODO: alerts when updating article info ^
  * Giving the application for a test user to test, observing and taking notes
* Wed: 5h
  * Fixing issues the test user from yesterday found
  * Putting back add article button to the article listing page
  * Removing forms with a single field from their own page and combining them with another page
  * Refactoring code so that alerts can be shown when database is updated
  * Improving the UI
  * TODO: fix: tasks page shows name two times (title and "name in system")
  * TODO: use names somehow, e.g. make a search function
* Thu: 3 min
  * Writing How to Use and Deployment instructions
  * Fixing a bug
  * TODO: Normalize database?
  * TODO: Update database diagram
  * Feature: delete users
* Friday: 3h ?
  * ?

## Week 6, 27.-31.8.2018

**Total: 15h**

* Monday 5 h
  * Feature: Picture units
  * Feature: add pictures
* Tuesday 10 h
  * Feature: edit and delete pictures
  * Feature: list pictures
  * Feature: new roles: picture_editor, language_consultant, layout_artist
  * feature: picture editor can mark pictures ready
  * feature: language_consultant can set themselves as the language consultant of an article
  * feature: language_consultant of an article can mark it language_checked
  * TODO: admin can make users editors, language consultant, picture editors and layout artists
