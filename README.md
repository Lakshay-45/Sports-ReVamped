# Sports Revamped
#### Video Demo:  https://youtu.be/8t9txbQCR74
#### Description:

##### Agenda:

This final project was created keeping in mind the lack of a centralised system for institutions, to keep track of their sports records and to show off their ranking in sports on a global basis. Therefore, I have created a centralised ranking system as well as Tournament management system, keeping in mind simplicity of use, by the name of Sports Revamped. Although this web-app is not published right now on a server and the showcasing was done using the development server from my codespace itself, I would love to see this web-app being used by the institutes and governmental institutions in the future.

##### Files used:
##### app.py:
This file contains all the back end code of the web app using flask, as well as uses werkzeug.security library for importing generate hash and check hash functions to store passwords in hash form in the database which is made using sqlite3. It contains various routes for all the pages that are there in the web app and by a design choice, only decorates some of the functions with login required function.

##### helpers.py:
This file contains the function definiton of the login_required decorator, for making sure some fucntions are only available to the institutes themselves, after they have logged in with the correct credentials.

##### sports.db:
This is the database that contains all the data and helps in the management of all tha data related requests on the back end. It has 4 different tables, institute, sport_reg, tournament, students, of which, students table was decommissioned due of the evolution of the idea for the project. This same design caviat is also present throughout the html files in the project, which you will be able to see in the description further.

##### Templates:
##### layout.html:
This file in the heart and soul of all the project and is expanded upon by other html files by using jinja2 syntaxing. It contains a navbar in the head tag, allowing for a mobile friendly view of the web app, making sure it doesn't clutter, keeping it cleans design wise as well. It also contains the name of the project viz. Sports Revamped, which is a link to the home page of the website.

##### add_sport.html:
This file has the decorator of login_required in the app.py file, since it allows the currently logged in institute to register for a new sports of the institute's choosing. It presents the user with a input field where the user can enter the name of the sport they would like their institute to partake in. It also makes sure the field is not empty when the user tries to submit the form and also checks if the institute has already registered for the said sport earlier, to avoid duplicate entries. Once registration process is complete, it takes you back to the screen which shows all the sports the currently logged in institute is registered for.

##### contact.html:
This is a really simple file that extends on the layout.html file and it provides the user with the means for contacting the admin of the web-app which under current circumstances, has my email linked.

##### create_tourney.html:
This file also has the login_required decorator since it allows the currently logged in institute to publish a new tournament for a sport they are already registered for. It has a dropdown that allows the user to select the sport for which to create the tournament, and it contains input fields for the location, name and prize pool(in $) for the tournament being published. Again, this was made it so that none of the fields can be left empty for the registration to be completed, and for the tournameent to finally publish on the web-app. After successful registration of a new tournament, it redirects the user back to the screen where the user can look at all the tournaments that are currently live.

##### index.html:
This was one of the earlier pages that was decommissioned later as its use case declined. It basically contained 2 buttons that would take the user to the login page or the leaderboard, according to the user's command, but later this option was removed and the user is directly taken to the leaderboard page, to reduce redunduncy.

##### insti_admin.html:
This is a really basic page that shows the currently logged in institute all the sports that the institute has registered to participate in, due to which it is also decorated wiith the login_required tag. Further, it is necessary for a institute to be registered for a sport they wish to partake in or to create a tournament for since that is the only way the admin can update the leaderboard for the said institute in the said sport, to maintain global rankings.

##### insti_login.html:
This page allows the institute to login into the system, just so they are able to use various institue specefic features on the web app. This page houses 2 different input fields, one for the institute code/name and another for the password. Again, this page makes sure that none of the fields are empty before the form is submitted and it displays an appropriate error message, if the institute code/name or password in the login credentials don't match the one in the database, shown in the video as well.

##### insti_register.html:
This page allows for new institues to register on the web-app, taking as input the institute code/name and a password on the institute's own choosing and also has a field for the confirmation of the password. Like all the pages before this, it doesn't allow for the input fiels to be empty before the form is submitted and also checks if the institute trying to register already exists or if the password and confirmation password entered is the same. If any of the above conditions are violated, it displays an appropriate error message.

##### leader.html:
This form contains the code for the leaderboard page that is also the page with which the user of the web-app is greeted upon opening the home link. It has a fiter field up-top, which allows the user to filter the leaderboard in accordance to a said sport which the user can select from the dropdown menu. If no sport if selected or if the user has loaded the leaderboard for the first time, the leaderboard shown is an overall leaderboard, which shows the institutes in descending order, basically from highest to the lowest points on the leaderboard by summing all the points a certain institute has accross sports. If the user selects a certain sport from the dropdown menu, the table is updated to contain entries from that sport only. Since anyone can view the leaderboard, this page doesn't require the user to be logged in to the web-app.

##### link_shop.html:
This is a basic page that contains links to various pages pertaining to various businesses that sell sports gear online. This page promotes various online stores such as Decathlon, also providing quality of life features to the user so that they don't have to open up various online sports sellers manually and also gives them a good deal of choice between various online stores, so that the user is well aware of their options.

##### link_tut.html:
This page contains the links to wiki pages of various basic sports, so that any user can quickly look up information on any sport they want to, wether they want to look as the rules of play or the equipment used or want to unserstand the sport in general, the wiki has covered it all.

##### list_tourney.html:
This page shows the list of all the live tournaments that are currently going on when the user first opens the page, after which the user is greeted with a filter dropdown menu that allows the user to filter the various tournaments that are live by their location. If the user has already filtered the list by a said location and wants to look at all the tournaments irrespective of the location once again, the user can just simply leave the filter by dropdown as is and click on filter, which will reload the list with all the tournaments running, without constraints on the location.

##### login.html:
This is also an older page that was removed once the design and idea evolved a little. It contained buttons to take the user to either institute or student login pages but was removed later as the student login page was not required anymore.

##### prize.html:
This page contains all the rules pertaining to the distribution of the prizes (moentary and medals,etc. if applicable) and points on the web app. All these rules were hand crafted by me, and i tried to keep in mind all the edge case scenarios that can occur while writing these rules.

##### register.html:
Again, this page was designed at an earlier state of the project which allowed for both student and institute registrations and this page contained links to both the said paages, but was also removed since student registration wasn't required anymore.

##### rem_sport.html:
This page allows the currently logged in institute to remove any sport from their portfolio that they don't wish to take part in anymore. It contains a dropdown that contains the names of all the sports the current institute is registered for and allows the institue to select any sport they wish to. Further, it makes sure that the user selected a sport before trying to submit the form and if the user doesn't select a sport before submitting the form, it displays an appropriate error message. Finally, when the sport is removed from the database, the page redirects the user to the page where the user can see all the sports the institute is now registered for after the said update.

##### rem_tourney.html:
This page allows the currently logged in institute to take down a tournament from the web-app once it has completed, by allowing the user to remove the tournament from the database with the help of a dropdown menu that lists the name of the tournaments that are currently running under the said institute.

##### student_login.html:
This was an older page that was removed later, which allowed the students to log in to the web-app.

##### student_register.html:
This was also an older page that allowed students to register on the web-app, but was removed later.

##### static:
This folder contains various images that were tested out for the background of the web-app as well as the styles.css file.

##### styles.css:
This file contains various styling features for all the html pages as well as the background image for all the pages. Even so, the length of the file isn't very long since most of the styling of the web-app was done through bootstrap.

##### flask_session:
This contains data pertaining to the various sessions that were run during and after the development of the web-app.

##### Others:
If I forgot to mention any other feature in this readme file, I would like to apologise and would request you to take a look at the video link above since it contains showcasing of all the features of the web-app, if not done so already.

##### Thank You
