# User stories, updated 27.8.2018 16:36

**User** is a person who engages with the application.

**Person** is a person in the application database, who is not necessarily a user but can be.

**Issue** refers to a magazine issue.

An **admin** is always an **editor**, **language consultant** and **picture editor** as well (not enforced).

A **picture editor** is always an **editor** as well (not enforced).

## As a user

- [x] I can create an account, so that I can be logged-in.
- [x] I can see articles in the system.
  - [x] I can see the article's name
  - [ ] I can see the article's title, subtitle and table-of-contents text
  - [x] I can see the writer of the article
  - [x] I can see the editor-in-charge of the article
  - [ ] I can see the language consultant of the article
  - [ ] I can see the layout artist of the article
  - [x] I can see the writing status, editing status of the article
  - [x] I can see the language consultation status of the article
  - [ ] I can see the layout status of the article
  - [ ] I can see the amount of pages of the article

## As a user who has an account

- [x] I can log-in so that I can do things I otherwise could not.

## As a logged-in user

- [x] I can change the name and password associated to my account.

- [x] I can see the unfinished tasks I am related to, so that I know what I have yet to be done.
  - [x] I can see the unfinished articles whose writer I am.
  - [x] I can see the unfinished articles whose language consultant I am.
  - [x] I can see the unfinished picture units whose artist I am.

## As a logged-in user who is an editor

- [x] I can add an issue to the system, provided that there is no issue with the same number already in the system, so that articles can be associated with it.
- [x] I can add people in the system, so that they can be associated with tasks such as writing or editing an article or creating a  picture unit.
- [x] I can add names to the people in the system, so that searches using those names will find the right person.
- [x] I can remove names of the people in the system, so that a name that was typoed or that is wrong will not stay in the system.
- [x] I can add an article in the system, provided that I give it a name, so that other editors will know what articles are coming in the future issues.
  - [x] I can associate the article to an issue
  - [x] I can associate an editor as the editor-in-charge of the new article.
  - [x] I can associate a person as the writer of the new article.
  - [ ] I can give the new article a title, subtitle and a table-of-contents text.
  - [ ] I can give the new article an amount of pages.
  - [x] I can give the new article a writing status.
  - [x] I can give the new article a synopsis.
- [x] I can see the unfinished articles whose editor-in-charge I am, so that I can keep track of their progress.
- [x] I can add picture units to articles, so that the picture editor knows that pictures are provided or needed.
- [x] I can associate a user as the responsible person for those picture units.
- [ ] I can see the articles whose layout artist I am, so that I can keep track of their progress and I will know when they are ready for layout phase.
- [ ] I can edit all the information related to articles.
  - [x] I can edit the name of the article
  - [x] I can edit the issue associated with the article
  - [x] I can edit the writer of the article.
  - [x] I can change or add the editor-in-charge of the article.
  - [x] I can edit the writing status of the article.
  - [x] I can edit the editing status of the article.
  - [x] I can edit the synopsis of the article.
  - [ ] I can edit the amount of pages of the article.
- [x] I can see what tasks other users have been associated with, so that I can get a feeling of how they are proceeding.
- [x] I can update info of a picture unit
  - [x] I can update the progress status of a picture unit
  - [x] I can update the description of a picture unit
  - [x] I can update the person responsible for a picture unit

## As a logged-in user who is a language consultant

- [x] I can mark myself as the language consultant of an article that is 100% written and edited so that other language consultants know not to language check this article
- [x] I can mark articles whose language consultant I am as being language-checked

## As a logged-in user who is a picture editor

- [x] I can mark pictures that are 100% done (status is 100) as being ready

## As a logged-in user who is a layout artist

- [ ] I can mark articles that are language-checked and whose pictures are ready as ready.

## As a logged-in user who is an admin

- [x] I can delete issues from the system
- [x] I can delete articles from the system
- [x] I can grant editor previledges to another user
- [x] I can take editor previledges away from a user
- [x] I can remove a picture unit, so that if I create a reduntant picture unit or if a picture order is cancelled, it will not be left hanging in the system, confusing users.
- [x] I can remove users
- [ ] I can associate a registered user with a dummy-account