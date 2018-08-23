How to Use
==========

SkrolliEditor application supports three types of user accounts: **admin**, **editor** and **assistant**. Admins are also editors always. Assistant accounts do not have any special previledges, and at the moment; they can only view the content in the system and not manipulate it. Editor accounts have all the priviledges to manipulate the data except to delete issues and articles. Only admins can delete them. Newly registered users have assistant accounts, and at the moment (23.8.2018), there is no way to give previledges to accounts via the user interface.

Users can access different content via the dropdown menus on the top of the page, in the navbar.


## The article view

The article views show the articles separated into five different categories: planned, draft, written, edited and finished. The **status** of the article determines which category the article belongs to.

By clicking the article title in the article view, the article card opens and shows information about the article. **JavaScript must be enabled** in the browser. The picture-pill in the article card header does not have any meaning yet.

The two progress bars represent the **writing status** and the **editing status** of the article. Editors can change these by using the sliders under the progress bars (visible only to editors). After adjusting the sliders, editor must press the "update sliders" button to apply the change.

When article is created, it belongs in the 'planned' category. When writing has been started (status is something else than 0 %), article moves into the 'draft' category. When writing status is 100 %, article is 'written'. Bringing the editing status to 100 % moves it to the 'edited' category. There is no way, at the moment, to mark the article as 'finished'. Note that the editing status can never be higher than the writing status, as content that has not been written can not be edited.

An **orphan article** means an article that belong to no particular issue.

## The users view

The users view shows all the users in the system. The users with no username are so-called 'dummy users', that can be set as a writer of an article, but that can not be used to log into the system. The users can have aliases, which do not have any meaning at the moment. (Later, there will be a search function that uses the aliases.)

Editors can add new dummy users to the system and add and remove aliases to/from all existing users.

By clicking the name of an user in the list, one can access the **'tasks page'** of that user. It shows what articles that user is writing and editing.

## The issues view

The issues view shows all the current **magazine issues** in the system. Editors can add new issues, but their name must follow a strict format: 2018.1, 2018.1E, 2018.2 ... 2018.4, 2019.1 ...

## My page

The 'my page' view is same as the **tasks page** for your account. Naturally, you can only access 'my page' if you have logged-in to the system.

## The forms in the system

A red start bedisides the form field label indicates that the field is required. Otherwise, the field can be left as empty.

## Deleting articles and issues

Admin can delete an article by clicking the delete-button on the bottom left on the article card. The system will show no warning but deletes the article instantly.

Admin can delete an issue by cliking the red 'x' button on the bottom right on the issue card. The system will show no warning but deletes the issue instantly. All the articles that belonged to the issue will be made **orphans**.