# User stories

**User** is a person who engages with the application.

**Person** is a person in the application database, who is not necessarily a user but can be.

**Issue** refers to a magazine issue.

A **picture editor** is always an **editor** as well.

## As a user

- [x] I can create an account, so that I can be logged-in.

## As a user who has an account

- [x] I can log-in so that I can do things I otherwise could not.

## As a logged-in user

- [x] I can change the name and password associated to my account.
- [ ] I can see articles in the system.
  - [x] I can see the article's name
  - [ ] I can see the article's title, subtitle and table-of-contents text
  - [x] I can see the writer of the article
  - [x] I can see the editor-in-charge of the article
  - [ ] I can see the language consultant of the article
  - [ ] I can see the layout artist of the article
  - [ ] I can see the writing status, editing status, language consultation status and all-around (layout) status of the article
  - [ ] I can see the amount of pages of the article
- [ ] I can add names related to my account.
- [ ] I can remove names related to my account.
- [ ] I can see the unfinished tasks I am related to, so that I know what I have yet to be done.
  - [x] I can see the unfinished articles whose writer I am.
  - [ ] I can see the unfinished articles whose language consultant I am.
  - [ ] I can see the unfinished picture units whose artist I am.
- [ ] I can edit the status of a task I am related to, so that I can let other people know of my progress.
  - [ ] As a writer, I can edit the article's writing status
  - [ ] As a language consultant, I can edit the article's language consultation status
  - [ ] As an artist, I can edit the picture unit's completition status
- [ ] I can request editor previledges
- [ ] I can request to be associated with an existing dummy-account

## As a logged-in user who is an editor

- [x] I can add an issue to the system, provided that there is no issue with the same number already in the system, so that articles can be associated with it.
- [x] I can add people in the system, so that they can be associated with tasks such as writing or editing an article or creating a  picture unit.
- [x] I can add names to the people in the system, so that searches using those names will find the right person.
- [x] I can remove names of the people in the system, so that a name that was typoed or that is wrong will not stay in the system.
- [x] I can add an article in the system, provided that I give it a name, so that other editors will know what articles are coming in the future issues.
  - [x] I can associate the article to an issue
  - [x] I can associate an editor as the editor-in-charge of the new article.
  - [x] I can associate a person as the writer of the new article.
  - [ ] I can associate a person as the language consultant of the new article.
  - [ ] I can associate an editor as the layout artist of the new article.
  - [ ] I can give the new article a title, subtitle and a table-of-contents text.
  - [ ] I can give the new article an amount of pages.
  - [ ] I can give the new article a writing status.
  - [x] I can give the new article a synopsis.
- [x] I can see the unfinished articles whose editor-in-charge I am, so that I can keep track of their progress.
  - [ ] I can add picture units to those articles, so that I can let the picture editor know that pictures are provided or needed.
    - [ ] I can associate myself as the artist of those picture units.
- [ ] I can see the articles whose layout artist I am, so that I can keep track of their progress and I will know when they are ready for layout phase.
- [ ] I can edit all the information related to articles.
  - [ ] I can edit the name of the article
  - [ ] I can edit the issue associated with the article
  - [ ] I can edit the writer of the article.
  - [ ] I can change or add the editor-in-charge of the article.
  - [ ] I can edit the amount of pages of the article.
  - [ ] I can edit the title of the article.
  - [ ] I can edit the subtitle of the article.
  - [ ] I can edit the table-of-contents text of the article.
  - [ ] I can edit the writing status of the article.
  - [ ] I can edit the editing status of the article.
  - [ ] I can edit the language consultation status of the article.
  - [ ] I can edit the layout artist of the article.
  - [ ] I can edit the synopsis of the article.
- [ ] I can see what tasks other users have been associated with, so that I can get a feeling of how they are proceeding.
- [ ] I can grant editor previledges to another user
- [ ] I can associate a registered user with a dummy-account
- [ ] I can update the status of a picture unit, so that I can let other editors know, for example, where the picture file is located

## As a logged-in user who is a picture editor

- [ ] I can add picture units to an article, so that editors can keep track of what pictures are coming to an article.
- [ ] I can associate a person with a picture unit, so that people will know whose task is to do that picture.
- [ ] I can edit all the information related to the picture units.
- [ ] I can remove a picture unit, so that if I create a reduntant picture unit or if a picture order is cancelled, it will not be left hanging in the system, confusing users.