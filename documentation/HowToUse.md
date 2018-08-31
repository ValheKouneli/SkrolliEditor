How to Use
==========

## The editorial process of Skrolli

First, there is an issue. Skrolli publishes four issues per year, and sometimes English language issues.
Then there are articles. Article starts as an idea ('planned'). It might have a writer, but not necessarily. For example, we migh just decide that __someone__ should write an article about the latest Assembly.

The article writer can be anyone. They do not work on the article on their own, but the article always has an **editor-in-charge** (vastuutoimittaja) who takes care of the article. The editor-in-charge edits the text and takes care that the article is finished in time.

The article will need pictures, of course. There are different types of pictures, such as graphs, photographs and illustrations. The person who draws the illustation or takes the photo is often not the same as the writer of the article. The people responsible for the pictures are come outside of the editorial team. Just like in the case of an article text, a picture is never printed in the magazine unless someone from the editorial team has approved it. This person is the **picture editor** (kuvatoimittaja). Even if the creator of the picture thinks it's ready and all the editors think it's ready, the picture editor has to approve it so it can be marked ready.

But wait! Even the article text is not ready after the editor-in-charge says so. The **language consultant** has to read it and correct the grammar and make sure everything is in check. The language consultant can be from outside of the editorial team and thus not one of the editors. There can be many language consultants working concurrently.

The pictures for the article and the text of the article progress independent of each other. The picture editor is somewhat interested in the text status of the articles, and the editor-in-charge is also partially responsible that there are appropriate pictures coming for the article.

After both the text and the pictures are ready, the layout artist can put the article together. After that it still need to be proof-read...

# The application

SkrolliEditor's version on 31.8.2018 supports six types of user accounts: **admin**, **editor**, **language consultant**, **picture editor** and **assistant**. Admin has all the other roles as well. Assistant accounts do not have any special previledges, and at the moment; they can only view the content in the system and not manipulate it.

Only picture editor can mark pictures ready, and only language consultants can mark articles 'language checked' i.e. 'Finished'. Editor accounts have all the other priviledges to manipulate the data except to delete users, issues and articles. Only admins can delete them. Admin can make other registered users editors. At the moment, there is no way to make other users picture editors or language consultants. Newly registered users have assistant accounts.

Users can access different content via the dropdown menus on the top of the page, in the navbar.


## The article view

The article views show the articles separated into five different categories: planned, draft, written, edited and finished. The **status** of the article determines which category the article belongs to. When the article is written, edited and 'language checked', it belongs to the 'Finished' category.

By clicking the article title in the article view, the article card opens and shows information about the article. **JavaScript must be enabled** in the browser.

The article card title shows a small pill saying either "no pics" or "pics". The color of this pill represents the status of the article's pictures. By clicking the pill or the "More" button in the open article card user can see the overall view of the article.

The two progress bars represent the **writing status** and the **editing status** of the article. Editors can change these by using the sliders under the progress bars (visible only to editors). After adjusting the sliders, editor must press the "update sliders" button to apply the change.

When article is created, it belongs to the 'planned' category. When writing has been started (status is something else than 0 %), article moves into the 'draft' category. When writing status is 100 %, article is 'written'. Bringing the editing status to 100 % moves it to the 'edited' category. In this view, articles can not be moved to the 'Finished' category.

Note that the editing status can never be higher than the writing status, as content that has not been written can not be edited.

An **orphan article** means an article that belong to no particular issue.

## The (view as) langauge consultant page

The page lists all the articles that are both written and edited but not 'language checked'. On the page, a language consultant can 'grab' articles that are written and edited (but not language checked). Grabbing means that they indicate to other language consultant they are working on that article. Once they have grabbed an article, they can mark their work as ready: the article becomes 'language checked' and in the article view, it is moved in to the 'Finished' section.

## The (view as) picture editor page

The page lists all the pictures whose status is 100 but are not marked ready. On the page, a picture editor can mark those pictures ready.

## The pictures view

The pictures view small all the pictures in the system as cards that can be opened. The title tells what type of picture it is and the name after the arrow tells the name of the article it belongs to.

There is a small pill that says "text" on the card header. Its color indicates the status of the article's text. By clicking the pill or the More button on the opened card, user can see the overall view of the article the picture belongs to.

When the card is opened, there is a progress bar that indicates this pictures status. Editors can change this by using the slider that is only visible to them, just like in the article view.

## The users view

The users view shows all the users in the system. The users with no username are so-called 'dummy users', that can be set as a writer of an article, but that can not be used to log into the system. The users can have aliases, which do not have any meaning at the moment. (Later, there will be a search function that uses the aliases.)

Editors can add new dummy users to the system and add and remove aliases to/from all existing users.
Admin can delete users and make registered users editors or remove editor privilegres from editors (including themselves at the moment).

By clicking the name of an user in the list, one can access the **'tasks page'** of that user. It shows what articles that user is writing and editing.

Editors see an 'edit' link next to the username. They can add and remove aliases to the user on the page behind the link.


## The issues view

The issues view shows all the current **magazine issues** in the system. Editors can add new issues, but their name must follow a strict format: 2018.1, 2018.1E, 2018.2 ... 2018.4, 2019.1 ...

## My page

The 'my page' view is same as the **tasks page** for your account. Naturally, you can only access 'my page' if you have logged-in to the system. The page shows articles you are writing, article's you are editing, pictures you are responsible of, and language editors see the articles they have 'grabbed' on this page as well.

## The forms in the system

A red start bedisides the form field label indicates that the field is required. Otherwise, the field can be left as empty.

## Deleting articles and issues

Admin can delete an article by clicking the delete-button on the bottom left on the article card. All the pictures related to that article are deleted as well. The system will show no warning but deletes the article instantly.

Admin can delete a picture by clicking the delete-button on the botton left on the picture card. The system will show no warning.

Admin can delete an issue by cliking the red 'x' button on the bottom right on the issue card. The system will show no warning but deletes the issue instantly. All the articles that belonged to the issue will be made **orphans**.