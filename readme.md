# InfoBot

A silly little python script that allows you to define you own info leaflet telegram bot using xml

## Setting up

- Install requirements for the project
  ```shell 
  pip install -r requirements.txt
  ```
- Put your bot's token into a file named `token`
  ```shell
  echo BOT_TOKEN > token
  ```
- Put pages information into `pages.xml` (see below for details)
- Start your bot by running `main.py`
  ```shell
  python main.py
  ```

## Defining pages

InfoBot uses a single xml file to define content of the leaflet.

### The xml file can have the following tags:

- `<page>` - a page element
- `<content>` - a element defining the content of a page
- `<button>` - a button that calls a custom callback

### The xml file has the following format:

- The root element has to be a `<page>`
- Every `<page>` element has to have exactly 1 `<content>` element
- `<page>` elements can contain any number of other `<page>` or `<button>` elements
- `<page>` and `<button>` elements should have a title attribute specified.
  This will define what is written on the page's transition button
- `<content>` should have its contents written in accordance with telegram's markdown_v2 (has little to do with actual
  markdown) and should have all lines formatted exactly how they have to show up in the message (i.e no leading tabs)

### Example pages.xml:
```xml
<!-- This file contains definitions of pages that the bot will display -->
<page title="info"> <!-- the title of a unit defines what is written on the button that transitions you to the unit -->
    <content> <!-- the content element defines the text contained within each page. every page element has to have exactly 1 content element -->
Lorem ipsum dolor sit amet\, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua\.
    </content>
    <page title="Page A"> <!-- page element may contain any number of other page elements -->
        <content>
*Sed ut perspiciatis unde omnis iste natus error*

sit voluptatem accusantium doloremque laudantium, totam rem
aperiam\, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
explicabo\.
Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit
        </content>
        <page title="Page A1">
            <content>
Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam\, nisi ut
aliquid ex ea commodi consequatur\? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse
quam nihil molestiae consequatur\, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur\?
            </content>
        </page>
        <page title="Page A2">
            <content>
At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum
deleniti atque corrupti
quos dolores et quas molestias excepturi sint occaecati cupiditate non provident\, similique sunt in
culpa qui officia deserunt mollitia animi\, id est laborum et dolorum fuga\.
            </content>
        </page>
    </page>
    <page title="Page B">
        <content>
            At vero eos et accusamus et iusto odio dignissimos
        </content>
        <button title="Action A"> <!-- page elements can also contain button elements, these will call a callback function when clicked by the user. This one will call example_callback-->
            example_callback
        </button>
    </page>
</page>
```